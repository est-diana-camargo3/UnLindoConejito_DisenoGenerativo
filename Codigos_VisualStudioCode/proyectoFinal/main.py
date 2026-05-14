
#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║         Generador de Conejos  Aleatorios en Maya              ║
#                         ║              M I   D U L C E   F O R T U N A                  ║
#                         ║     Desarrollado por: Mayerly Camargo codigo 1202327 y        ║
#                         ║              Jennifer Lizeth Leiva codigo 1202617             ║                                               
#                         ║                                                               ║
#                         ╚═══════════════════════════════════════════════════════════════╝

import maya.cmds as cmds # Módulo de comandos de Maya para crear y manipular objetos en la escena.
import sys # Llamar funciones dentro de la carpeta
import os #importar imagenes 

from proyectoFinal import sistemaChain
from proyectoFinal import sistemaIKFK
from proyectoFinal import crearConejo
from proyectoFinal import funcionesFK

#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Cambiar unidades a centimetros.                                ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝

cmds.currentUnit(linear="centimeter") #Cambiar unidades a centimetros, facilita la creación de los objetos 
# Windows → Settings/Preferences → Preferences → Settings → Working Units  →"Linear"  → "centimeter"

#region jerarquia
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Crear una jerarquia general                                    ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝

def crear_jerarquia_general():

    grupos = {

        "master": "Conejo_RIG_GRP",

        "geo": "GEO_GRP",
        "rig": "RIG_GRP",

        "fk": "FK_GRP",
        "ik": "IK_GRP",
        "main": "MAIN_GRP",

        "ctrl": "CTRL_GRP",
        "loc": "LOCATORS_GRP",
        "spline": "SPLINE_GRP",
        "systems": "SYSTEMS_GRP"
    }

    for g in grupos.values():
        if not cmds.objExists(g):
            cmds.group(em=True, n=g)

    # =========================
    # PARENTS
    # =========================

    cmds.parent(grupos["geo"], grupos["master"])
    cmds.parent(grupos["rig"], grupos["master"])

    cmds.parent(
        grupos["fk"],
        grupos["ik"],
        grupos["main"],
        grupos["ctrl"],
        grupos["loc"],
        grupos["spline"],
        grupos["systems"],
        grupos["rig"]
    )

    print("✅ Jerarquía general creada")

    return grupos
def crear_master_control():

    ctrl = cmds.circle(
        n="MASTER_CTRL",
        nr=(0,1,0),
        r=40
    )[0]

    root = cmds.group(ctrl, n="MASTER_CTRL_ROOT")

    cmds.parent("RIG_GRP", ctrl)
    cmds.parent("GEO_GRP", ctrl)

    print("✅ MASTER CTRL creado")

    return ctrl

def organizar_cadenas_principales():

    joints = cmds.ls(type="joint")

    for j in joints:

        raiz = cmds.listRelatives(j, parent=True)

        # SOLO raíces
        if raiz:
            continue

        if j.startswith("FK_"):
            cmds.parent(j, "FK_GRP")

        elif j.startswith("IK_"):
            cmds.parent(j, "IK_GRP")

        elif j.startswith("MAIN_"):
            cmds.parent(j, "MAIN_GRP")

    print("✅ Cadenas organizadas")

def crear_grupo_sistema(nombre):

    grp = f"{nombre}_SYSTEM_GRP"

    if not cmds.objExists(grp):
        grp = cmds.group(em=True, n=grp)

        cmds.parent(grp, "SYSTEMS_GRP")

    return grp

def organizar_chain_system(
        nombre,
        curve,
        locators,
        targets,
        roots
    ):

    sistema_grp = crear_grupo_sistema(nombre)

    # =========================
    # SUBGRUPOS
    # =========================

    curve_grp = cmds.group(em=True, n=f"{nombre}_CURVES_GRP")
    loc_grp = cmds.group(em=True, n=f"{nombre}_LOCATORS_GRP")
    ctrl_grp = cmds.group(em=True, n=f"{nombre}_CTRLS_GRP")
    target_grp = cmds.group(em=True, n=f"{nombre}_TARGETS_GRP")

    cmds.parent(
        curve_grp,
        loc_grp,
        ctrl_grp,
        target_grp,
        sistema_grp
    )

    # =========================
    # PARENT
    # =========================

    cmds.parent(curve, curve_grp)

    if locators:
        cmds.parent(locators, loc_grp)

    if targets:
        cmds.parent(targets, target_grp)

    if roots:
        cmds.parent(roots, ctrl_grp)

    print(f"✅ Sistema organizado -> {nombre}")


