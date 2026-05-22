#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║                    PINTAR CONEJO PROCEDURAL                   ║
#                         ║              Estilos: PixelArt y Bento Art                   ║
#                         ╚═══════════════════════════════════════════════════════════════╝

import maya.cmds as cmds
import random

from proyectoFinal.paletas import PALETAS


# =========================================================
# DATOS CURIOSOS
# =========================================================

def generar_dato_curioso(emocion="calma"):

    global dato_curioso

    if emocion == "descanso":
        dato_curioso = "La piedra de jade esta relacionada \ncon la buena suerte y el descanso"

    elif emocion == "feo":
        dato_curioso = "El color mostaza ocre junto con \ngris opaco y violeta no es bello a la vista\n debido a su falta de luz"

    elif emocion == "pequeno":
        dato_curioso = "Los colores gris, cafe y rosado eran \nusados por personas de clase baja que no \nse podian permitir una tintura pura"

    elif emocion == "fantasia":
        dato_curioso = "El color púrpura se relaciona con la \niglesia, de ahi que se relacione con los milagros \ny la fantasía"

    elif emocion == "odio":
        dato_curioso = "El color negro transforma la cualidad \npositiva de un color en negativa ejm: el \nrojo es amor, pero con negro es odio"

    elif emocion == "envidia":
        dato_curioso = "El amarillo intenso es el color \nde la envidia."

    elif emocion == "artificial":
        dato_curioso = "El color morado representa lo artificial y mágico."

    elif emocion == "verdad":
        dato_curioso = "El color oro representa lo digno, poderoso y verdadero."


# =========================================================
# MATERIAL DEGRADADO SUAVE
# =========================================================

# =========================================================
# MATERIAL DEGRADADO CABEZA → PIES
# =========================================================

def crear_material_degradado(nombre, emocion):

    # =====================================================
    # MATERIAL BLINN
    # =====================================================

    material = cmds.shadingNode(
        "blinn",
        asShader=True,
        name=f"{nombre}_{emocion}_MAT"
    )

    shading_group = cmds.sets(
        renderable=True,
        noSurfaceShader=True,
        empty=True,
        name=f"{material}SG"
    )

    cmds.connectAttr(
        f"{material}.outColor",
        f"{shading_group}.surfaceShader",
        force=True
    )

    # =====================================================
    # LOOK BRILLANTE
    # =====================================================

    cmds.setAttr(f"{material}.eccentricity", 0.25)
    cmds.setAttr(f"{material}.specularRollOff", 0.45)

    cmds.setAttr(
        f"{material}.specularColor",
        1,
        1,
        1,
        type="double3"
    )

    # =====================================================
    # RAMP
    # =====================================================

    ramp = cmds.shadingNode(
        "ramp",
        asTexture=True,
        name=f"{nombre}_{emocion}_RAMP"
    )

    # degradado suave
    cmds.setAttr(f"{ramp}.interpolation", 3)

    # vertical
    cmds.setAttr(f"{ramp}.type", 0)

    # =====================================================
    # PLACE2D
    # =====================================================

    place2d = cmds.shadingNode(
        "place2dTexture",
        asUtility=True,
        name=f"{nombre}_{emocion}_PLACE2D"
    )

    # conexiones necesarias
    cmds.connectAttr(
        f"{place2d}.outUV",
        f"{ramp}.uvCoord",
        force=True
    )

    cmds.connectAttr(
        f"{place2d}.outUvFilterSize",
        f"{ramp}.uvFilterSize",
        force=True
    )

    # =====================================================
    # PALETA
    # =====================================================

    paleta = PALETAS[emocion]

    # =====================================================
    # USAR CADA COLOR SOLO UNA VEZ
    # =====================================================

    paleta_ordenada = sorted(
        paleta,
        key=lambda x: x[1],
        reverse=True
    )

    total_pesos = sum(
        porcentaje for color, porcentaje in paleta_ordenada
    )

    acumulado = 0

    for i, (color, porcentaje) in enumerate(paleta_ordenada):

        posicion = acumulado / float(total_pesos)

        cmds.setAttr(
            f"{ramp}.colorEntryList[{i}].position",
            posicion
        )

        cmds.setAttr(
            f"{ramp}.colorEntryList[{i}].color",
            color[0],
            color[1],
            color[2],
            type="double3"
        )

        acumulado += porcentaje

    # último color abajo
    cmds.setAttr(
        f"{ramp}.colorEntryList[{len(paleta_ordenada)-1}].position",
        1
    )

    # =====================================================
    # ESCALA DEL DEGRADADO
    # =====================================================

    cmds.setAttr(
        f"{place2d}.repeatUV",
        1,
        1,
        type="double2"
    )

    # =====================================================
    # RAMP → MATERIAL
    # =====================================================

    cmds.connectAttr(
        f"{ramp}.outColor",
        f"{material}.color",
        force=True
    )

    return material

# =========================================================
# CREAR MATERIAL SIMPLE
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
# COLOR ALEATORIO
# =========================================================

def obtener_color_aleatorio(emocion):

    datos_paleta = PALETAS[emocion]

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
# PIXEL ART
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

            color = obtener_color_aleatorio(emocion)

            nombre_material = f"PIXEL_MAT_{contador}"

            sg = crear_material(
                nombre_material,
                color
            )

            cmds.sets(
                cara,
                edit=True,
                forceElement=sg
            )

            contador += 1

    print("✅ Estilo PixelArt aplicado")


# =========================================================
# BENTO ART
# =========================================================

def aplicar_bento(emocion):

    objetos = cmds.ls("*Primitiva*")

    contador = 0

    for obj in objetos:

        caras = cmds.ls(
            obj + ".f[*]",
            flatten=True
        )

        bloques = [
            caras[i:i+6]
            for i in range(0, len(caras), 6)
        ]

        for bloque in bloques:

            color = obtener_color_aleatorio(emocion)

            nombre_material = f"BENTO_MAT_{contador}"

            sg = crear_material(
                nombre_material,
                color
            )

            for cara in bloque:

                cmds.sets(
                    cara,
                    edit=True,
                    forceElement=sg
                )

            contador += 1

    print("✅ Estilo Bento aplicado")