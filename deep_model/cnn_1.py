import os, os.path, sys, time
import numpy as np
import cv2
import tensorflow as tf
slim = tf.contrib.slim


image_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(featurewise_center=False, rescale=True, rotation_range=5)
dataset_train = image_data_generator.flow_from_directory(
                                                    'out',
                                                    target_size=(128, 128),
                                                    batch_size=32,
                                                    class_mode='categorical',
                                                    shuffle=True)
                                                     
#dataset_val = image_data_generator.flow_from_directory(
#                                                    'out',
#                                                    target_size=(128, 128),
#                                                    batch_size=64,
#                                                    class_mode='categorical',
#                                                    shuffle=True,
#                                                    subset="validation") 

classes = dataset_train.class_indices
indexs = {}
for i in classes:
    indexs[classes[i]] = i
                                                        
def imgs(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()              


def get_loss(y, y_):
    # Calculate the loss from digits being incorrect.  Don't count loss from
    # digits that are in non-present plates.
    digits_loss = tf.nn.softmax_cross_entropy_with_logits(
                                          logits=tf.reshape(y[:, :],
                                                     [-1, len(classes)]),
                                          labels=tf.reshape(y_[:, :],
                                                     [-1, len(classes)]))
    digits_loss = tf.reshape(digits_loss, [-1, 1])
    digits_loss = tf.reduce_sum(digits_loss, 1)

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
    x_expanded = tf.placeholder(tf.float32, [None, 128, 128, 3])
    is_training = tf.placeholder(tf.bool, [])
    print ("IN", x_expanded.shape)
    # First layer
    strides = 1
    with slim.arg_scope([slim.conv2d],
                        normalizer_fn=slim.batch_norm,
                        normalizer_params={'is_training': is_training}):
        x = slim.conv2d(x_expanded, 3, (3, 3), stride=strides, padding="SAME", activation_fn=tf.nn.relu) 
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
        print ("END",x.shape)
        # Densely connected layer
        W_fc1 = weight_variable([10 * 10 * 256, 2048])
        b_fc1 = bias_variable([2048])
        conv_layer_flat = tf.reshape(x, [-1, 10 * 10 * 256])
        h_fc1 = tf.nn.relu(tf.matmul(conv_layer_flat, W_fc1) + b_fc1)
     
        W_fc2 = weight_variable([2048, 1 * len(classes)])
        b_fc2 = bias_variable([1 * len(classes)])

        y = tf.matmul(h_fc1, W_fc2) + b_fc2
     
        
        return x_expanded, y, is_training
    

#code_to_class = {0: 'palms', 1: 'bicycles', 2: 'cars', 3: 'signs', 4: 'mountains', 5: 'hydrants', 6: 'sculptures', 7: 'buses', 8: 'taxis', 9: 'motos', 10: 'boats', 11: 'trees', 12: 'tractors', 13: 'bridges', 14: 'stairs', 15: 'chimney', 16: 'crosswalks', 17: 'taxi'} 
#code_to_vec = {'palms': 0, 'bicycles': 1, 'cars': 2, 'signs': 3, 'mountains': 4, 'hydrants': 5, 'sculptures': 6, 'buses': 7, 'taxis': 8, 'motos': 9, 'boats': 10, 'trees': 11, 'tractors': 12, 'bridges': 13, 'stairs': 14, 'chimney': 15, 'crosswalks': 16, 'taxi': 17}



def train(learn_rate, report_steps, initial_weights=None):
    x, y, is_training = convolutional_layers()
    y_ = tf.placeholder(tf.float32, [None, 1 * len(classes)])
    loss = get_loss(y, y_)
    train_step = tf.train.AdamOptimizer(learn_rate).minimize(loss)

    best = tf.argmax(tf.reshape(y[:, :], [-1, 1, len(classes)]), 2)
    correct = tf.argmax(tf.reshape(y_[:, :], [-1, 1, len(classes)]), 2)

    init = tf.initialize_all_variables()

    def vec_to_plate(v):
        return "".join(code_to_class[i] for i in v)

    def do_report():
        r = sess.run([best,
                      correct,
                      loss],
                     feed_dict={x: batch_xs, y_: batch_ys, is_training:"False"})
#        r_short = (r[0][:190], r[1][:190])
#        for b, c in zip(*r_short):
#            print ("{} <-> {}".format(c,b))
            
            
        r_short = (r[0][:190], r[1][:190])
        for b, c in zip(*r_short):
            print ("{} <-> {}".format(c, b))
        "B{:3d} presence: {} |{}|"
        print (
            batch_idx,
            100.*np.sum(r[2])/32,
            "".join("X "[np.array_equal(b, c)] for b, c in zip(*r_short)))            

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

#        test_xs, test_ys = unzip(list(read_data("test/*.png"))[:50])
        test_xs, test_ys = dataset_train[-1]
        test_xs = test_xs.astype(np.float32) / 255.
        test_ys = test_ys.astype(np.float32)
        #imgs(test_xs[3])
        #print test_xs[0], test_ys[0].shape
        try:
            last_batch_idx = 0
            last_batch_time = time.time()
            for batch_idx, (batch_xs, batch_ys) in enumerate(dataset_train):
                batch_xs = batch_xs.astype(np.float32) / 255.
                batch_ys = batch_ys.astype(np.float32) 
                #print (batch_xs[0], batch_xs[0].shape, batch_ys[0].shape, batch_xs.shape, batch_ys.shape)
#                imgs(batch_xs[3])
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
    best = tf.argmax(tf.reshape(y[:, 1:], [-1, 1, len(classes)]), 2)
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
          initial_weights=initial_weights)

#    detect()