# endregion

def crear_controles_anatomicos():

    controles = {}

    # =========================
    # COG / PELVIS
    # =========================

    size = funcionesFK.tamano_desde_geometria(
        "Tronco_Primitiva_010",
        1.3
    )

    cog = cmds.circle(
        n="COG_CTRL",
        nr=(0,1,0),
        r=size
    )[0]

    cog_offset = cmds.group(
        cog,
        n="COG_CTRL_OFFSET"
    )

    cmds.delete(
        cmds.parentConstraint(
            "FK_Joint_08_Interno_ColumnaCadera",
            cog_offset
        )
    )

    controles["cog"] = cog

    # =========================
    # CHEST
    # =========================

    chest = cmds.circle(
        n="CHEST_CTRL",
        nr=(0,1,0),
        r=size * 0.8
    )[0]

    chest_offset = cmds.group(
        chest,
        n="CHEST_CTRL_OFFSET"
    )

    cmds.delete(
        cmds.parentConstraint(
            "FK_Joint_18_Medio_ColumnaCuello",
            chest_offset
        )
    )

    controles["chest"] = chest

    # =========================
    # HEAD
    # =========================

    head_size = funcionesFK.tamano_desde_geometria(
        "Cabeza_Primitiva_001"
    )

    head = cmds.circle(
        n="HEAD_CTRL",
        nr=(0,1,0),
        r=head_size
    )[0]

    head_offset = cmds.group(
        head,
        n="HEAD_CTRL_OFFSET"
    )

    cmds.delete(
        cmds.parentConstraint(
            "FK_Joint_19_ColumnaFrente",
            head_offset
        )
    )

    controles["head"] = head

    print("✅ Controles anatómicos creados")

    return controles

def crear_jerarquia_anatomica():

    # =========================
    # MASTER -> COG
    # =========================

    cmds.parent(
        "COG_CTRL_OFFSET",
        "MASTER_CTRL"
    )

    # =========================
    # COG -> CHEST
    # =========================

    cmds.parent(
        "CHEST_CTRL_OFFSET",
        "COG_CTRL"
    )

    # =========================
    # CHEST -> HEAD
    # =========================

    cmds.parent(
        "HEAD_CTRL_OFFSET",
        "CHEST_CTRL"
    )

    print("✅ Jerarquía anatómica creada")

def conectar_columna_a_controles():

    cmds.parentConstraint(
        "COG_CTRL",
        "FK_root_08_Interno_ColumnaCadera",
        mo=True
    )

    cmds.parentConstraint(
        "CHEST_CTRL",
        "FK_root_18_Medio_ColumnaCuello",
        mo=True
    )

    cmds.parentConstraint(
        "HEAD_CTRL",
        "FK_root_19_ColumnaFrente",
        mo=True
    )

    print("✅ Columna conectada")


def conectar_extremidades():

    # =========================
    # BRAZOS
    # =========================

    cmds.parent(
        "BrazoL_IK_CTRL_001_OFFSET",
        "CHEST_CTRL"
    )

    cmds.parent(
        "BrazoR_IK_CTRL_001_OFFSET",
        "CHEST_CTRL"
    )

    # =========================
    # PIERNAS
    # =========================

    cmds.parent(
        "PiernaL_IK_CTRL_001_OFFSET",
        "COG_CTRL"
    )

    cmds.parent(
        "PiernaR_IK_CTRL_001_OFFSET",
        "COG_CTRL"
    )

    print("✅ Extremidades conectadas")


def conectar_partes_secundarias():

    # =========================
    # OREJAS
    # =========================

    cmds.parent(
        "EarL_SYSTEM_GRP",
        "HEAD_CTRL"
    )

    cmds.parent(
        "EarR_SYSTEM_GRP",
        "HEAD_CTRL"
    )

    # =========================
    # COLA
    # =========================

    cmds.parent(
        "Tail_SYSTEM_GRP",
        "COG_CTRL"
    )

    print("✅ Orejas y cola conectadas")


#region fkik
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  generar sistema FKIK general                                   ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝


def crear_sistema_fkik(lista_fk, resultado_dup):

    sistemas = [
        {
            "fk": lista_fk["brazoR_FK"],
            "ik": [
                "IK_Joint_15_Interno_ManoDerecha",
                "IK_Joint_16_medio_ManoDerecha",
                "IK_Joint_17_Externo_ManoDerecha"
            ],
            "main": [
                "MAIN_Joint_15_Interno_ManoDerecha",
                "MAIN_Joint_16_medio_ManoDerecha",
                "MAIN_Joint_17_Externo_ManoDerecha"
            ],
            "prefix": "BrazoR"
        },

        {
            "fk": lista_fk["brazoL_FK"],
            "ik": [
                "IK_Joint_12_Interno_ManoIzquierda",
                "IK_Joint_13_medio_ManoIzquierda",
                "IK_Joint_14_Externo_ManoIzquierda"
            ],
            "main": [
                "MAIN_Joint_12_Interno_ManoIzquierda",
                "MAIN_Joint_13_medio_ManoIzquierda",
                "MAIN_Joint_14_Externo_ManoIzquierda"
            ],
            "prefix": "BrazoL"
        },

        {
            "fk": lista_fk["piernaR_FK"],
            "ik": [
                "IK_Joint_05_Interno_PieDerecho",
                "IK_Joint_06_medio_PieDerecho",
                "IK_Joint_07_Externo_PieDerecho"
            ],
            "main": [
                "MAIN_Joint_05_Interno_PieDerecho",
                "MAIN_Joint_06_medio_PieDerecho",
                "MAIN_Joint_07_Externo_PieDerecho"
            ],
            "prefix": "PiernaR"
        },

        {
            "fk": lista_fk["piernaL_FK"],
            "ik": [
                "IK_Joint_02_Interno_PieIzquierdo",
                "IK_Joint_03_medio_PieIzquierdo",
                "IK_Joint_04_Externo_PieIzquierdo"
            ],
            "main": [
                "MAIN_Joint_02_Interno_PieIzquierdo",
                "MAIN_Joint_03_medio_PieIzquierdo",
                "MAIN_Joint_04_Externo_PieIzquierdo"
            ],
            "prefix": "PiernaL"
        }
    ]

    resultados = {}
    for s in sistemas:

        resultado = sistemaIKFK.crear_sistema_ikfk(
            fk_chain=s["fk"],
            ik_chain=s["ik"],
            main_chain=s["main"],
            prefix=s["prefix"],
            joint_attr=s["main"][0]
        )

        resultados[s["prefix"]] = resultado

    print("✅ FKIK GENERAL COMPLETO")

    return resultados
# endregion

"""# region chain"""
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  generar sistema chain react general                            ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝

def crear_chain_reaction(
        joints,
        nombre,
        aimVector=(1,0,0)
    ):

    # =========================
    # POSICIONES
    # =========================

    positions = [
        cmds.xform(j, q=True, ws=True, t=True)
        for j in joints
    ]

    # =========================
    # SPLINE
    # =========================
    

    curve, shape = sistemaChain.create_spline_from_joints(joints)

    # =========================
    # LOCATORS
    # =========================

    locators = sistemaChain.create_locators_and_connect(
        shape,
        positions
    )

    # =========================
    # DECOMPOSE
    # =========================

    sistemaChain.connect_with_decompose(
        locators,
        shape
    )

    # =========================
    # CONTROLES
    # =========================

    ctrls = sistemaChain.create_controls(locators)

    # =========================
    # ROOTS
    # =========================

    roots = sistemaChain.create_root_groups(ctrls)

    # =========================
    # TARGETS
    # =========================

    targets = sistemaChain.create_targets(shape)

    # =========================
    # AIM
    # =========================

    sistemaChain.create_aim_constraints(targets)

    # =========================
    # FOLLOW
    # =========================

    sistemaChain.connect_joints_to_targets(
        joints,
        targets
    )

    # =========================
    # ORGANIZAR
    # =========================

    organizar_chain_system(
        nombre,
        curve,
        locators,
        targets,
        roots
    )

    print(f"✅ Chain Reaction creado -> {nombre}")

    return {
        "curve": curve,
        "locators": locators,
        "targets": targets,
        "roots": roots
    }
