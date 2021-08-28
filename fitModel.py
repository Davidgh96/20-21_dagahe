import sys
import os
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras import optimizers
from tensorflow.python.keras.models import Sequential
from createVGG19 import createVGG19Model

## Limpiamos las sesiones anteriores
K.clear_session()

## Rutas donde tenemos tanto la carpeta de entrenamiento como de validacion con las imagenes.
path_entrenamiento = './entrenamiento'
path_validacion = './validacion'

## Tamaño de imagen utilizado en el modelo.
longitud = 244
altura = 244

## Valor de aprendizaje del modelo, suele ser menor con muestras de imagenes mas grandes.
lr = 0.05

## Tamaño de cada paquete
batch_size = 51


## Generador de imagenes para nuestro entrenamiento. Incluye una serie de tranformaciones para 
## tener mas variedad de imagenes y que el modelo aprenda mejor ( Rescalados, rotaciones, zooms, etc...). 
generador_imagenes_entrenamiento = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.3,
    zoom_range=0.3,
    rotation_range = 60,
    width_shift_range = 0.3,
    height_shift_range = 0.25,
    horizontal_flip=True)

## Generador de imagenes para nuestra validacion. Solo es necesario el rescalado en este caso.
generador_imagenes_validacion = ImageDataGenerator(
    rescale=1. / 255)

## Obtencion de las imagenes modificadas para el entrenamiento.
entrenamiento_generador = generador_imagenes_entrenamiento.flow_from_directory(
    path_entrenamiento,
    target_size=(altura, longitud),
    class_mode='categorical',
    batch_size = batch_size)

## Obtencion de las imagenes para la validacion.
validacion_generador = generador_imagenes_validacion.flow_from_directory(
    path_validacion,
    target_size=(altura, longitud),
    class_mode='categorical',
    batch_size = batch_size)

## Creacion del modelo con la funcion de creacion creada anteriormente.
sequentialModel = createVGG19Model()

## Compilacion del modelo con el optimizador Adam.
sequentialModel.compile(
    loss='categorical_crossentropy',
    optimizer= optimizers.adam_v2.Adam(learning_rate= lr),
    metrics=['accuracy'])

## Numero de etapas que entrenara el modelo.
epochs = 51

## Numero de pasos por etapa
steps_per_epoch = int(entrenamiento_generador.n / batch_size)

## Numero de pasos por etapa en la validacion
validation_steps = int(validacion_generador.n / batch_size)

## Entrenamiento del modelo, con los generadores tanto de entrenamiento como de 
## validacion creados anteriormente y con los datos de etapas y pasos definidos.
history = sequentialModel.fit(
    entrenamiento_generador,
    steps_per_epoch= steps_per_epoch,
    epochs=epochs,
    validation_data=validacion_generador, 
    validation_steps = validation_steps)

## Carpeta donde almacenaremos el modelo y sus pesos generados.
target_directory = './modelo/'

## Crea la carpeta si no existe.
if not os.path.exists(target_directory):
  os.mkdir(target_directory)

## Guarda el modelo y los pesos ya entrenados.
sequentialModel.save('./modelo/modelo.h5')
sequentialModel.save_weights('./modelo/pesos.h5')

## Importacion de la libreria para las graficas.
import matplotlib.pyplot as plt

## Extraccion de los valores de aciertos y fallos del entrenamiento.
acc      = history.history['accuracy']
val_acc  = history.history['val_accuracy']
loss     = history.history['loss']
val_loss = history.history['val_loss']

#Grafica de los aciertos
epochs = range(1,len(acc)+1,1)
plt.plot(epochs,acc,'r--',label='Training accuracy')
plt.plot(epochs,val_acc,'b',label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.ylabel('accuracy')
plt.xlabel('epochs')
plt.legend()
plt.figure()

#Grafica de los fallos
epochs = range(1,len(loss)+1,1)
plt.plot(epochs,loss,'r--', label='Training loss')
plt.plot(epochs,val_loss ,'b',label='Validation loss')
plt.title('Training and validation loss')
plt.ylabel('loss')
plt.xlabel('epochs')
plt.legend()
plt.figure()