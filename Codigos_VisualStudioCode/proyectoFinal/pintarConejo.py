#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║                    PINTAR CONEJO PROCEDURAL                   ║
#                         ║              Estilos: PixelArt y Bento Art                   ║
#                         ╚═══════════════════════════════════════════════════════════════╝

import maya.cmds as cmds
import random

from proyectoFinal import paletas

def generar_dato_curioso(emocion="calma"):

    global dato_curioso

    if emocion == "descanso":
        dato_curioso = "La piedra de jade esta relacionada \ncon la buena suerte y el descanso"

    elif emocion == "feo":
        dato_curioso = "El color mostaza ocre junto con \ngris opaco y violeta no es bello a la vista\n debido a su falta de luz"

    elif emocion == "pequeño":
        dato_curioso = "Los colores gris, cafe y rosado eran \nusados por personas de clase baja que no \nse podian permitir una tintura pura"

    elif emocion == "fantasia":
        dato_curioso = "El color púrpura se relaciona con la \niglesia, de ahi que se relacione con los milagros \ny la fantasía"

    elif emocion == "odio":
        dato_curioso = "El color negro transforma la cualidad \npositiva de un color en negativa ejm: el \nrojo es amor, pero con negro es odio"

    elif emocion == "envidia":
        dato_curioso = "El amarillo intenso es el color \nde la envidia."

    elif emocion == "artificial":
            dato_curioso = "El color morado repsenta lo artificial y magico."

    elif emocion == "verdad":
            dato_curioso = "El color oro representa lo digno, poderoso y veradero."

   


# =========================================================
# CREAR MATERIAL
# =========================================================

def crear_material(nombre, color):

    shader = cmds.shadingNode(
        "lambert",
        asShader=True,
        name=nombre
    )

    cmds.setAttr(
        shader + ".color",
        color[0],
        color[1],
        color[2],
        type="double3"
    )

    sg = cmds.sets(
        renderable=True,
        noSurfaceShader=True,
        empty=True,
        name=nombre + "SG"
    )

    cmds.connectAttr(
        shader + ".outColor",
        sg + ".surfaceShader",
        force=True
    )

    return sg


# =========================================================
# OBTENER COLOR ALEATORIO SEGÚN PALETA
# =========================================================

def obtener_color_aleatorio(emocion):

    datos_paleta = paletas.PALETAS[emocion]

    colores = []
    pesos = []

    for color, porcentaje in datos_paleta:

        colores.append(color)
        pesos.append(porcentaje)

    color_elegido = random.choices(
        colores,
        weights=pesos,
        k=1
    )[0]

    return color_elegido


# =========================================================
# ESTILO PIXEL ART
# Cada cara obtiene un color distinto
# =========================================================

def aplicar_pixelart(emocion):

    objetos = cmds.ls("*Primitiva*")

    contador = 0

    for obj in objetos:

        caras = cmds.ls(
            obj + ".f[*]",
            flatten=True
        )

        for cara in caras:

            # =========================
            # COLOR ALEATORIO
            # =========================

            color = obtener_color_aleatorio(emocion)

            # =========================
            # MATERIAL
            # =========================

            nombre_material = f"PIXEL_MAT_{contador}"

            sg = crear_material(
                nombre_material,
                color
            )

            # =========================
            # ASIGNAR MATERIAL
            # =========================

            cmds.sets(
                cara,
                edit=True,
                forceElement=sg
            )

            contador += 1

    print("✅ Estilo PixelArt aplicado")


# =========================================================
# ESTILO BENTO ART
# Bloques de caras comparten color
# =========================================================

def aplicar_bento(emocion):

    objetos = cmds.ls("*Primitiva*")

    contador = 0

    for obj in objetos:

        caras = cmds.ls(
            obj + ".f[*]",
            flatten=True
        )

        # =========================
        # DIVIDIR EN BLOQUES
        # =========================

        bloques = [
            caras[i:i+6]
            for i in range(0, len(caras), 6)
        ]

        for bloque in bloques:

            # =========================
            # COLOR DEL BLOQUE
            # =========================

            color = obtener_color_aleatorio(emocion)

            # =========================
            # MATERIAL
            # =========================

            nombre_material = f"BENTO_MAT_{contador}"

            sg = crear_material(
                nombre_material,
                color
            )

            # =========================
            # ASIGNAR A TODAS LAS CARAS
            # =========================

            for cara in bloque:

                cmds.sets(
                    cara,
                    edit=True,
                    forceElement=sg
                )

            contador += 1

    print("✅ Estilo Bento aplicado")




