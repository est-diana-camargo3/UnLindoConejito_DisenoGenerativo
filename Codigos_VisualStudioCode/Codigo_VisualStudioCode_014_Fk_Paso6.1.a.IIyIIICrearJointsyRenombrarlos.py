
#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║  Generador de Conejos  Aleatorios en Maya                     ║
#                         ║              M I   D U L C E   F O R T U N A                  ║
#                         ║  Desarrollado por: Mayerly Camargo codigo 1202327 y           ║
#                         ║                  Jennifer Lizeth Leiva codigo 1202617         ║                                               
#                         ║                                                               ║
#                         ╚═══════════════════════════════════════════════════════════════╝

import maya.cmds as cmds # Importamos el módulo de comandos de Maya para poder crear y manipular objetos en la escena.
import random # Importamos el módulo random para generar números aleatorios.

#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  PASO 1: Cambiar unidades a centimetros.                        ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝

cmds.currentUnit(linear="centimeter") #Cambiar unidades a centimetros para facilitar la creación de los objetos 
# Windows → Settings/Preferences → Preferences → Settings → Working Units  →"Linear"  → "centimeter"


#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║  PASO 2: Definir Modulo m. (ancho de Cabeza alearorio)        ║             
#                         ╚═══════════════════════════════════════════════════════════════╝

# ancho de cabeza es un numero entero aleatorio entre 20 y 43 cm
# nuestro modulo sera " m "
# m = ancho de cabeza / 10
ancho_cabeza = random.randint(20, 43) 
m = ancho_cabeza / 10

#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  PASO 3: Entender como Maya saca las formas, Funcion crear_cubo ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝

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
    # Al finalizar el conejo debemos reubicar los pivotes para que los joints se creen en el centro de las formas.
    offset_x = ancho / 2
    offset_y = -(alto / 2)
    offset_z = -(profundidad / 2)
    cmds.move(posicion[0] + offset_x, posicion[1] + offset_y, posicion[2] + offset_z, cubo)
    
    return cubo


#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  PASO 4: Crear Conejo Estandar                                  ║
#                         ╚═════════════════════════════════════════════════════════════════╝

