# Modelado y Control de Velocidad de un Servo Simulado (1ªParte)

<h2>Introducción</h2>
Se trata de un simulador desarrollado por la UNED para sus laboratorios virtuales los cuales, nos permiten descargar y ejecutar localmente la aplicación realizada en html+javascript para practicar. El simulador está muy logrado e implementa el funcionamiento de la maqueta con bastante detalle aunque he tenido que modificar parte del código javascript ya que no funcionaba la parte de guardar los datos. Podéis probarlo aquí.
<br>
<p align="center">
  <img src="https://garikoitz.info/blog/wp-content/uploads/2025/03/DCmotor_sim-png.webp" width="450" alt="simulador">
</p>

<h2>El Simulador</h2>
La interfaz es muy intuitiva. En la parte izquierda tenemos el disco graduado simulado. En la parte derecha tenemos las diferentes gráficas para ver la evolución de los parámetros y en la parte inferior tenemos los parámetros del PID y el control de la simulación. Cada vez que modificamos un parámetro la caja de texto se pone en amarillo y debemos pulsar la tecla «enter» para que tenga efecto. Ya que siempre uso unos términos específicos en todas mis maquetas PID os voy a poner la correspondencia de parámetros aunque entiendo que son muy intuitivos.

· Ref = SP (Punto de consigna o SetPoint)<br>
· U = OP (en términos académicos la U siempre se refiere a la salida del controlador)<br>
· Kp = Kc (creo más acertado llamar Kc a la ganancia del controlador)<br>
· Posición = PV (en el control de posición)<br>
· Velocidad = PV (en el control de velocidad)<br>

<h2>Funcionamiento</h2>
Disponemos de un servo de 5 voltios que en su eje lleva acoplado un disco graduado entre 0 y 360 grados. El voltaje aplicado sobre el motor hace que éste gire en un sentido de forma continua pudiéndose invertir la polaridad para que el motor gire en sentido contrario. A medida que aplicamos más voltaje, más rápido gira el disco.

<h2>Control de Velocidad</h2>
Atendiendo al simulador, el rango de la velocidad (PV) va de -30 a 30 º/s y el voltaje del motor (OP) va de -5 a 5 V.

<h3>Identificación</h3>
Con el control en manual y en reposo introducimos un voltaje y observamos la respuesta de la velocidad. Por suerte para nosotros la velocidad muestra una respuesta de primer orden, o dicho de otro modo, estamos antes una respuesta autorregulada.
<br>
<p align="center">
  <img src="https://garikoitz.info/blog/wp-content/uploads/2025/03/Ident_v1-1024x512.webp" width="450" alt="identificación">
</p>
Aprovechando que estamos ante una respuesta autorregulada vamos a realizar la identificación del sistema mediante el método de T1 y T2 para hallar T0 y Tp. Tanto para generar la gráfica PV/OP como para la identificación he creado dos sencillos scripts de Python que os dejo en la carpeta del proyecto.
<br>
<p align="center">
  <img src="https://garikoitz.info/blog/wp-content/uploads/2025/03/Ident_v1_identificado-2048x1229.webp" width="450" alt="steptest">
</p>

...

Tenéis la información completa de la identificación y cálculo de sintonías en la entrada del blog:
<br>
https://garikoitz.info/blog/2025/04/control-de-velocidad-con-un-motor-de-corriente-continua-simulado/
