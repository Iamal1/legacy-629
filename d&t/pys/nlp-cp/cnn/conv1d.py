#-*- coding=utf-8 -*-
from keras.layers import Input, Dense
from keras.models import Model
from keras.models import Sequential  
from keras.layers.core import Dense, Dropout, Activation  
from keras.optimizers import SGD  
from keras.utils import np_utils
from keras.layers import Convolution1D, MaxPooling1D,Flatten
import numpy as np
from gensim.models import word2vec 

# set parameters:
# max_features = 5000
# maxlen = 20
# batch_size = 32
# embedding_dims = 50
nb_filter = 50
filter_length = 5
hidden_dims = 128
nb_epoch = 2
v_dim = 200
seq_length = 20
#...word to vector model
vecmodel = word2vec.Word2Vec.load("../trainvec200sg.model")

#prepare data and label from ...
data = []
labels = []
with open('../dev.txt') as file:
    for line in file.readlines():
        words = line.split()
        label = int(words[0])
        labels.append(label)
        words = words[1:]
        vec=np.zeros(v_dim)
        count = 0
        for word in words:
            if count < seq_length:
                try:
                    vec = vecmodel[word]
                    
                    # print vecmodel[word]
                    count += 1
                except KeyError:
                    continue
                data.append(vec)
            else:
                break
        if count < seq_length:
            zeros = np.zeros(v_dim)
            for i in range(seq_length-count):
                data.append(zeros)

#change the shape of input
nb_samples = len(labels)
print nb_samples
labels = np.array(labels)
labels.reshape(nb_samples,1)
labels = np_utils.to_categorical(labels,5)
# print labels
data = np.array(data)
data = data.reshape(nb_samples,seq_length,v_dim)
#尝试量化？？
# data = (data*100).round()
# print data
#随机数据
# nb_samples=1000
# data=np.random.random((nb_samples,v_dim))
# labels=np.random.randint(5,size=(nb_samples,1))
# labels = np_utils.to_categorical(labels,5)

## model CON1D
model = Sequential()
model.add(Convolution1D(nb_filter=nb_filter,
                        filter_length=filter_length,
                        border_mode='valid',
                        activation='relu',
                        subsample_length=1,init = 'uniform',input_dim = v_dim,input_length = seq_length))
# we use max pooling:
model.add(MaxPooling1D(pool_length=2))
# We flatten the output of the conv layer,# so that we can add a vanilla dense layer:
model.add(Flatten())

# We add a vanilla hidden layer:
model.add(Dense(hidden_dims))
model.add(Dropout(0.2))
model.add(Activation('relu'))

model.add(Dense(5))
model.add(Activation('softmax'))
sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True) 
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])

# model.load_weights('testadammlpv200t_relu.d5')
model.fit(data,labels,batch_size=35,nb_epoch=10,shuffle=True,\
	verbose=2,show_accuracy=True,validation_split=0.1)
# model.save_weights('testadammlpv200t_relu.d5', overwrite=True)
# tmp ="The most hopelessly monotonous film of the year , noteworthy only for the gimmick of being filmed as a single unbroken 87-minute take ."
# tmp = tmp.split()
# # print tmp
# xt = get_word_vectors(tmp).reshape(1,v_dim)
# # print xt
# err,acc =model.evaluate(data, labels, batch_size=100, show_accuracy=True,verbose=1)
# print err, acc
# np.set_printoptions(threshold='nan')
# yt = model.predict(data)
# print yt
# yc = model.predict_classes(data)
# print yc
# tdata = []
# tlabels = []
# with open('dev.txt') as file:
#     for line in file.readlines():
#         words = line.split()
#         label = int(words[0])
#         tlabels.append(label)
#         words = words[1:]
#         vec = get_word_vectors(words)
#         tdata.append(vec)


# tnb_samples = len(tlabels)
# print tnb_samples
# tlabels = np.array(tlabels)
# tlabels.reshape(tnb_samples,1)
# tlabels = np_utils.to_categorical(tlabels,5)
# # print labels
# tdata = np.array(tdata)
# tdata.reshape(tnb_samples,v_dim)
# # s_w = np.ones(tnb_samples)
# err,acc =model.evaluate(tdata, tlabels, batch_size=100, show_accuracy=True,verbose=1)
# # err, acc = model.test_on_batch(tdata, tlabels, sample_weight=None)
# ### ValueError: Input arrays should have the same number of samples as target arrays. Found 1101 input samples and 8544 target samples.
# print err, acc