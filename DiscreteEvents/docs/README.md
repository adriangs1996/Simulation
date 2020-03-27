# Proyecto de Eventos Discretos.

*Autor: [Adrian Gonzalez Sanchez](https://github.com/adriangs1996)*

*Grupo: C-412*

**Orden del Problema**:
Un canal marı́timo consiste en una o más exclusas colocadas en diques consecutivos de manera que la combinación de estas
permite el ascenso o descenso de los barcos, permitiendo el acceso del barco al dique siguiente. Estos canales son usados para la navegación a través de aguas turbulentas o para atravesar terrenos terrestres. Se desea conocer el tiempo de espera de los barcos para el uso de un canal con 5 diques para su funcionamiento. La operación de un canal puede ser dividido en dos ciclos muy similares que llamaremos ciclo de subida y ciclo de bajada. El ciclo de subida comienza con la compuerta del nivel superior cerrada y la compuerta del nivel inferior abierta. Los barcos esperando en el nivel inferior entran en el dique. Cuando los barcos se acomodan dentro del dique las puertas del nivel inferior se cierran y las puertas del nivel superior se abren y el agua del nivel superior inunda el dique, haciendo la función de un elevador marı́timo. Luego los barcos pasan al nivel superior, dejando el dique vacı́o. El ciclo de bajada consiste en el funcionamiento opuesto del ciclo descrito.

Ambos ciclos tienen las mismas 3 fases para su cumplimento, que se pueden llamar como fase de entrada, fase de transporte y fase de salida respectivamente. La fase de entrada consiste en abrir las puertas del nivel inferior y dejar entrar a
los barcos esperando hasta que estos se acomodan dentro del dique, la duración de este proceso depende del tiempo de apertura de las compuertas que distribuye de manera exponencial con λ = 4 minutos y el tiempo que se demora cada barco en entrar al dique, que distribuye de manera exponencial con λ = 2 minutos independientemente del tamaño de cada barco. Los barcos a entrar en el dique son tomados de manera secuencial de la cola de arribo de los barcos y en caso de que algún barco no quepa en el dique, el siguiente en la cola toma su lugar, en caso de que ningún barco quepa en el dique, la fase comienza sin llenar la capacidad del dique. 

La fase de transporte incluye cerrar la compuerta del nivel inferior, la apertura del nivel superior y el llenado del dique, esta fase tiene un tiempo de duración que distribuye de manera exponencial con λ = 7 minutos. La fase de salida se compone por la salida de los barcos del dique ası́ como el cerrar la puerta del nivel superior, esta fase tarda un tiempo que distribuye de manera exponencial con λ = 1,5 minutos por cada barco en el dique. El número total de barcos que pueden ser acomodados en un dique depende del tamaño fı́sico de los barcos. Estos tienen 3 tamaños distintos: pequeño, mediano y grande y el tamaño de cada uno de estos corresponde a la mitad del anterior. Cada dique puede albergar 2 filas con espacio para el equivalente a 3 barcos medianos (1 grande y dos pequeños). 

El tiempo de arribo de los barcos distribuye de acuerdo con la función Normal y dependen del tamaño del barco ası́ como de la hora del dı́a (el canal funciona de 8 am a 8 pm), los parámetros de la función se resumen en la tabla siguiente.

**Tamaño**  |  **8:00am - 11:00am**    | **11:00am - 5:00pm**    |  **5:00pm - 8:00pm**

Pequeño       ![equation](http://www.sciweavers.org/upload/Tex2Img_1585279398/render.png) | ![equation](http://www.sciweavers.org/upload/Tex2Img_1585279281/render.png) | ![equation](http://www.sciweavers.org/upload/Tex2Img_1585279309/render.png)

Mediano      ![equation](http://www.sciweavers.org/upload/Tex2Img_1585279454/render.png) | ![equation](http://www.sciweavers.org/upload/Tex2Img_1585279498/render.png) | ![equation](http://www.sciweavers.org/upload/Tex2Img_1585279537/render.png)

Grande        ![equation](http://www.sciweavers.org/upload/Tex2Img_1585279619/render.png) | ![equation](http://www.sciweavers.org/upload/Tex2Img_1585279645/render.png) | ![equation](http://www.sciweavers.org/upload/Tex2Img_1585279677/render.png)


## Ideas e interpretación

Para atacar este problema, primero hubo que llegar a un grupo de restricciones o reglas sobre el problema, que ayuden a modelar mejor la situación que se nos plantea. Se define entonces las siguientes invariantes:

***
* Un canal consiste en una combinación de diques.

* Cada dique tiene un modo (subida o bajada).

* Cada dique ejecuta una fase cuando tiene barcos disponibles y el dique no tiene ocupación, funcionando como un elevador (puede ser ascenso o descenso).

* Cada fase que ejecuta un dique hace que el dique ascienda o descienda (depende de su modo) y luego regresa a su posición.

* No necesariamente la fase de subida dura lo mismo que la de bajada (las distribuciones no necesariamente son iguales).

* En cada fase, se tiene en cuenta el tiempo que demora abrir o cerrar las compuertas.

* El canal funciona de 8:00 AM a 8:00 PM, o sea 12 horas o 720 minutos.

* Se asume que los barcos pueden llegar antes de la hora programada de funcionamiento del canal. Esta restricción permite acercarse un poco al funcionamiento real de los canales, ya que pueden existir eventos que hagan que un barco tenga que cambiar su ruta, o por calendario, la hora de llegada al canal no coincide con las 12 h de funcionamiento del mismo exactamente (ejemplo un crucero, que puede que llegue a las 7am al canal de Panamá y tenga que esperar 1h para poder cruzar). Generalmente estos casos son barcos grandes, por tanto se debe tener en cuenta a la hora de proveer de una función para calcular los arribos antes de tiempo. Estos eventos deben ser suficientes como para tenerlos en cuenta en el tiempo calculado, pero no tantos como para afectar sustancialmente este resultado.

* Los barcos entran y salen de los diques de manera secuencial.

Con estas reglas podemos definir un modelo de N-servidores en serie, donde cada dique es un servidor que atiende a los clientes que permanecen en su cola de epera (barcos) a medida que se desocupa (termina de procesar otros barcos o actualmente no procesa a nadie). Con esto en mente, nuestro objetivo es detectar el tiempo esperado de permanencia en cola de cada barco.

## Modelo

![](canal.png)

La figura representa una canal con dos diques, uno de subida y otro de bajada. Para subir, el dique 1 tiene que abrir sus compuertas superiores, cerrar las inferiores, cerrar las superiores, llenarse de agua, abrir las inferiores, trasladar los barcos a la cola del dique 2, cerrar las compuertas inferiores y vaciarse de agua para volver a su estado original. El dique 2 tiene que hacer el proceso inverso para mover los barcos fuera del canal.

Además, se puede notar que el dique 1 está procesando 2 barcos mientras que el dique 2 procesa 1; y ambos tienen barcos esperando en sus respectivas colas.

Entonces, se definen las siguientes variables para lograr este funcionamiento del canal:

* **Variables de tiempo**:

  1. ![equation](http://www.sciweavers.org/upload/Tex2Img_1585336689/render.png): Tiempo total.
  
  2. ![equation](http://www.sciweavers.org/upload/Tex2Img_1585336596/render.png): El tiempo en el cual se desocupa el dique i.
  
  3. ![equation](http://www.sciweavers.org/upload/Tex2Img_1585336727/render.png): Tiempo que demora el dique i en procesar los barcos que toma de la cola.
  
  4. ![equation](http://www.sciweavers.org/upload/Tex2Img_1585336936/render.png): Tiempo que ha usado el barco i en su trayecto por los diques.
  
  5. ![equation](http://www.sciweavers.org/upload/Tex2Img_1585337198/render.png): Tiempo de arribo del barco i.
  
* **Variables de estado del sistema**
  
  1. ![equation](http://www.sciweavers.org/upload/Tex2Img_1585337290/render.png): Cantidad de barcos en la cola de espera del dique i.
  
  2. ![equation](http://www.sciweavers.org/upload/Tex2Img_1585337370/render.png): Cantidad de barcos en el sistema (que no han pasado a la cola de ningun dique) en el tiempo t.
  
  3. ![equation](http://www.sciweavers.org/upload/Tex2Img_1585346045/render.png): Cantidad de barcos que toma el dique i de su cola de espera
  
* **Variable de conteo**

  1. ![equation](http://www.sciweavers.org/upload/Tex2Img_1585337791/render.png): Cantidad de barcos que han abandonado el sistema (que ya han transitado por todos los diques).
  
Al definir estas variables, queda claro que los eventos de nuestra simulación son: las llegadas de los barcos al sistema y el tiempo de finalización de cada dique, o sea, la lista de eventos es:


![equation](http://www.sciweavers.org/upload/Tex2Img_1585338895/render.png)

donde ![equation](http://www.sciweavers.org/upload/Tex2Img_1585338809/render.png) es el tiempo de arribo del barco i y ![equation](http://www.sciweavers.org/upload/Tex2Img_1585338948/render.png) es el tiempo en que el dique j termina de procesar a los barcos que posee actualmente. Si el dique j no procesa barcos actualmente, entonces ![equation](http://www.sciweavers.org/upload/Tex2Img_1585340274/render.png).

Las variables que nos interesa capturar en la salida son los ![equation](http://www.sciweavers.org/upload/Tex2Img_1585340377/render.png) para cada barco i, ya que a partir de estas, podemos calcular el tiempo de espera en cola de un barco a través de la siguiente ecuación:

![equation](http://www.sciweavers.org/upload/Tex2Img_1585340528/render.png)

Entonces, para comenzar la simulación, inicializamos las variables:

![equation](http://www.sciweavers.org/upload/Tex2Img_1585341002/render.png)

***MIENTRAS ![equation](http://www.sciweavers.org/upload/Tex2Img_1585341216/render.png):***
    
   ![equation](http://www.sciweavers.org/upload/Tex2Img_1585345621/render.png)
   
   Si ![equation](http://www.sciweavers.org/upload/Tex2Img_1585345693/render.png)
   
   Determinar los diques que pueden funcionar en el tiempo actual:
   
   ![equation](http://www.sciweavers.org/upload/Tex2Img_1585341871/render.png)
   
   Analizando el modelo, se puede apreciar que un dique solamente puede atender barcos pendientes en su cola, pero para que estos barcos lleguen a la cola, es necesario que el dique i-1 haya terminado en el tiempo t de procesar sus barcos, por tanto, una vez que el dique i va a procesar barcos, podemos actualizar su tiempo de ocupación de la siguiente manera:
   
   ![equation](http://www.sciweavers.org/upload/Tex2Img_1585342619/render.png)
   
   ![equation](http://www.sciweavers.org/upload/Tex2Img_1585342508/render.png)
   
   si el dique i es el es el ultimo en la cadena, entonces se calcula el tiempo de espera para cada barco j que proceso este dique:
   
   ![equation](http://www.sciweavers.org/upload/Tex2Img_1585343032/render.png)
   
   y se actualiza la cantidad de barcos que abandonan el sistema:
   
   ![equation](http://www.sciweavers.org/upload/Tex2Img_1585345139/render.png)
   
   Actualizamos ![equation](http://www.sciweavers.org/upload/Tex2Img_1585346482/render.png) para cada dique i que se procese.
   
   Actualizamos ![equation](http://www.sciweavers.org/upload/Tex2Img_1585346275/render.png) para cada dique i que se procese y que no sea el ultimo dique.
   
   actualizamos el tiempo t, notar que solo pasa un tiempo igual al menor tiempo que le toma a un dique procesar sus barcos si todos los diques procesan, de lo contrario tiempo aumenta en 1:
   
   ![equation](http://www.sciweavers.org/upload/Tex2Img_1585343394/render.png)
 
 **REPETIR**
   
**Al finalizar:**
  Devolver ![equation](http://www.sciweavers.org/upload/Tex2Img_1585345342/render.png)
  
  
## Implementación

La implementación del modelo sugerido en la sección anterior se basa en un conjunto de clases de support, que se ensamblan en la clase SeaChannel para formar el pipeline completo de la simulación.

*Ship*: La clase Ship es la encargada de manejar el arribo de barcos al sistema, o sea, posee una función "arrive" que devuelve un valor ![equation](http://www.sciweavers.org/upload/Tex2Img_1585347212/render.png). Esta clase es un contenedor y no debe ser instanciada directamente, sino a partir de sus descendientes *LargeShip*, *MediumShip* y *SmallShip*, que no solo se ocupan de pasar los argumentos de la normal, sino que inicializan el valor de size, variable que es necesaria a la hora de decidir si un barco entra en un dique.

*Hatch*: Esta clase se ocupa de representar un dique, en ella se simula todo el funcionamiento del dique (cerrar o abrir las compuertas, vaciar o llenar el dique, dejar entrar o sacar barcos del dique). Las distintas funciones de esta clase devuelven valores para el tiempo ![equation](http://www.sciweavers.org/upload/Tex2Img_1585347533/render.png) generados a partir de la simulación de los procesos que ocurren en el dique (tomando exponenciales con los argumentos ofrecidos en la descripción del problema), y tambien se ocupa de actualizar valores como ![equation](http://www.sciweavers.org/upload/Tex2Img_1585347667/render.png) para cada barco i que transita por el dique. Esta clase tampoco se debe instanciar directamente, de eso se ocupa la clase general SeaChannel.

*HatchSystem*: Ofrece funciones de ayuda para manejar un conjunto de diques, ya sea poder acceder a ellos a traves de subindices, preguntar cuantos hay, y realizar una fase completa en alguno de los diques del sistema.

*SeaChannel*: Es la clase principal que se ocupa de enlazar todas las estructuras del sistema. Posee una rutina *get_ships* que simula la llegada de los barcos al sistema. La implementación de esta función en SeaChannel genera un barco de un tipo aleatorio (grande, mediano, o chico) y luego decide el tiempo en que va a arribar dicho barco. Esta forma de generar los barcos probó no ser muy realista, y luego de un poco de investigación, se creó la clase *MultiShipsSeaChannel* que hereda directo de *SeaChannel* y reimplementa la función *get_ships* para generar entonces barcos chicos, medianos y grandes independientes, y ver, para cada tipo, los tiempos de arribo.

SeaChannel posee una rutina *run_day*, que simula una jornada del canal, utilizando el modelo de la sección anterior.

Para probar la implementación, se ofrece el módulo *driver.py*, que es el encargado de parametrizar la simulación y reportar los resultads. La forma de correr el simulador en su manera mas sencilla es:

```bash
$ ./driver.py
```
  
Para ver una lista de los argumentos que recibe *driver.py* y una breve descripción de los mismos:

```bash
$ ./driver.py --help
```

Los mejores resultados se obtuvieron corriendo el algoritmo de la siguiente manera:

```bash
$ ./driver -i -c 1000 -m --hatches 5 -d U D U U U
```
Al correr con -c, *driver* reporta el resultado de cada simulación y de pasarse el argumento -m se calcula el promedio del valor obtenido en cada simulación. 

El argumento de mayor importancia es -i, el cual cambia entre las funciones que generan los arribos de los barcos, por tanto se recomienda siempre pasar este argumento.

## Consideraciones

Al simular varias veces la situación planteada, se pudo obtener una idea de los problemas a los que nos podemos enfrentar al construir un canal marı́timo. Por ejemplo, con 5 diques, asumiendo que el tiempo de bajada y subida de los diques se comporta con la misma distribución y generando los barcos de distintas dimensiones de manera independiente, se obtiene un tiempo de espera promedio que oscila entre los 28 minutos, este tiempo incluye el tiempo que un barco espera porque se abran las compuertas para pasar, o que un barco espera por otro para poder entrar al dique (recordar que estamos asumiendo que los barcos entran a los diques de uno en uno y salen de la misma forma). 28 minutos puede no parecer mucho, pero este tiempo crece proporcionalmente a la cantidad de diques, reportando valores de 38 minutos para 6 diques, 48 para 7 y 54 para 8, por ejemplo. Esto es bastante intuitivo, producto del allotment de los diques el cual puede significar un cuello de botella en horarios muy concurridos. Las formas para reducir este tiempo de espera puede ser:

  * Garantizar menos arribos de barcos al sistema (al correr sin el argumento -i, el simulador reporta tiempos de espera alrededor de los 12 minutos).
  
  * Reducir la cantidad de diques del sistema (Por ejemplo con 1 dique, los tiempos de espera rondan los 5 minutos, aproximadamente el tiempo que le toma a cada barco entrar al dique y este realizar una fase entera). En la realidad, esta opción puede no ser viable, ya que generalmente la cantidad de diques responden a la necesidad de llevar barcos a zonas elevadas o cruzar largos tramos de aguas turbulentas.
  
  * Agilizar la apertura de compuertas. Variar los argumentos de las exponenciales que rigen el comportamiento de las compuertas retornó resultados favorables, auqnue los cambios no fueron tan perceptibles como la cantidad de diques o la cantidad de arribo de barcos (en los mejores casos, se obtiene de 4 a 5 minutos de mejora, pero implica considerar valores muy chicos para los lambdas de las exponenciales, algo que en la realidad puede no ser factible).
  
Si nos abstraemos un poco y pensamos en los barcos como procesos y en el canal como un scheduler, se puede transformar este problema en un problema de minimizar el turn-around time de procesos y sabemos, por ejemplo de algoritmos como STCF que dado las restricciones de nuestro problema, ofrecen buenos resultados, de hecho durante la simulación, se intento ordenar la cola de espera de cada dique por dimensión de los barcos, tratando de atender en cada momento a la mayor cantidad de barcos posibles (estas colas por supuesto solo contienen barcos que hayan arribado al sistema en el tiempo t); lo que arrojó algunas mejoras en el tiempo de espera en cola de cada barco. Esta implementación no se incluye en el proyecto, pues a lo mejor se sale del objetivo y es muy sencillo de incorporar al modelo, pero a la hora de reportar aspectos que influyen en el funcionamiento del canal, podemos decir:

 1. Cantidad de arribos de barcos en los distintos horarios (en particular las colisiones de tiempo en los arribos, o sea muchos barcos que llegan en intervalos muy chicos de tiempo).
 
 2. Cantidad de diques en el canal.
 
 3. Orden en que se toman los barcos a la hora dejarlos entrar a un dique.
