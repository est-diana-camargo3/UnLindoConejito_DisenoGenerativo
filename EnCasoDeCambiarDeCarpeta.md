##### **#SI SE CAMBIA DE CARPETA de ejecucion se debe cambiar la ruta en el userSetup**

\#Ruta C:\\Users\\USUARIO\\Documents\\Maya\\scripts

\##Aqui se puede copiar directamente la ruta desde la barra de la carpeta, los slash deben ir asi \\



import maya.cmds as cmds

import sys

sys.path.append(r"C:\\Users\\USUARIO\\Documents\\GitHub\\UnLindoConejito\_DisenoGenerativo\\Codigos\_VisualStudioCode\\proyectoFinal")

sys.path.append(r"C:\\Users\\USUARIO\\Documents\\GitHub\\vscode-environment-for-maya\\.venv\\Lib\\site-packages")

if not cmds.commandPort(":4434", query=True):

&#x20;   cmds.commandPort(name=":4434")





##### **#Luego ahi si copiamos esta ruta en el script editor de maya en la seccion python para ejecutar aplicacion de conejos**

Solo es cambiarle la ruta

Aqui NO se puede copiar la ruta desde la barra de la carpeta deben ir asi /



import sys

import importlib

sys.path.append("C:/Users/USUARIO/Documents/GitHub/UnLindoConejito\_DisenoGenerativo/Codigos\_VisualStudioCode")

from proyectoFinal import main

importlib.reload(main)

main.crear\_ui()





#### **#Regiones**



\#region Colores  

aquí va el código 

\#endregion





#### **#Contraer y mostrar todo** 

contraer 

&#x09;ctrl+k luego ctrl+2

mostrar

&#x09;ctrl+k luego ctrl+j





#### **#Filas y columnas en una ventana** 

&#x20;   # region Ventana, Medidas y scroll  

&#x20;   # rowLayout UNA sola fila horizontal.  

&#x20;   #                                       \[ elemento ]\[ elemento ]\[ elemento ]

&#x20;   # rowColumnLayout sirve para organizar tablas 

&#x20;   #                                       \[ elemento ]\[ elemento ]\[ elemento ]

&#x20;   #                                       \[ elemento ]\[ elemento ]\[ elemento ]

&#x20;   #                                       \[ elemento ]\[ elemento ]\[ elemento ]

&#x20;   # En Maya no creamos las filas de manera manual estas se crean con rowColumnLayout dependiendo de cuantos 

&#x20;   # elementos agreguemos, por ejemplo si hacemos un rowColumnLayout de 3 columnas y agregamos 6 elementos se van a organizar asi:

&#x20;   #  1 | 2 | 3

&#x20;   #  4 | 5 | 6...y asi sucesivamente dependiendo cuandos elementos agreguemos.

&#x20;   # cmds.columnLayout crea columna vertical

&#x20;   # cmds.columnLayout(  columnAttach=("left", 30)) #Padding interno

&#x20;   

&#x20;   #---Raya division lila

&#x20;   #cmds.separator(h=5, style="none") #espacio vacio

&#x20;   #cmds.text(label="", height=6, width=anchomenu,bgc=lila)



