## Importacion de librerias para el procesamiento y lectura de imagenes.
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model

## Tamaño de las imagenes a tratar.
longitud = 224
altura = 224

## Rutas del modelo y sus pesos previamente guardados.
modelo = './modelo/modelo.h5'
pesos_modelo = './modelo/pesos.h5'

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

## Llamada a la funcion de prediccion, pasando como parametro la ruta de la imagen a probar.
predecirImagen('./Pruebas/tablet_163.JPG')