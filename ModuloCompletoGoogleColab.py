## Librerias relacionadas con las redes neuronales y su gestion, ademas de algunas para la gestion de imagenes y ficheros.
import sys
import os
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.applications import vgg19
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras import optimizers
from tensorflow.python.keras.models import Sequential

## Metodo para crear una red neuronal VGG19 modificada, con una capa oculta extra con activacion y una final para la eleccion de resultado.
def createVGG19Model():

    ## Iniciacion de la red VGG19 y de una red sequencial.
    vgg19Model = vgg19.VGG19()
    sequentialModel = Sequential()

    ## Añadidas todas las capas de la red neuronal VGG19 a la red sequencial para poder trabajar con ella.
    for capa in vgg19Model.layers:
        sequentialModel.add(capa)

    ## Extraccion de la ultima capa del modelo, la capa predictiva.
    sequentialModel.pop()

    ## Al tratarse de un modelo prentrenado, evitamos que posteriormente se vuelva a entrenar, ahorrandonos mucho tiempo.
    for capa in sequentialModel.layers:
        capa.trainable = False

    ## Finalmente añadimos una capa de decision con dos neuronas y una funcion de activacion softmax.
    sequentialModel.add(Dense(2,activation= 'softmax'))      
        
    ## Devolvemos el modelo personalizado.
    return sequentialModel

## Limpiamos las sesiones anteriores
K.clear_session()

## Rutas donde tenemos tanto la carpeta de entrenamiento como de validacion con las imagenes.
path_entrenamiento = './drive/MyDrive/tfm/Entrenamiento'
path_validacion = './drive/MyDrive/tfm/Validacion'

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
sequentialModel.save('./modelo/modeloFirstVersion.h5')
sequentialModel.save_weights('./modelo/pesosFirstVersion.h5')

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

####################################################################################################################################

## Importacion de librerias para el procesamiento y lectura de imagenes.
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model

## Tamaño de las imagenes a tratar.
longitud = 224
altura = 224

## Rutas del modelo y sus pesos previamente guardados.
modelo = './drive/MyDrive/tfm/modulo/modeloFirstVersion.h5'
pesos_modelo = './drive/MyDrive/tfm/modulo/pesosFirstVersion.h5'

## Carga del modelo y sus pesos.
sequentialModel = load_model(modelo)
sequentialModel.load_weights(pesos_modelo)

## Funcion para predecir si una imagen es correcta o es un ataque por presentacion
def predecirImagen(file):

  # Carga de la imagen con sus dimensiones, la convierte a array y la expande, para poder realizar la prediccion.
  imagen = load_img(
      file,
      target_size=(longitud, altura))
  imagenArray = img_to_array(imagen)
  valorFinal = np.expand_dims(imagenArray, axis=0)

  ## Prediccionde la imagen
  array = sequentialModel.predict(valorFinal)

  ##Obtencion del resultado y escritura por pantalla si es un ataque por presentacion o no.
  resultado = array[0]
  print(resultado)
  correcto = np.argmax(resultado)
  if correcto == 0:
    print("Prediccion: ATAQUE")
  elif correcto == 1:
    print("Prediccion: REAL")

  return correcto

####################################################################################################################################

## Llamada a la funcion de prediccion, pasando como parametro la ruta de la imagen a probar.
predecirImagen('./drive/MyDrive/tfm/Pruebas/tablet_163.JPG')
