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