def crear_conejo(emocion="calma"):
    #MiCubitoDePrueba = crear_cubo("MiCubitoDePrueba", (1, 2, 3), (0, 0, 0)) 
    # #Crea un cubo en 0,0,0 con escala 1 de ancho,2 cm de alto ,3 cm de profundo y nombre "MiCubitoDePrueba"
    # Si queremos ver las medidas del cubo: chanel box → polyCube1 → input NO en escala, la escala siempre dira 1 

    #                            nombre                            escala                            posicion 
    cabeza = crear_cubo("Cabeza_Primitiva_001",          (m*10,   m*10,         (m*10)/2 ),    (0,     0,                  0          )  ) 
    ojo_izq = crear_cubo("OjoIzquierdo_Primitiva_002",   (m,      m,            (m*1.7)  ),    (m*7,   (-(m*10)/3.7),      (m*1.7)-m  )  )
    ojo_der = crear_cubo("OjoDerecho_Primitiva_003",     (m,      m,            (m*1.7)  ),    (m*2,   (-(m*10)/3.7),      (m*1.7)-m  )  )
    nariz = crear_cubo("Nariz_Primitiva_004",            (m,      m,            (m*1.7)  ),    (m*4.5, (-(m*10)/2),        (m*1.7)-m  )  )
    boca = crear_cubo("Boca_Primitiva_005",              (m*3,    m/2,          (m*1.7)  ),    (m*3.5, (-(m*10)/1.33),     (m*1.7)-m  )  )
    oreja_izq = crear_cubo("Oreja_Izquierda_006",        (m*3,    ((m*10)/3)*2, m*2      ),    (m*6,   (((m*10)/3)*2)-m,   (-m*1.5)   )  )
    oreja_der = crear_cubo("Oreja_Derecha_007",          (m*3,    ((m*10)/3)*2, m*2      ),    (m,     (((m*10)/3)*2)-m,   (-m*1.5)   )  )
    

    pie_izq = crear_cubo("PieIzquierdo_Primitiva_008",   (m*3,    m*3,          m*2      ),    (m*6,    (-m*21),              (-m*1.5)))
    pie_der = crear_cubo("PieDerecho_Primitiva_009",     (m*3,    m*3,          m*2      ),    (m,      (-m*21),              (-m*1.5)))
    tronco = crear_cubo("Tronco_Primitiva_010",          (m*13,   m*13,         (m*16)/2 ),    (-m*1.5, (-m*9),            (m*1.5)   )  )
    mano_izq = crear_cubo("ManoIzquierda_Primitiva_011", (m*4,    m*3,          m*2      ),    (m*10.5, (-m*12),           (-m*1.5)   )  )
    mano_der = crear_cubo("ManoDerecha_Primitiva_012",   (m*4,    m*3,          m*2      ),    (-m*4.5, (-m*12),           (-m*1.5)   )  )
    cola = crear_cubo("Cola_Primitiva_013",              (m,      m,            m*2      ),    (m*4.5,  (-m*9)+(-m*7.2),   (-m*5.5)   )  ) 
    
    parte_superior = cmds.group(cabeza, ojo_izq, ojo_der, nariz, boca, oreja_izq, oreja_der, name="ParteSuperior_Grupo")
    parte_inferior = cmds.group(tronco, mano_izq, mano_der, pie_izq, pie_der, cola, name="ParteInferior_Grupo")
    conejo = cmds.group(parte_superior, parte_inferior, name="Conejo_Grupo_001")

    
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  PASO 6: Sistema FK                                             ║
#                         ╚═════════════════════════════════════════════════════════════════╝

# =========================
# PASO 6.0. UBICAR PIVOTES EN EL CENTRO DE LAS PRIMITIVAS
# =========================

#Como yo movi los pivotes a la esquina superior izquierda de la cara frontal de cada cubo, para dibujar mas fácil , 
# debo devolverlos al centro para poder obtener las coordenadas del centro en x,y,z de cada forma y colocar los joints en el x,y que me de 
# el z si debe ser en el centro de la profundidad...todos coplanares (en el paso 6.1  explico porque coplanares )

def mostrar_ejes_conejo():
    
    objetos = [
        "Cabeza_Primitiva_001",
        "Oreja_Izquierda_006", "Oreja_Derecha_007",
        "Tronco_Primitiva_010",
        "ManoIzquierda_Primitiva_011", "ManoDerecha_Primitiva_012",
        "PieIzquierdo_Primitiva_008", "PieDerecho_Primitiva_009",
        "Cola_Primitiva_013"
    ]
    
    for obj in objetos:
        if cmds.objExists(obj):
            cmds.setAttr(obj + ".displayLocalAxis", 1)
    # Para ocultarlos despues 
    #for obj in cmds.ls(type="transform"):
        #cmds.setAttr(obj + ".displayLocalAxis", 0)


# =========================
# PASO 6.1. CREAR JOINTS
# =========================
# 6.1.A. Crear joints coplanares en z= m/4
# Yo inicie a dibujar la cabeza del conejo en 0,0,0 y tiene una profundidad en z de -m*10/2,
# Por lo tanto la mitad de la profundidad de la cabeza es z= -(m*10/2)/2 es decir z= -m*10/4
# Ese es el plano central del conejo en z, ahi voy a dibujar los joints de manera coplanar 
# Porque es el plano que todas las primitivas comparten. 

# =========================
# Paso 6.1.A.I. Obtenemos posicion de pivote y caja envolvente con extremos de geometria de cada primitiva.
# =========================

