
#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║  Generador de Conejos  Aleatorios en Maya                     ║
#                         ║              M I   D U L C E   F O R T U N A                  ║
#                         ║  Desarrollado por: Mayerly Camargo codigo 1202327 y           ║
#                         ║                  Jennifer Lizeth Leiva codigo 1202617         ║                                               
#                         ║                                                               ║
#                         ╚═══════════════════════════════════════════════════════════════╝

import maya.cmds as cmds # Importamos el módulo de comandos de Maya para poder crear y manipular objetos en la escena.
import random # Importamos el módulo random para generar números aleatorios.

#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║  PASO 1: Cambiar unidades a centimetros.                      ║                                                               ║
#                         ╚═══════════════════════════════════════════════════════════════╝

cmds.currentUnit(linear="centimeter") #Cambiar unidades a centimetros para facilitar la creación de los objetos 
# Windows → Settings/Preferences → Preferences → Settings → Working Units  →"Linear"  → "centimeter"


#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║  PASO 2: Entender como Maya saca las formas                   ║                                                               ║
#                         ╚═══════════════════════════════════════════════════════════════╝

def crear_cubo(nombre, escala, posicion): 
    ancho, alto, profundidad = escala # Definimos como se llamaran los valores de la escala, en lugar de w.h.d que son por defecto.
    #Creamos una función reutilizable para dibujar n cubos.
    # parametros: nombre STRING que llevara el cubo en el ouliner de maya (string), 
    #             escala VECTOR (3 valores para x= ancho, y= alto, z= profundidad),
    #             posicion VECTOR (3 valores para coordenadas x,y,z)
  
    cubo = cmds.polyCube( name=nombre, w=ancho, h=alto, d=profundidad )[0]  
    #Creamos un cubo con el comando polyCube y le asignamos un nombre.  y una escala
    #                                    la razon por la que usamos una lista, es porque polycube devuelve una lista, 
    #                                    En la que el primer elemento es el objeto (la geometria)
    #                                    y el segundo elemento es las transformaciones que se le han hecho
    #                                    nosotros cogemos la primera que es el objeto y le asigamos nombre y escala. 
    
    #Calculamos el offset de la posicion, porque por defcto el cubo se crea con su centro en el origen (0,0,0), y nosotros queremos que siempre el 
    # punto de referencia sea la esquina superior izquierda de la cara frontal del cubo, y que se dibuje de ahi para abajo y hacia la derecha y la sobre el plano xy osea z=0
    offset_x = ancho / 2
    offset_y = -(alto / 2)
    offset_z = -(profundidad / 2)
    cmds.move(posicion[0] + offset_x, posicion[1] + offset_y, posicion[2] + offset_z, cubo)
    return cubo


cabeza = crear_cubo("MiCubitoDePrueba", (1, 2, 3), (0, 0, 0)) #Dibujamos un cubo de prueba y Funciona perfectamente 







#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║  PASO 1: Cambiar unidades a centimetros.                      ║                                                               ║
#                         ╚═══════════════════════════════════════════════════════════════╝

ancho_cabeza = random.uniform(2.0, 4.3) #Generamos un número aleatorio entre 2.0 y 4.3 para el ancho de la cabeza del conejo, esto nos permitirá crear conejos de diferentes tamaños cada vez que ejecutemos el script.






"""

def obtener_color(emocion):
    colores = {
        "calma": (0.88, 0.98, 0.92),
        "tristeza": (0.0, 0.41, 0.54),
        "alegria": (1.0, 0.85, 0.6),
        "ternura": (0.96, 0.8, 1.0),
        "enojo": (1.0, 0.58, 0.58)
    }
    return colores.get(emocion, (1,1,1))

def crear_material(nombre, color):
    shader = cmds.shadingNode('lambert', asShader=True, name=nombre)
    cmds.setAttr(shader + ".color", color[0], color[1], color[2], type="double3")
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=nombre + "SG")
    cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True)
    return shader, sg

def crear_cubo(nombre, escala, posicion):
    cubo = cmds.polyCube(name=nombre)[0]
    cmds.scale(escala[0], escala[1], escala[2], cubo)
    cmds.move(posicion[0], posicion[1], posicion[2], cubo)
    return cubo

def crear_conejo(emocion="calma"):
    
    cmds.select(all=True)
    cmds.delete()
    
    color = obtener_color(emocion)
    shader, sg = crear_material("conejo_mat", color)
    
    ancho_cabeza = random.uniform(2.0, 4.3)
    
    cabeza = crear_cubo("Cabeza_Primitiva_001", (ancho_cabeza, ancho_cabeza, ancho_cabeza), (0, 5, 0))
    
    ojo_izq = crear_cubo("OjoIzquierdo_Primitiva_002", (0.2,0.2,0.2), (-0.5,5.5,1))
    ojo_der = crear_cubo("OjoDerecho_Primitiva_003", (0.2,0.2,0.2), (0.5,5.5,1))
    
    nariz = crear_cubo("Nariz_Primitiva_004", (0.2,0.2,0.2), (0,5.2,1))
    boca = crear_cubo("Boca_Primitiva_005", (0.4,0.1,0.1), (0,4.8,1))
    
    oreja_izq = crear_cubo("Oreja_Izquierda_006", (0.5,2,0.5), (-0.5,7,0))
    oreja_der = crear_cubo("Oreja_Derecha_007", (0.5,2,0.5), (0.5,7,0))
    
    tronco = crear_cubo("Tronco_Primitiva_010", (3,4,2), (0,2,0))
    
    mano_izq = crear_cubo("ManoIzquierda_Primitiva_011", (0.5,1.5,0.5), (-2,2,0))
    mano_der = crear_cubo("ManoDerecha_Primitiva_012", (0.5,1.5,0.5), (2,2,0))
    
    pie_izq = crear_cubo("PieIzquierdo_Primitiva_008", (0.7,0.7,0.7), (-1,0,0))
    pie_der = crear_cubo("PieDerecho_Primitiva_009", (0.7,0.7,0.7), (1,0,0))
    
    cola = crear_cubo("Cola_Primitiva_013", (0.5,0.5,0.5), (0,2,-1.5))
    
    partes = [cabeza, ojo_izq, ojo_der, nariz, boca, oreja_izq, oreja_der,
              tronco, mano_izq, mano_der, pie_izq, pie_der, cola]
    
    for p in partes:
        cmds.sets(p, edit=True, forceElement=sg)
    
    parte_superior = cmds.group(cabeza, ojo_izq, ojo_der, nariz, boca, oreja_izq, oreja_der, name="ParteSuperior_Grupo")
    parte_inferior = cmds.group(tronco, mano_izq, mano_der, pie_izq, pie_der, cola, name="ParteInferior_Grupo")
    
    conejo = cmds.group(parte_superior, parte_inferior, name="Conejo_Grupo_001")

crear_conejo("ternura")

  """