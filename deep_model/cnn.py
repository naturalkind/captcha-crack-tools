import os, os.path
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import layers

class DATA(object):
   def __init__(self):
       self.file = {}
       self.label = {}
   def parseIMG(self, dir_name):
       path = dir_name+"/"
       print ("PARSING",path)
       for r, d, f in os.walk(path):
           for ix, file in enumerate(f):
                          if ".png" in file.lower():
                              self.file[file.split(".")[0]] = [os.path.join(r, file), Class, Non_Class]
                          if ".jpg" in file.lower(): 
                              self.file[file.split(".")[0]] = [os.path.join(r, file), Class, Non_Class]
                          if ".jpeg" in file.lower(): 
                              self.file[file.split(".")[0]] = [os.path.join(r, file), Class, Non_Class]    
                                                        
def imgs(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()              


def get_loss(y, y_):
    # Calculate the loss from digits being incorrect.  Don't count loss from
    # digits that are in non-present plates.
    digits_loss = tf.nn.softmax_cross_entropy_with_logits(
                                          logits=tf.reshape(y[:, 1:],
                                                     [-1, len(common.CHARS)]),
                                          labels=tf.reshape(y_[:, 1:],
                                                     [-1, len(common.CHARS)]))
    digits_loss = tf.reshape(digits_loss, [-1, 9])
    digits_loss = tf.reduce_sum(digits_loss, 1)
    digits_loss *= (y_[:, 0] != 0)
    digits_loss = tf.reduce_sum(digits_loss)

    return digits_loss

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)


def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def res_net_block(input_data, filter_count):
  x = slim.conv2d(input_data, filter_count, (1, 1), padding="SAME", activation_fn=tf.nn.relu)
  x = slim.conv2d(x, filter_count, (3, 3), padding="SAME", activation_fn=None)
  x = tf.nn.relu(x)
  x = slim.conv2d(x, filter_count, (1, 1), padding="SAME", activation_fn=None)
  x = tf.add(x, input_data)
  x = tf.nn.relu(x)
  return x


def convolutional_layers():
    """
    Get the convolutional layers of the model.
    """
    x_ = tf.placeholder(tf.float32, [None, 128, 128])
    x_expanded = tf.expand_dims(x_, 3)
    is_training = tf.placeholder(tf.bool, [])
    print ("IN", x_expanded.shape)
    # First layer
    strides = 1
    with slim.arg_scope([slim.conv2d],
                        normalizer_fn=slim.batch_norm,
                        normalizer_params={'is_training': is_training}):
        x = slim.conv2d(x_expanded, 32, (3, 3), stride=strides, padding="SAME", activation_fn=tf.nn.relu) 
        x = slim.max_pool2d(x, kernel_size=2, stride=2)
        print (x.shape)
        x = slim.conv2d(x, 64, (3, 3), stride=strides, padding="SAME", activation_fn=tf.nn.relu) 
        x = slim.max_pool2d(x, kernel_size=2, stride=2)        
        x = res_net_block(x, 64)
        print (x.shape)
        x = slim.conv2d(x, 128, (3, 3), stride=strides, padding="SAME", activation_fn=tf.nn.relu) 
        x = slim.max_pool2d(x, kernel_size=2, stride=2)
        x = res_net_block(x, 128)    
        print (x.shape)
        x = slim.conv2d(x, 128, (3, 3), stride=strides, padding="SAME", activation_fn=tf.nn.relu) 
        x = slim.conv2d(x, 256, (3, 3), stride=strides, padding="VALID", activation_fn=tf.nn.relu) 
        x = res_net_block(x, 256)
        x = slim.conv2d(x, 256, (2, 2), stride=strides, padding="VALID", activation_fn=tf.nn.relu) 
        x = slim.conv2d(x, 256, (3, 3), stride=strides, padding="VALID", activation_fn=tf.nn.relu) 
        print (x.shape)  
        x = res_net_block(x, 256)
        x = slim.conv2d(x, 256, (2, 2), stride=strides, padding="VALID", activation_fn=tf.nn.relu)  
        print (x.shape)
        # Densely connected layer
        W_fc1 = weight_variable([2 * 10 * 256, 2048])
        b_fc1 = bias_variable([2048])
        conv_layer_flat = tf.reshape(x, [-1, 2 * 10 * 256])
        h_fc1 = tf.nn.relu(tf.matmul(conv_layer_flat, W_fc1) + b_fc1)
     
        W_fc2 = weight_variable([2048, 1 + 9 * len(common.CHARS)])
        b_fc2 = bias_variable([1 + 9 * len(common.CHARS)])

        y = tf.matmul(h_fc1, W_fc2) + b_fc2
     
        
        return x_, y, is_training
    

