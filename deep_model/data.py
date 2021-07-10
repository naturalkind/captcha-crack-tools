import os, os.path
import numpy as np
import cv2
import tensorflow as tf
from tensorflow import keras


def see_stat(x, y=0):
    if y == "list":
        print (x.columns.tolist())
    else:
        for c in  x.columns.tolist():
            print (f"###############\n{x[c].value_counts(dropna=False)}")

class DATA(object):
   def __init__(self):
       self.file = {}
       self.label = {}
   def parseIMG(self, dir_name):
       path = dir_name+"/"
       print ("PARSING",path)
       for r, d, f in os.walk(path):
           for ix, file in enumerate(f):
                      Z = r.split("/")
                      Class, Type = Z[1].split("_")[0], Z[1].split("_")[1]
##                      try:
#                      
#                      if Type == "4x4":
#                          #print (Class, Type)
#                          if ".png" in file.lower():
#                              self.file[file.split(".")[0]] = [os.path.join(r, file)]
#                          if ".jpg" in file.lower(): 
#                              self.file[file.split(".")[0]] = [os.path.join(r, file)]
#                          if ".jpeg" in file.lower(): 
#                              self.file[file.split(".")[0]] = [os.path.join(r, file)]     
                    
                      if Type == "3x3":
                          Non_Class = Z[-1].split("_")[0]
                          if ".png" in file.lower():
                              self.file[file.split(".")[0]] = [os.path.join(r, file), Class, Non_Class]
                          if ".jpg" in file.lower(): 
                              self.file[file.split(".")[0]] = [os.path.join(r, file), Class, Non_Class]
                          if ".jpeg" in file.lower(): 
                              self.file[file.split(".")[0]] = [os.path.join(r, file), Class, Non_Class]                              


                      if ".csv" in file:
                          self.label[file.split(".")[0]] = [os.path.join(r, file), Class]
                          
def imgs(x):
      cv2.imshow('Rotat', np.array(x).astype(np.uint8))
      cv2.waitKey(0)
      cv2.destroyAllWindows()              

def cutimg(data, col):
                im_w, im_h, im_c = data.shape
                w, h = im_w//col, im_h//col
                w_num, h_num = int(im_w/w), int(im_h/h)
                num = []
                for wi in range(0, w_num):
                    for hi in range(0, h_num):
                        num.append(data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
                        #cutpart = data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :]
                return num

def img4x4():
    P = DATA()
    P.parseIMG("extract") 
    print (len(P.file), len(P.label))  
    for o in P.label:
        F = open(P.label[o][0],"r").readlines()
        Class = P.label[o][1]
        try:
            os.mkdir(f"out/{Class}")
        except FileExistsError:
            print ("Error")    
        for o in F[:50000]:
            _temp = o.split("\n")[0]
            _id = _temp.split(";")[0]
            _answ = _temp.split(";")[1]
            try:
                if _answ != "no_matching_images":
                    _answ = _answ.split(":")[-1].split("/")
                    print (P.file[_id][0], _answ, Class) 
                    # Image open
                    img = cv2.imread(P.file[_id][0])
                    list_img = cutimg(img, 4)
                    for a in _answ:
                        
                        #imgs(list_img[int(a)-1])
                        cv2.imwrite(f"out/{Class}/{_id}_{int(a)-1}_{Class}.jpg", list_img[int(a)-1])
            except KeyError:
                pass  
                          
if __name__ == '__main__':
#    P = DATA()
#    P.parseIMG("extract") 
#    print (len(P.file), len(P.label))  
#    for o in P.file:
#        if P.file[o][2] != "not":
#            try:
#                os.mkdir(f"out/{P.file[o][1]}")
#            except FileExistsError:
#                print ("Error")  
#            print (f"out/{P.file[o][1]}/{o}_{P.file[o][1]}.jpg", P.file[o][0], P.file[o][1], P.file[o][2])
#            img = cv2.imread(P.file[o][0])
#            #imgs(img)
#            cv2.imwrite(f"out/{P.file[o][1]}/{o}_{P.file[o][1]}.jpg", img)

# OPEN ----------------------------------->
#    S = {}
#    for r, d, f in os.walk("out/"):
#        for ix, file in enumerate(f):  
#            #print (file) 
#            #img = cv2.imread(os.path.join(r, file))
#            Class = file.split(".")[0].split("_")[-1]
#            S[Class] = 1
#            #imgs(img)
#    print (len(S), S)            
#            
##18 class
##{'palms':, 'bicycles': 1, 'cars': 1, 'signs': 1, 'mountains': 1, 'hydrants': 1, 'sculptures': 1, 'buses': 1, 'taxis': 1, 'motos': 1, 'boats': 1, 'trees': 1, 'tractors': 1, 'bridges': 1, 'stairs': 1, 'chimney': 1, 'crosswalks': 1, 'taxi': 1}
#    code_to_vec = {}
#    code_to_class = {}
#    for ix, o in enumerate(S):
#        print (ix, o)
#        code_to_class[ix] = o
#        code_to_vec[o] = ix
#    print (code_to_class, code_to_vec)

#    image_data_generator = keras.preprocessing.image.ImageDataGenerator(featurewise_center=False,dtype='float32')
#    dataset = keras.preprocessing.image.DirectoryIterator('out', image_data_generator, batch_size=64, target_size=(128, 128))
#    print (dataset)
#    for i in dataset:
#        imgs(i[0])
        #print (i[0], i[1])
        
    image_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(featurewise_center=False, dtype='float32', rescale=True, rotation_range=5, validation_split=0.2)
    print (dir(image_data_generator))
    dataset_train = image_data_generator.flow_from_directory(
                                                        'out',
                                                        target_size=(128, 128),
                                                        batch_size=64,
                                                        class_mode='categorical',
                                                        shuffle=True,
                                                        subset="training")
                                                         
    dataset_val = image_data_generator.flow_from_directory(
                                                        'out',
                                                        target_size=(128, 128),
                                                        batch_size=64,
                                                        class_mode='categorical',
                                                        shuffle=True,
                                                        subset="validation")                                                         
    print (dir(dataset_train), dataset_train.class_indices)
#    dataset = tf.keras.preprocessing.image.DirectoryIterator('out', image_data_generator, batch_size=64, target_size=(128, 128), shuffle=True)
    print (len(dataset_train), len(dataset_val))
    classes = dataset_train.class_indices
    indexs = {}
    for i in classes:
        indexs[classes[i]] = i
    def unzip(b):
        xs, ys = zip(*b)
        xs = numpy.array(xs)
        ys = numpy.array(ys)
        return xs, ys  
    test_xs, test_ys = dataset_val[0]
    print (test_ys[0])
    for batch_idx, (batch_xs, batch_ys) in enumerate(dataset_train):
        print (batch_idx, batch_ys)
#    for i in dataset:
#        #imgs(i[0][0])
#        print (i[0].shape, i[1].shape)
#        #imgs(i[0][0]*.255)
#        print (vec_to_plate(i[1][0]))  
              

    """
    Сначала отсортировать 4x4
    Затем получить 3x3
    """