def datos_primitiva(obj, z_plano):
    # Devuelve una lista [X, Y, Z] con la posicion del pivote  de la primitiva, para colocar joints EXACTAMENTE en el centro x,y en z si es (z= -m*10/4)
    centro = cmds.xform(obj, q=True, ws=True, rp=True) 
    #devuelve una lista de [xmin, ymin, zmin, xmax, ymax, zmax] para encontrar extremos de la geometría y colocar los 2 joints de las puntas o extremos (orejas, pies, etc.)
    bbox = cmds.exactWorldBoundingBox(obj)     
    return {
        "centro": (centro[0], centro[1], z_plano),
        "xmin": bbox[0],
        "ymin": bbox[1],
        "zmin": bbox[2],
        "xmax": bbox[3],
        "ymax": bbox[4],
        "zmax": bbox[5]
    }

# =========================
# Paso 6.1.A.II.   Crear joints coplanares en z= m/4 (24 JOINTS)
# Paso 6.1.A.III.  Renombrar joints (upper, middle, end)
# =========================

def crear_joints_coplanares():

    cmds.select(clear=True)

    z_plano = -(m*10)/4

    # =========================
    # COLUMNA Joints (22,23,24)
    # =========================
    cabeza = datos_primitiva("Cabeza_Primitiva_001", z_plano) # extraemos posicion del pivote y box de la caja
    tronco = datos_primitiva("Tronco_Primitiva_010", z_plano)
    cola   = datos_primitiva("Cola_Primitiva_013", z_plano)

    j22 = cmds.joint(name="UpperColumna_Frente_joint22",  p=(cabeza["centro"][0], cabeza["ymax"], z_plano) ) # centro en x, ymax en y, z en el plano coplanar
    j23 = cmds.joint(name="MiddleColumna_Cuello_joint23", p=(tronco["centro"][0], tronco["ymax"], z_plano) )
    j24 = cmds.joint(name="LowerColumna_Cadera_joint24", p=(cola["centro"][0], cola["ymax"], z_plano) )


"""
    # =========================
    # OREJA DERECHA (1,2,3)
    # =========================
    cmds.select(j22)

    earR = datos_primitiva("Oreja_Derecha_007", z_plano)

    cmds.joint(name="J1_earR_base", p=(earR["centro"][0], earR["ymin"], z_plano))
    cmds.joint(name="J2_earR_mid",  p=earR["centro"])
    cmds.joint(name="J3_earR_tip",  p=(earR["centro"][0], earR["ymax"], z_plano))

    # =========================
    # OREJA IZQUIERDA (4,5,6)
    # =========================
    cmds.select(j22)

    earL = datos_primitiva("Oreja_Izquierda_006", z_plano)

    cmds.joint(name="J4_earL_base", p=(earL["centro"][0], earL["ymin"], z_plano))
    cmds.joint(name="J5_earL_mid",  p=earL["centro"])
    cmds.joint(name="J6_earL_tip",  p=(earL["centro"][0], earL["ymax"], z_plano))

    # =========================
    # MANO DERECHA (7,8,9)
    # =========================
    cmds.select(j23)

    armR = datos_primitiva("ManoDerecha_Primitiva_012", z_plano)

    cmds.joint(name="J7_armR_base", p=(armR["xmax"], armR["centro"][1], z_plano))
    cmds.joint(name="J8_armR_mid",  p=armR["centro"])
    cmds.joint(name="J9_armR_tip",  p=(armR["xmin"], armR["centro"][1], z_plano))

    # =========================
    # MANO IZQUIERDA (10,11,12)
    # =========================
    cmds.select(j23)

    armL = datos_primitiva("ManoIzquierda_Primitiva_011", z_plano)

    cmds.joint(name="J10_armL_base", p=(armL["xmin"], armL["centro"][1], z_plano))
    cmds.joint(name="J11_armL_mid",  p=armL["centro"])
    cmds.joint(name="J12_armL_tip",  p=(armL["xmax"], armL["centro"][1], z_plano))

    # =========================
    # PIE DERECHO (13,14,15)
    # =========================
    cmds.select(j24)

    legR = datos_primitiva("PieDerecho_Primitiva_009", z_plano)

    cmds.joint(name="J13_legR_base", p=(legR["centro"][0], legR["ymax"], z_plano))
    cmds.joint(name="J14_legR_mid",  p=legR["centro"])
    cmds.joint(name="J15_legR_tip",  p=(legR["centro"][0], legR["ymin"], z_plano))

    # =========================
    # PIE IZQUIERDO (16,17,18)
    # =========================
    cmds.select(j24)

    legL = datos_primitiva("PieIzquierdo_Primitiva_008", z_plano)

    cmds.joint(name="J16_legL_base", p=(legL["centro"][0], legL["ymax"], z_plano))
    cmds.joint(name="J17_legL_mid",  p=legL["centro"])
    cmds.joint(name="J18_legL_tip",  p=(legL["centro"][0], legL["ymin"], z_plano))

    # =========================
    # COLA (19,20,21)
    # =========================
    cmds.select(j24)

    tail = datos_primitiva("Cola_Primitiva_013", z_plano)

    cmds.joint(name="J19_tail_base", p=(tail["centro"][0], tail["ymax"], z_plano))
    cmds.joint(name="J20_tail_mid",  p=tail["centro"])
    cmds.joint(name="J21_tail_tip",  p=(tail["centro"][0], tail["ymin"], z_plano))
    

    print("✅ JOINTS LIMPIOS, COPLANARES Y BIEN POSICIONADOS")
    """




