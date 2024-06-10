# TFM_UOC
TFM - Análisis Gentrificación Madrid

En primer lugar, aclarar a cualquier usuario que visite este repositiorio, que éste corresponde al desarrollo del proyecto de final de máster en Ciencia de Datos de la UOC con título "Análisis de los factores de gentrificación en los barrios de Madrid".

Para ejecutar el código una vez clonado, es necesario instalar los requerimientos utilizando el comando pip install -r requierements.txt. Seguidamente, se clonará el repositorio en la máquina correspondiente o se descargarán los datos en la ruta elegida por el usuario. Recomiendo crear una carpeta 'Resultados' donde se irán guardando los diferentes archivos de salida que se usarán en herramientas posteriores.

El primer paso, debido al tamaño de uno de los archivos, es acudir al portal web "https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=66665cde99be2410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default" y descargar el fichero JSON categorizado dentro de "Censo de locales y sus actividades" y en concreto en el apartado "Actividades". Una vez descargado, guardar el archivo dentro de la carpeta ...\TFM_UOC\Fuentes de datos\JSON Hostelería y Alojamientos.

Una vez instaladas todas las librerías y sus versiones correspondientes, es muy importante hacer unas pequeñas modificaciones en los códigos Python relacionados con la ruta a la que va a buscar o guardar los documentos para asegurar el correcto funcionamiento en cualquier ordenador. En concreto las modificaciones son las siguientes:

- Archivo CargaHistoricoDemografico.py: 
Línea 5 de código --> Sustituir r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Históricos Demográficos' por r'RUTA ELEGIDA POR CADA USUARIO\TFM_UOC\Fuentes de datos\Históricos Demográficos' // MUY IMPORTANTE TENER EN CUENTA GUARDAR EL DOCUMENTO combined_output.csv EN LA CARPETA 'Resultados' CREADA PREVIAMENTE.

- Archivo CargaHostelería.py: 
Línea 6 de código --> Sustituir r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\actividadeconomica202405.json' por r'RUTA ELEGIDA POR CADA USUARIO\TFM_UOC\Fuentes de datos\JSON Hostelería y Alojamientos\actividadeconomica202405.json'

Línea 45 de código --> Sustituir r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\output.csv' por r'RUTA ELEGIDA POR CADA USUARIO\TFM_UOC\Resultados\output.csv'

- Archivo CargaJSON.py: 
Línea 15 de código --> Sustituir r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\JSON Tipo Ubicaciones' por r'RUTA ELEGIDA POR CADA USUARIO\TFM_UOC\Fuentes de datos\JSON Tipo Ubicaciones' // MUY IMPORTANTE TENER EN CUENTA GUARDAR EL DOCUMENTO datos_salida.csv EN LA CARPETA 'Resultados' CREADA PREVIAMENTE.

- Archivo JoinShapefile.py:
Línea 5 de código --> Sustituir r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\output.csv' por r'RUTA ELEGIDA POR CADA USUARIO\TFM_UOC\Resultados\output.csv'

Línea 6 de código --> Sustituir r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\datos_salida.csv' por r'RUTA ELEGIDA POR CADA USUARIO\TFM_UOC\Resultados\datos_salida.csv'

Línea 9 de código --> Sustituir r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\Distritos.shp' por r'RUTA ELEGIDA POR CADA USUARIO\TFM_UOC\Fuentes de datos\Información geográfica distritos Madrid\Distritos.shp'

Línea 42 de código --> Sustituir r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\servicios_con_distritos.csv' por r'RUTA ELEGIDA POR CADA USUARIO\TFM_UOC\Resultados\servicios_con_distritos.csv'

Línea 43 de código --> Sustituir r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\ubicaciones_con_distritos.csv' por r'RUTA ELEGIDA POR CADA USUARIO\TFM_UOC\Resultados\ubicaciones_con_distritos.csv'

- Archivo KMeans_Historico_Demografico.py:
Línea 13 de código --> Sustituir r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Históricos Demográficos' por r'RUTA ELEGIDA POR CADA USUARIO\TFM_UOC\Resultados'

Línea 74 de código --> Sustituir r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\Distritos.shp' por r'RUTA ELEGIDA POR CADA USUARIO\TFM_UOC\Fuentes de datos\Información geográfica distritos Madrid\Distritos.shp'


