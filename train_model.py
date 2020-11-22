import pandas as pd 
import numpy as np 
import tensorflow as tf 
from tensorflow import keras 
from keras.utils.np_utils import to_categorical 
from keras.layers import Dense, Flatten, Input, Conv2D
from keras.models import Model  

# data

path = "train.csv"
data = pd.read_csv(path)   
Y_data = data['label']
X = data.drop(['label'], axis='columns')
Y_shape = np.shape(Y_data)[0] 
Y_train = to_categorical(Y_data)        
X_train = np.array(X) / 255  

for x in np.nditer(X_train, op_flags=['readwrite']):    # нормализация значений для приложения -> в "рисовалке" используются значения 0, 0.5, 1
    if x[...] > 0.7:
        x[...] = 1
    elif x[...] < 0.3:
        x[...] = 0
    else:
        x[...] = 0.5 

X_train = np.reshape(X_train, (-1, 28, 28, 1))
 
# model 

inp = Input(shape=(28,28,1))
x = Flatten()(inp)
x = Dense(80, activation="relu")(x)
x = Dense(80, activation="relu")(x)
out = Dense(10, activation="softmax")(x)

model = Model(inputs=inp, outputs=out) 

model.compile(optimizer='adam',
              loss='binary_crossentropy',    
              metrics=['accuracy'])
model.fit(X_train, Y_train, epochs=7)

path = "model/my_model.h5"
model.save(path)  