#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  PASO 5: Interfaz UI                                            ║
#                         ╚═════════════════════════════════════════════════════════════════╝


# =========================
# COLORES para interfaz (RGB normalizados 0–1)
# =========================
fondorosado = (236/255, 188/255, 251/255)   # #ecbcfb
morado = (204/255, 79/255, 252/255)   # #cc4ffc
lila = (204/255, 153/255, 255/255)   # CC99FF
gris = (116/255, 116/255, 116/255)    # #747474
blanco = (1,1,1)

# =========================
# FUNCIÓN DEL BOTÓN GENERAR
# =========================
def generar_conejo_ui(*args):
    
    seleccion = cmds.radioCollection("emociones", q=True, select=True)
    
    crear_conejo(seleccion)
    mostrar_ejes_conejo()
    crear_joints_coplanares()
    


# =========================
# FUNCIÓN BOTÓN BORRAR
# =========================
def borrar_escena(*args):
    cmds.select(all=True)
    cmds.delete()

def crear_ui():
    
    if cmds.window("miVentanaConejo", exists=True):
        cmds.deleteUI("miVentanaConejo")
  
    ventana = cmds.window("miVentanaConejo", title="MI DULCE FORTUNA", widthHeight=(600, 400))

    # =========================
    # LAYOUT PRINCIPAL (2 COLUMNAS)
    # =========================
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)

    # =========================
    # 🖼️ COLUMNA IZQUIERDA (IMAGEN)
    # =========================
    ruta_imagen = "C:/Users/USUARIO/Documents/GitHub/UnLindoConejito_DisenoGenerativo/Imagenes/ImagenMenu.png"

    cmds.columnLayout(width=300)
    cmds.image(image=ruta_imagen)
    cmds.setParent('..')

    # =========================
    # 🎛️ COLUMNA DERECHA (MENÚ)
    # =========================
    cmds.columnLayout(adjustableColumn=True, bgc=fondorosado)

    cmds.separator(h=20, style="none")

    cmds.text(label="MI DULCE FORTUNA",
              height=30,
              bgc=fondorosado,
              font="boldLabelFont",
              align="center")
    cmds.separator(h=10, style="none") #espacio vacio
    
    # Raya division
    cmds.text(label="", height=6, bgc=lila)
    cmds.separator(h=1, style="in")

    cmds.separator(h=10, style="none") #espacio vacio
    cmds.text(label="Selecciona una emoción y da clic a generar", bgc=fondorosado)
    cmds.separator(h=10, style="none") #espacio vacio

    # =========================
    # EMOCIONES (DESPLAZADAS)
    # =========================
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(100, 200))  # ← 30 px espacio

    cmds.text(label="", bgc=fondorosado)  # ← espacio vacío izquierda

    cmds.columnLayout(adjustableColumn=True, bgc=fondorosado)

    cmds.radioCollection("emociones")
    cmds.radioButton("calma", label="Calma 😌", select=True)
    cmds.radioButton("tristeza", label="Tristeza 😞")
    cmds.radioButton("alegria", label="Alegría 😊")
    cmds.radioButton("ternura", label="Ternura 😍")
    cmds.radioButton("enojo", label="Enojo 😠")

    cmds.setParent('..')  # cerrar columnLayout
    cmds.setParent('..')  # cerrar rowLayout

    cmds.separator(h=15, style="none")

    # =========================
    # 4. BOTONES
    # =========================
    cmds.rowLayout(numberOfColumns=3,columnWidth3=(80, 120, 100)) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(
        label="Generar Conejito 🐰",
        command=generar_conejo_ui,
        bgc=(1,1,1),
        height=40
    )
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este
    cmds.separator(h=10, style="none")


    cmds.rowLayout(numberOfColumns=3,columnWidth3=(90, 120, 100)) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(
        label="Borrar Escena 🧹",
        command=borrar_escena,
        bgc=(1,1,1),
        height=40
    )
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este
    cmds.separator(h=10, style="none") #espacio vacio

    # Raya division
    cmds.text(label="", bgc=lila,height=6) 
    cmds.separator(h=1, style="in")

    cmds.separator(h=10, style="none") #espacio vacio
    cmds.text(label="Mayerly Camargo Pedraza Código 1202327", bgc=fondorosado)
    cmds.text(label="Jennifer Lizeth Leiva Código 1202617", bgc=fondorosado)
    cmds.text(label="Docente: Diego Felipe Beltrán Cardona", bgc=fondorosado)
    cmds.text(label="UMNG 2026", bgc=fondorosado)
   
    cmds.separator(h=20, style="none") #espacio vacio

    cmds.setParent('..')  # ← cerrar columnLayout derecha
    cmds.setParent('..')  # ← cerrar rowLayout principal

    cmds.showWindow(ventana)