def crear_todos_los_chain_systems(lista_fk):

    resultados = {}

    sistemas = [

        {
            "joints": lista_fk["columna_FK"],
            "nombre": "Spine"
        },

        {
            "joints": lista_fk["cola_FK"],
            "nombre": "Tail"
        },

        {
            "joints": lista_fk["orejaR_FK"],
            "nombre": "EarR"
        },

        {
            "joints": lista_fk["orejaL_FK"],
            "nombre": "EarL"
        }
    ]

    for s in sistemas:

        resultado = crear_chain_reaction(
            s["joints"],
            s["nombre"]
        )

        resultados[s["nombre"]] = resultado

    print("✅ TODOS LOS CHAIN SYSTEMS CREADOS")

    return resultados
# endregion

# region ui
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Interfaz UI                                                    ║
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
    crearConejo.crear_conejo(seleccion)
    crear_jerarquia_general()
    lista_fk = funcionesFK.crear_joints_coplanares(crearConejo.m)
    funcionesFK.orientar_joints_de_toda_la_cadena_FK(lista_fk)
    resultado_dup = funcionesFK.duplicar_y_renombrar_cadenas_IK_y_MAIN()
    funcionesFK.ocultar_cadenas_IK_y_MAIN()
    organizar_cadenas_principales()
    funcionesFK.crear_fk_auto_root_control(lista_fk)
    crear_sistema_fkik(
        lista_fk,
        resultado_dup
    )
    crear_todos_los_chain_systems(lista_fk)

    
    crear_master_control()
    
    crear_controles_anatomicos()

    crear_jerarquia_anatomica()

    conectar_columna_a_controles()

    conectar_extremidades()

    conectar_partes_secundarias()

    
    #suavizar_conejo_preview()
    


# =========================
# FUNCIÓN BOTÓN BORRAR
# =========================
def borrar_escena(*args):
    cmds.select(all=True)
    cmds.delete()

# =========================
# CREACIÓN UI
# =========================
def crear_ui():
    
    if cmds.window("miVentanaConejo", exists=True):
        cmds.deleteUI("miVentanaConejo")
    ventana = cmds.window("miVentanaConejo", title="MI DULCE FORTUNA", widthHeight=(600, 400))

    # =========================
    # LAYOUT PRINCIPAL (2 COLUMNAS)
    # =========================
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)

    # =========================
    # COLUMNA IZQUIERDA (IMAGEN)
    # =========================

    ruta_actual = os.path.dirname(__file__)

    ruta_imagen = os.path.join(
        ruta_actual,
        "ImagenMenu.png"
    )

    ruta_imagen = ruta_imagen.replace("\\", "/")

    cmds.columnLayout(width=300)

    cmds.image(image=ruta_imagen)

    cmds.setParent('..')

    # =========================
    # COLUMNA DERECHA (MENÚ)
    # =========================
    cmds.columnLayout(adjustableColumn=True, bgc=fondorosado)

    cmds.separator(h=20, style="none")

    cmds.text(label="MI DULCE FORTUNA", height=35,  bgc=fondorosado,font="boldLabelFont",align="center")
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
    cmds.radioButton("aPieria", label="APiería 😊")
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
# endregion

# region Notas

#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Notas                                                          ║
#                         ╚═════════════════════════════════════════════════════════════════╝

# Cambiar una variable en donde este 
# ctrl + shift +l

"""Comentario"""
""" # region Notas
# código aquí
# endregion
"""

# Linea a copiar en el script editor de maya en la seccion python para ejecutar aplicacion de conejos
# Solo es cambiarle el numero el nombre

#import sys
#import importlib
#sys.path.append("C:/Users/USUARIO/Documents/GitHub/UnLindoConejito_DisenoGenerativo/Codigos_VisualStudioCode")
#import Codigo_VisualStudioCode_021_Fk_Paso62c_FKCurvasDeControl
#importlib.reload(Codigo_VisualStudioCode_021_Fk_Paso62c_FKCurvasDeControl)
#Codigo_VisualStudioCode_021_Fk_Paso62c_FKCurvasDeControl.crear_ui()
# endregion

# region Codigo sin usar
"""

def obtener_color(emocion):
    colores = {
        "calma": (0.88, 0.98, 0.92),
        "tristeza": (0.0, 0.41, 0.54),
        "aPieria": (1.0, 0.85, 0.6),
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
# endregion













