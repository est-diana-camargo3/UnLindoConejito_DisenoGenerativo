#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║                    PINTAR CONEJO PROCEDURAL                   ║
#                         ║              Estilos: PixelArt y Bento Art                   ║
#                         ╚═══════════════════════════════════════════════════════════════╝

import maya.cmds as cmds
import random
import proyectoFinal.crearConejo as crearConejo

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
# MATERIAL DEGRADADO CABEZA → PIES
# =========================================================

def crear_material_degradado(nombre, emocion):

    # =====================================================
    # MATERIAL
    # =====================================================

    material = cmds.shadingNode(
        "blinn",
        asShader=True,
        name=f"{nombre}_{emocion}_MAT"
    )

    sg = cmds.sets(
        renderable=True,
        noSurfaceShader=True,
        empty=True,
        name=f"{material}SG"
    )

    cmds.connectAttr(
        f"{material}.outColor",
        f"{sg}.surfaceShader",
        force=True
    )

    # =====================================================
    # LOOK BRILLANTE
    # =====================================================

    cmds.setAttr(f"{material}.eccentricity", 0.25)
    cmds.setAttr(f"{material}.specularRollOff", 0.4)

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

    # vertical
    cmds.setAttr(f"{ramp}.type", 1)

    # suave
    cmds.setAttr(f"{ramp}.interpolation", 3)

    # =====================================================
    # PALETA
    # =====================================================

    paleta = PALETAS[emocion]

    total_colores = len(paleta)

    for i, (color, porcentaje) in enumerate(paleta):

        posicion = float(i) / float(total_colores - 1)

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

    # =====================================================
    # PROJECTION
    # =====================================================

    projection = cmds.shadingNode(
        "projection",
        asTexture=True,
        name=f"{nombre}_{emocion}_PROJ"
    )

    place3d = cmds.shadingNode(
        "place3dTexture",
        asUtility=True,
        name=f"{nombre}_{emocion}_PLACE3D"
    )

    # conectar projection
    cmds.defaultNavigation(
        connectToExisting=True,
        source=ramp,
        destination=projection
    )

    cmds.connectAttr(
        f"{place3d}.worldInverseMatrix",
        f"{projection}.placementMatrix",
        force=True
    )

    # =====================================================
    # PLANAR
    # =====================================================

    cmds.setAttr(f"{projection}.projType", 1)

    # =====================================================
    # CENTRAR PROYECCIÓN EN EL CONEJO
    # =====================================================

    bbox = cmds.exactWorldBoundingBox(
        crearConejo.piezas_deformables
    )

    xmin, ymin, zmin, xmax, ymax, zmax = bbox

    centro_x = (xmin + xmax) / 2
    centro_y = (ymin + ymax) / 2
    centro_z = (zmin + zmax) / 2

    # mover projection al centro
    cmds.setAttr(f"{place3d}.translateX", centro_x)
    cmds.setAttr(f"{place3d}.translateY", centro_y)
    cmds.setAttr(f"{place3d}.translateZ", centro_z)

    # =====================================================
    # PROYECTAR DESDE EL FRENTE
    # =====================================================

    cmds.setAttr(f"{place3d}.rotateX", 0)
    cmds.setAttr(f"{place3d}.rotateY", 0)
    cmds.setAttr(f"{place3d}.rotateZ", 90)

    # =====================================================
    # ESCALA AUTOMÁTICA SEGÚN MORFOLOGÍA (proporcion)
    # =====================================================

    ancho = xmax - xmin
    alto = ymax - ymin
    profundo = zmax - zmin

    # =====================================================
    # VERTICAL
    # =====================================================

    if crearConejo.morfologia == "vertical":

        cmds.setAttr(f"{place3d}.scaleX", alto * 1.5)
        cmds.setAttr(f"{place3d}.scaleY", ancho * 0.9)
        cmds.setAttr(f"{place3d}.scaleZ", profundo * 1.2)

    # =====================================================
    # ESTÁNDAR - Horizontal
    # =====================================================

    else:

        cmds.setAttr(f"{place3d}.scaleX", alto * 0.5)
        cmds.setAttr(f"{place3d}.scaleY", ancho * 0.50)
        cmds.setAttr(f"{place3d}.scaleZ", profundo * 1.2)




    # =====================================================
    # CONECTAR MATERIAL
    # =====================================================

    cmds.connectAttr(
        f"{projection}.outColor",
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