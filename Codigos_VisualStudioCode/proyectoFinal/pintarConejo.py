#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║                    PINTAR CONEJO PROCEDURAL                   ║
#                         ║         Estilos: Degradado procedural +Bento art              ║
#                         ╚═══════════════════════════════════════════════════════════════╝

import maya.cmds as cmds
import random
import colorsys #colores aleatorios del plano 
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
# MATERIAL BASE NEGRA BRILLANTE
# =========================================================
def pintar_cilindro_base():

    # verificar que exista la base
    if not cmds.objExists("Base_Conejo"):
        print("⚠️ No existe la base")
        return

    # =====================================================
    # CREAR MATERIAL
    # =====================================================

    material = cmds.shadingNode(
        "blinn",
        asShader=True,
        name="Base_Negra_MAT"
    )

    sg = cmds.sets(
        renderable=True,
        noSurfaceShader=True,
        empty=True,
        name="Base_Negra_MATSG"
    )

    cmds.connectAttr(
        f"{material}.outColor",
        f"{sg}.surfaceShader",
        force=True
    )



    # =====================================================
    # Color y BRILLO
    # =====================================================
    cmds.setAttr( f"{material}.color", 0.05, 0.05, 0.05, type="double3" )     # COLOR NEGRO
    
    #brillo
    cmds.setAttr(f"{material}.eccentricity", 0.18)
    cmds.setAttr(f"{material}.specularRollOff", 0.8)
    cmds.setAttr( f"{material}.specularColor", 1,1,1, type="double3"  )

    # =====================================================
    # ASIGNAR A BASE
    # =====================================================

    cmds.select("Base_Conejo")

    cmds.hyperShade(assign=material)

    print("✅ Base pintada")



# =========================================================
# COLOR CON SATURACIÓN VARIABLE
# =========================================================
def variar_saturacion(color):

    r, g, b = color

    # RGB → HSV
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    # saturación aleatoria 40%–60%
    nueva_s = random.uniform(0.4, 0.6)

    # HSV → RGB
    nuevo_r, nuevo_g, nuevo_b = colorsys.hsv_to_rgb(
        h,
        nueva_s,
        v
    )
    return (nuevo_r, nuevo_g, nuevo_b)

# =========================================================
# PINTAR PLANO DE FONDO
# =========================================================

def pintar_plano_fondo(emocion):
    # se pinta con uno de los colores de la paleta de la emocion seleccionada 
    # pero desaturado al 60%

    if not cmds.objExists("Plano_Fondo"):
        return

    # color random de la paleta
    color_original, porcentaje = random.choice(
        PALETAS[emocion]
    )

    # variar saturación
    color_final = variar_saturacion(color_original)

    material = cmds.shadingNode(
        "lambert",
        asShader=True,
        name="Plano_Fondo_MAT"
    )

    sg = cmds.sets(
        renderable=True,
        noSurfaceShader=True,
        empty=True,
        name="Plano_Fondo_MATSG"
    )

    cmds.connectAttr(
        f"{material}.outColor",
        f"{sg}.surfaceShader",
        force=True
    )

    cmds.setAttr(
        f"{material}.color",
        color_final[0]+0.6,
        color_final[1]+0.6,
        color_final[2]+0.6,
        type="double3"
    )

    cmds.select("Plano_Fondo")

    cmds.hyperShade(assign=material)

    print("✅ Plano pintado")


# =========================================================
# MATERIAL DEGRADADO CABEZA → PIES
# =========================================================
#nos basamos en el estilo bento que consiste en dividir todo en caja , en nuestro caso "caras" y pintar caras o cajas contiguas 
# nosotros quisimos hacerlo con degradado para una transicion mas suave 
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

    paleta = PALETAS[emocion][:]

    # mezclar orden cada vez
    random.shuffle(paleta)

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

    # ocultar cuadrito del projection osea el cuadrito del degradado
    cmds.setAttr(f"{place3d}.visibility", 0)

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

    
    pintar_cilindro_base()
    pintar_plano_fondo(emocion)
    return material





