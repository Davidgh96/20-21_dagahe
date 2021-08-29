# 20-21_dagahe
# Modulo de detección de ataques por presentación en sistemas biométricos faciales.

Trabajo Fin de Master

Master en Ciberseguridad y Privacidad

Curso 2020 / 2021

Universidad Rey Juan Carlos

Alumno: **David Garcia Herrero**

Tutora : **Cristina Conde Vilda**


# Resumen del proyecto

En un mundo donde el uso de las biometrías no para de expandirse, muchas entidades han apostado por utilizarlas en sus controles de acceso para proteger sus recursos, debido a su gran potencial, siendo los sistemas faciales uno de los mas utilizados, por su gran rendimiento a un coste no muy elevado. El problema es que a la vez que se están expandiendo estas tecnologías,  el interés de los hackers y cibercriminales aumenta, a la vez que los ataques e intentos de ruptura. <br>

Dentro de estos ataques a sistemas biométricos faciales, los sensores que recogen y analizan esos datos, son un objetivo muy codiciado por los hackers. Conseguir acceso a un recurso valioso al que no tenemos acceso o impedir que un sujeto con permisos no pueda acceder a él, es uno de los objetivos principales.  Para ello, han creado un tipo de ataque, conocido por Ataques por presentación, que simulan las biometrías reales de una persona para acceder a un recurso protegido. <br>

Con el objetivo de  evitar estos ataques y  como parte principal de este proyecto final, hemos desarrollado un sistema que es capaz de recibir una imagen e identificar, con una precisión muy alta, si se trata de una imagen real o de un ataque por presentación. <br>

En los siguientes puntos, explicaremos la manera de configurar este modulo con varias opciones disponibles, sugiriendo la mas sencilla para el usuario y comentando paso a paso como realizar las predicciones y extraer la maxima efectividad de este proyecto.

# Entorno de uso

## Google Colab (Recomendado)

Es la manera mas sencilla y recomendada, debido a su mayor eficiencia y sencillez. Para ello, abrimos Google Colab en una nueva hoja y usaremos el fichero **ModuloCompletoGoogleColab.py**. Para mayor comodidad, este fichero se añadira en tres bloques diferentes a la hoja de Google Colab, para poder ejecutarse de manera independiente (el fichero tiene dos separaciones con ####### para distinguir las tres secciones). Tendremos un primer bloque de entrenamiento, un segundo de carga del modelo y la funcion de prediccion, y una tercera para realizar las predicciones.

## Instalar Tensorflow en local

Es necesario realizar la instalcion de Tensorflow y Keras, dependencias que utiliza el proyecto. En este enlace nos ayuda a relizar todas las instalaciones con pip:   https://www.tensorflow.org/install/pip?hl=es-419 <br>
Para utilizar el modulo de esta manera, utilizaremos los ficheros **createModelVGG19.py** **fitModel.py** y **predictModel.py** , en ese orden.

# Configuracion del modulo

## Utilizando el modelo ya entrenado por el alumno (Recomendado)

En Google Colab, debemos subir los ficheros **modeloFirstVersion.h5** **pesosFirstVersion.h5** y las imagenes dentro de la carpeta **imagenes_prueba/** a nuestra cuenta de Drive , para poder acceso a ellas.
A continuacion debemos setear las siguientes variables dentro de **ModuloCompletoGoogleColab.py** en Google Colab.

***modelo = 'path_al_fichero/modeloFirstVersion.h5'***   <br>
***pesos_modelo = 'path_al_fichero/pesosFirstVersion.h5'***

Al tener ya los dos ficheros con el modelo y sus pesos, no tenemos que realizar entrenamiento y el tiempo de ejecucion es minimo. Por ello, solo debemos ejecutar los dos ultimos bloques comentados anteriormente, dejando el primero (el del entrenamiento) sin ejecutar. 

## Entrenando uno mismo el modelo

El tiempo aumenta sustancialmente y ademas por proteccion de datos, no podemos subir la base de datos con las imaganes utilizadas para el proyecto ( excepto las subidas en la carpeta ***imaganes_pruebas***, autorizadas previamente). Si se dipone de una base de datos propia con imaganes correctas y ataques por presentacion, se configura de la siguiente manera.  
 
 ![image](https://user-images.githubusercontent.com/25246266/131260889-24bc7134-6b7d-48c7-9307-1d25d393f365.png)

Creamos ese arbol de carpetas con las imaganes clasificadas. Un 80% de las imagenes deben ir a la carpeta Entrenamiento y el otro 20% a la Validacion. A parte, dejaremos alguna imagen aparte para añadir a la carpeta Pruebas (o usad las proporcionadas en este proyecto). Todo este arbol de carpetas estara subido a Google Drive, para realizar el entrenamiento en Google Colab.
Una vez esta subido todo, configuramos de nuevo las siguientes rutas:

***path_entrenamiento = 'path_a_la_carpeta/Entrenamiento'*** <br>
***path_validacion = 'path_a_la_carpeta/Validacion'***

***sequentialModel.save('path_destino/modelo.h5')*** <br>
***sequentialModel.save_weights('path_destino/pesos.h5')***

***modelo = 'path_destino/modelo.h5'*** <br>
***pesos_modelo = 'path_destino/pesos.h5'***

De esta manera, generaremos de cero los ficheros con el modelo entrenado y sus pesos, pero el tiempo es mayor. Para ello, ahora si debemos ejecutar los tres bloques en Google Colab y no necesitamos usar los ficheros **modeloFirstVersion.h5** **pesosFirstVersion.h5** proporcionados por el alumno.

# Uso del modulo

Una vez tenemos todo entrenado y tenemos los ficheros con el modelo y los pesos, podemos realizar las predicciones, utilizando el ultimo bloque del codigo:

***predecirImagen('path_a_carpeta/Pruebas/NOMBRE_IMAGEN.JPG')***

# Bibligrafia

***Google Colab:*** https://colab.research.google.com/ <br>
***Tensorflow :*** https://www.tensorflow.org/api_docs/python/tf <br>
***Keras Applications :*** https://keras.io/api/applications/  <br>
***StackOverflow :*** https://es.stackoverflow.com/ <br>
