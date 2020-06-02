# E3 versión 1.0.0
Aplicación de escritorio hecha en Python. Estadísticas de temperatura y precipitaciones de un registro meteorológico.<br>
Con E3 se pueden visualizar datos, crear estadísticas y gráficos en base a un archivo de extensión .txt que contengan registros
meteorológicos diarios.
Dicho archivo debe respetar un formato, 6 columnas siguiendo el siguiente orden: año, mes, dia, precipitacion, temperatura máxima y 
temperatura mínima. Estas 3 últimas variables deben usar un punto (.) como decimal, y en caso de faltantes, deben ser escritos como
NaN. Las columnas no deben llevar títulos. La aplicación, por el momento, no realiza ningun control de calidad de los datos, tales como
outliers o fechas repetidas.
Un ejemplo en pocas líneas:

1990 1 1 0.0 18.7 9.6 <br>
1990 1 2 0.0 21.4 NaN <br>
1990 1 3 0.0 22.4 14 <br>

Algunas cosas que se pueden hacer con la aplicación:
-Ver, descargar y graficar valores diarios entre una fecha y otra <br>
-Obtener, descargar y graficar valores mensuales medios y extremos, entre un año inicial y un año final <br>
-Formar un ranking por mes, por quincena o por década (10 días) <br>
-Calcular los percentiles múltiplos al 5 del período 1981-2010. <br>

Pronto podrá ser descargado en un PDF el manual completo.

La aplicación se encuentra en proceso de mejora, razón por la cual estoy trabajando en crear nuevas funcionalidades o mejorarlas.
Entre ellas, planeo agregar la opción de línea de tendencias a los gráficos, armada de estadísticas del período 1981-2010 (luego
será 1991-2020) para ser descargados en un txt, y algún pequeño control de los datos (detectar cuando hay demasiada cantidad de
datos faltantes).

Contacto: infometeoba.blogspot
