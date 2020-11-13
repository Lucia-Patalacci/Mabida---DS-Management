import os
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import matplotlib.pyplot as plt
import matplotlib as mpl
import re
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense
from keras.callbacks import EarlyStopping
early_stop = EarlyStopping(monitor='val_loss', patience=5, verbose=1)

path='C:\\Alessandro\\Python\\Master - Gigli\\lab_ikea'
npixel=187500
filelist=[x for x in os.listdir(path) if '.JPG' in x]
dataset=np.array([[]], "float32")
target=np.array([[]], "float32")
i=-1
for image in filelist:
 i+=1   
 img = load_img(image)  # this is a PIL image
 x = img_to_array(img)  # this is a Numpy array with shape (250, 250, 3) 187500 valori
 price=image[image.find('Price'):image.find('Rating')]
 price=float(re.sub('[^0-9.]', "", price))
 dataset = np.append(dataset, x.flatten())
 target = np.append(target, price)

 #plt.figure()
 #plt.imshow(x/255.)#, interpolation='nearest', cmap=mpl.cm.Blues)
 #plt.axis('off')
#plt.show()
dataset= np.reshape(dataset, (len(target),npixel) )
target = np.reshape(target, (len(target),1)  )
target = (target - np.min(target))/np.ptp(target)
print('dataset: ',dataset)
print('dataset shape: ',dataset.shape)
print('target: ',target)
print('target shape: ',target.shape)
 
model = Sequential()
model.add(Dense(300, input_dim=npixel, activation='sigmoid'))
model.add(Dense(300,  activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))   #activation='sigmoid'))
model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['accuracy'])
print(model.summary())
hist=model.fit(dataset,
               target,
               batch_size=32, 
               epochs=100,
               verbose=1,
               validation_data=(dataset, target))#,
               #callbacks=[early_stop])

print('model.predict(training_data).round()')
print(model.predict(dataset).round())

loss, accuracy = model.evaluate(dataset, target, verbose=0)
print('Test Loss:', loss)
print('Test Accuracy:', accuracy)

# Visulize how the loss and accuracy change over epochs
plt.figure()
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.legend(['Training', 'Validation'])
plt.figure()
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.plot(hist.history['acc'])
plt.plot(hist.history['val_acc'])
plt.legend(['Training', 'Validation'], loc='lower right')
plt.show()