# =========================
# EJECUTAR UI
# =========================
crear_ui()













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


def crear_conejo(emocion="calma"):
    
    cmds.select(all=True)
    cmds.delete()
    
    color = obtener_color(emocion)
    shader, sg = crear_material("conejo_mat", color)
    
  
    
    
    
    
    
    
    
    
    partes = [cabeza, ojo_izq, ojo_der, nariz, boca, oreja_izq, oreja_der,
              tronco, mano_izq, mano_der, pie_izq, pie_der, cola]
    
    for p in partes:
        cmds.sets(p, edit=True, forceElement=sg)
    

    
    
    conejo = cmds.group(parte_superior, parte_inferior, name="Conejo_Grupo_001")

crear_conejo("ternura") """



#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Notas                                                          ║
#                         ╚═════════════════════════════════════════════════════════════════╝

# Cambiar una variable en donde este 
# ctrl + shift +l

# Linea a copiar en el script editor de maya en la seccion python para ejecutar aplicacion de conejos
# Solo es cambiarle el numero el nombre

#import sys
#import importlib
#sys.path.append("C:/Users/USUARIO/Documents/GitHub/UnLindoConejito_DisenoGenerativo/Codigos_VisualStudioCode")
#import Codigo_VisualStudioCode_009_Interfaz
#importlib.reload(Codigo_VisualStudioCode_009_Interfaz)
#Codigo_VisualStudioCode_009_Interfaz.crear_ui()