def train(learn_rate, report_steps, batch_size, initial_weights=None):
    x, y, is_training = convolutional_layers()
    y_ = tf.placeholder(tf.float32, [None, 1 * len(common.CHARS)])
    loss = get_loss(y, y_)
    train_step = tf.train.AdamOptimizer(learn_rate).minimize(loss)

    best = tf.argmax(tf.reshape(y[:, :], [-1, 1, len(CLASSES)]), 2)
    correct = tf.argmax(tf.reshape(y_[:, :], [-1, 1, len(CLASSES)]), 2)

    init = tf.initialize_all_variables()

    def vec_to_plate(v):
        return "".join(CLASSES[i] for i in v)

    def do_report():
        r = sess.run([best,
                      correct,
                      tf.greater(y[:, 0], 0),
                      y_[:, 0],
                      digits_loss,
                      presence_loss,
                      loss],
                     feed_dict={x: test_xs, y_: test_ys, is_training:"False"})
        num_correct = numpy.sum(
                        numpy.logical_or(
                            numpy.all(r[0] == r[1], axis=1),
                            numpy.logical_and(r[2] < 0.5,
                                              r[3] < 0.5)))
        r_short = (r[0][:190], r[1][:190], r[2][:190], r[3][:190])
        for b, c, pb, pc in zip(*r_short):
            print ("{} {} <-> {} {}".format(vec_to_plate(c), pc,
                                           vec_to_plate(b), float(pb)))
        num_p_correct = numpy.sum(r[2] == r[3])
        "B{:3d} {:2.02f}% {:02.02f}% loss: {} (digits: {}, presence: {}) |{}|"
        print (
            batch_idx,
            100. * num_correct / (len(r[0])),
            100. * num_p_correct / len(r[2]),
            r[6],
            r[4],
            r[5],
            "".join("X "[numpy.array_equal(b, c) or (not pb and not pc)]
                                           for b, c, pb, pc in zip(*r_short)))

    def do_batch():
        sess.run(train_step,
                 feed_dict={x: batch_xs, y_: batch_ys, is_training:"True"})
        #imgs(batch_xs[0])
        if batch_idx % report_steps == 0:
            do_report()

    saver = tf.train.Saver()
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.70)
    with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
        if initial_weights is not None:
            saver.restore(sess, "model_slim/model.ckpt")
        else:    
            sess.run(init)

        test_xs, test_ys = unzip(list(read_data("test/*.png"))[:50])
        #imgs(test_xs[3])
        #print test_xs[0], test_ys[0].shape
        try:
            last_batch_idx = 0
            last_batch_time = time.time()
            batch_iter = enumerate(read_batches(batch_size))
            for batch_idx, (batch_xs, batch_ys) in batch_iter:
                #print batch_xs[0].shape, batch_ys[0].shape
                #imgs(batch_xs[3])
                do_batch()
                if batch_idx % report_steps == 0:
                    batch_time = time.time()
                    if last_batch_idx != batch_idx:
                        print ("time for 60 batches {}".format(
                            60 * (last_batch_time - batch_time) /
                                            (last_batch_idx - batch_idx)))
                        last_batch_idx = batch_idx
                        last_batch_time = batch_time

        except KeyboardInterrupt:
             #model.save("h.npz")
             save_path = saver.save(sess, "model_slim/model.ckpt")
             print("Model saved in path: %s" % save_path)
             print ("STOP")

def detect():
    x, y = convolutional_layers()
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.60)
    saver = tf.train.Saver()
    best = tf.argmax(tf.reshape(y[:, 1:], [-1, 9, len(common.CHARS)]), 2)
    with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
        set_session(sess)
        saver.restore(sess, "model_slim/model.ckpt")
        #im = cv2.imread("test/00000035_KA1804AO_1.png")[:, :, 0].astype(numpy.float32) / 255.
        im = cv2.imread("/media/sadko/1b32d2c7-3fcf-4c94-ad20-4fb130a7a7d4/PLAYGROUND/OCR/generate_train/test/00000827_B999EX40_1.png")[:, :, 0].astype(numpy.float32) / 255.
        
        im = np.reshape(im,[1,64,128])
        feed_dict = {x: im, is_training:"False"}
        answ = sess.run(best, feed_dict=feed_dict)
        #letter_probs = (answ[0,0,0,1:].reshape(9, len(common.CHARS)))
        #letter_probs = common.softmax(letter_probs)  
        print (answ.shape, "".join(common.CHARS[i] for i in answ[0]))
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
       initial_weights = sys.argv
    else:
       initial_weights = None

    train(learn_rate=0.001,
          report_steps=20,
          batch_size=50,
          initial_weights=initial_weights)

#    detect()


