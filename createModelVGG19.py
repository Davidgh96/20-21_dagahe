## Librerias relacionadas con las redes neuronales y su gestion, ademas de algunas para la gestion de imagenes y ficheros.
from tensorflow.python.keras.applications import vgg19
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