#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║                    PINTAR CONEJO PROCEDURAL                   ║
#                         ║         Estilos: Degradado procedural +Bento art              ║
#                         ╚═══════════════════════════════════════════════════════════════╝

import maya.cmds as cmds
import maya.mel as mel
import random

import os
import colorsys #colores aleatorios del plano 
import proyectoFinal.crearConejo as crearConejo


ULTIMO_COLOR_OUTLINE = (1, 0, 0.5)

from proyectoFinal.paletas import PALETAS


# =========================================================
# DATOS CURIOSOS
# =========================================================

def generar_dato_curioso(emocion="calma"):

    if emocion == "descanso":
        return "Dato Curioso:\nSi se le regala una piedra de jade a una mujer, esta tendrá buena suerte y descanso."

    elif emocion == "feo":
        return "Dato Curioso:\nEl color mostaza ocre es el color de la cobardía; por eso Judas viste ese color en las películas."

    elif emocion == "pequeno":
        return "Dato Curioso:\nEl rosado pastel es pequeño, pero el rosado saturado es extravagante y se asocia a lo ordinario."

    elif emocion == "fantasia":
        return "Dato Curioso:\nEn la religión católica solo los obispos pueden vestirse de morado, los cardenales de rojo y los párrocos de negro."

    elif emocion == "odio":
        return "Dato Curioso:\nEl color negro transforma la cualidad positiva de un color en negativa; por ejemplo, el rojo es amor, pero con negro es odio."

    elif emocion == "infiel":
        return "Dato Curioso:\nDicen que si un hombre regala rosas amarillas a su pareja es porque fue infiel."

    elif emocion == "artificial":
        return "Dato Curioso:\nEl color lila o morado claro representa la soltería femenina y la frivolidad."

    elif emocion == "verdad":
        return "Dato Curioso:\nNinguna joya, ni siquiera la de 24 kilates, es pura porque el oro puro es blando e inmanejable; todo son aleaciones."

    return "Dato Curioso:\nEste conejo guarda un detalle especial según la emoción seleccionada."


# =========================================================
# MATERIAL BASE NEGRA BRILLANTE
# =========================================================
def pintar_cilindro_base(
        color1=None,
        color2=None):

    base = crearConejo.base_conejo

    if not base or not cmds.objExists(base):
        print("No existe la base")
        return None

    material, sg = _crear_ai_shader("Base_Metal_Rampa_MAT")

    _configurar_shader_por_tipo(
        material,
        "metal",
        [color1, color2]
    )

    ramp = cmds.shadingNode(
        "ramp",
        asTexture=True,
        name="Base_Metal_Rampa"
    )

    cmds.setAttr(f"{ramp}.type", 0)
    cmds.setAttr(f"{ramp}.interpolation", 3)

    cmds.setAttr(f"{ramp}.colorEntryList[0].position", 0)
    cmds.setAttr(
        f"{ramp}.colorEntryList[0].color",
        *color1,
        type="double3"
    )

    cmds.setAttr(f"{ramp}.colorEntryList[1].position", 1)
    cmds.setAttr(
        f"{ramp}.colorEntryList[1].color",
        *color2,
        type="double3"
    )

    cmds.connectAttr(
        f"{ramp}.outColor",
        f"{material}.baseColor",
        force=True
    )

    cmds.sets(
        base,
        edit=True,
        forceElement=sg
    )

    return material, sg

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
# MATERIAL DEGRADADO CABEZA → PIES
# =========================================================
#nos basamos en el estilo bento que consiste en dividir todo en caja , en nuestro caso "caras" y pintar caras o cajas contiguas 
# nosotros quisimos hacerlo con degradado para una transicion mas suave 
def _set_attr_si_existe(nodo, atributo, *valores, **kwargs):
    if cmds.attributeQuery(atributo, node=nodo, exists=True):
        cmds.setAttr(f"{nodo}.{atributo}", *valores, **kwargs)


def _crear_ai_shader(nombre):
    shader = cmds.shadingNode(
        "aiStandardSurface",
        asShader=True,
        name=nombre
    )

    sg = cmds.sets(
        renderable=True,
        noSurfaceShader=True,
        empty=True,
        name=nombre + "SG"
    )

    cmds.connectAttr(
        f"{shader}.outColor",
        f"{sg}.surfaceShader",
        force=True
    )

    return shader, sg



# =========================================================
# PINTAR CARA POR EMOCION
# =========================================================

COLORES_CARA_POR_EMOCION = {
    "descanso": (0.05, 0.20, 0.35),
    "feo": (0.03, 0.03, 0.03),
    "pequeno": (1.00, 0.55, 0.78),
    "fantasia": (0.10, 0.30, 0.70),
    "odio": (0.00, 0.00, 0.00),
    "infiel": (0.95, 0.62, 0.05),
    "artificial": (0.30, 0.40, 0.60),
    "verdad": (1.00, 1.00, 1.00)
}

def crear_material_color_plano(nombre, color):
    material, sg = _crear_ai_shader(nombre)

    cmds.setAttr(
        f"{material}.baseColor",
        color[0],
        color[1],
        color[2],
        type="double3"
    )

    _set_attr_si_existe(material, "specularRoughness", 0.25)
    _set_attr_si_existe(material, "coat", 0.15)

    return material, sg


def pintar_cara_por_emocion(emocion="descanso"):
    color_cara = COLORES_CARA_POR_EMOCION.get(
        emocion,
        COLORES_CARA_POR_EMOCION["descanso"]
    )

    ojos = []
    boca = []

    if len(crearConejo.cara) >= 3:
        ojos = [
            crearConejo.cara[1],  # ojo derecho
            crearConejo.cara[2]   # ojo izquierdo
        ]

    if len(crearConejo.cara) >= 4:
        boca.append(crearConejo.cara[3])  # por ahora usa la nariz como boca/color de expresion

    objetos_boca = cmds.ls("*Boca*", type="transform") or []
    boca += objetos_boca

    ojos = [
        objeto
        for objeto in ojos
        if objeto and cmds.objExists(objeto)
    ]

    boca = [
        objeto
        for objeto in boca
        if objeto and cmds.objExists(objeto)
    ]

    
    if ojos or boca:
        material_cara, sg_cara = crear_material_color_plano(
            f"Cara_{emocion}_MAT",
            color_cara
        )

        cmds.sets(
            ojos + boca,
            edit=True,
            forceElement=sg_cara
        )
    else:
        cmds.warning("No hay ojos ni boca/nariz para pintar")

    print(f"Cara pintada para emocion: {emocion}")



def _colores_desde_paleta(emocion):
    paleta = PALETAS.get(emocion, PALETAS["descanso"])[:]
    random.shuffle(paleta)

    cantidad_ramp = random.choice([2, 3])
    cantidad_ramp = min(cantidad_ramp, len(paleta))

    colores_ramp = [color for color, porcentaje in paleta[:cantidad_ramp]]
    sobrantes = [color for color, porcentaje in paleta[cantidad_ramp:]]

    if not sobrantes:
        sobrantes = colores_ramp[:]

    return colores_ramp, sobrantes


def _configurar_ramp_por_emocion(ramp, emocion):
    tipo_ramp = 0
    noise = 0
    noise_freq = 0
    vwave = 0

    if emocion == "odio":
        tipo_ramp = random.choice([1, 7, 8])

    elif emocion in ["feo", "fantasia"]:
        tipo_ramp = 4

    elif emocion == "verdad":
        tipo_ramp = 0
        noise = random.uniform(0.0, 1.0)
        noise_freq = random.uniform(0.0, 8.0)
        vwave = random.uniform(0.0, 1.0)

    elif emocion == "artificial":
        tipo_ramp = 0
        noise = random.uniform(0.0, 0.3)
        noise_freq = random.uniform(0.0, 1.0)
        vwave = random.uniform(0.0, 1.0)

    cmds.setAttr(f"{ramp}.type", tipo_ramp)
    cmds.setAttr(f"{ramp}.interpolation", 3)
    cmds.setAttr(f"{ramp}.noise", noise)
    cmds.setAttr(f"{ramp}.noiseFreq", noise_freq)
    cmds.setAttr(f"{ramp}.vWave", vwave)

    return tipo_ramp


def _elegir_tipo_shader(emocion):
     
    if emocion in ["verdad", "odio"]:
        return "metal"

    if emocion in ["artificial"]:
        return "cristal"
    
    if emocion == "descanso":
        return random.choice(["color"])
    
    if emocion == "fantasia":
        return random.choice(["metal", "cristal"])

    return "color"


def _configurar_shader_por_tipo(shader, tipo_shader, colores_sobrantes):
    color_extra = colores_sobrantes[0]
    color_extra_2 = colores_sobrantes[1] if len(colores_sobrantes) > 1 else color_extra

    if tipo_shader == "metal":
        _set_attr_si_existe(shader, "metalness", 0.9)
        _set_attr_si_existe(shader, "specularRoughness", random.uniform(0.05, 0.5))
        _set_attr_si_existe(shader, "specularColor", *color_extra, type="double3")
        _set_attr_si_existe(shader, "coat", random.uniform(0.0, 0.25))
        _set_attr_si_existe(shader, "coatColor", *color_extra_2, type="double3")

    elif tipo_shader == "cristal":
        _set_attr_si_existe(shader, "base", 0.20)
        _set_attr_si_existe(shader, "transmission", 0.80)
        _set_attr_si_existe(shader, "transmissionColor", *color_extra, type="double3")
        _set_attr_si_existe(shader, "specularRoughness", random.uniform(0.02, 0.12))
        _set_attr_si_existe(shader, "coat", random.uniform(0.1, 0.35))
        _set_attr_si_existe(shader, "coatColor", *color_extra_2, type="double3")

    else:
        _set_attr_si_existe(shader, "specularRoughness", random.uniform(0.02, 0.18))
        _set_attr_si_existe(shader, "specularColor", *color_extra, type="double3")
        _set_attr_si_existe(shader, "coat", random.uniform(0.25, 0.65))
        _set_attr_si_existe(shader, "coatColor", *color_extra_2, type="double3")


def _ruta_textura(nombre_textura):
    ruta = os.path.join(
        os.path.dirname(__file__),
        "textures",
        nombre_textura + ".jpg"
    )

    if os.path.exists(ruta):
        return ruta.replace("\\", "/")

    return None


def _elegir_textura_para_material(tipo_shader):
    if tipo_shader == "color":
        preferidas = ["fieltro", "tejido", "pasto"]
    else:
        preferidas = ["glaceado", "nieve"]

    disponibles = []

    for nombre in preferidas:
        ruta = _ruta_textura(nombre)
        if ruta:
            disponibles.append(ruta)

    if not disponibles:
        for nombre in ["fieltro", "tejido", "nieve", "glaceado", "pasto"]:
            ruta = _ruta_textura(nombre)
            if ruta:
                disponibles.append(ruta)

    if disponibles and random.random() < 0.65:
        return random.choice(disponibles)

    return None


def _conectar_bump(shader, ruta, intensidad=0.12):
    file_node = cmds.shadingNode(
        "file",
        asTexture=True,
        isColorManaged=True,
        name="Conejo_bump_file"
    )

    place2d = cmds.shadingNode(
        "place2dTexture",
        asUtility=True,
        name="Conejo_bump_place2d"
    )

    cmds.connectAttr(f"{place2d}.outUV", f"{file_node}.uvCoord", force=True)
    cmds.connectAttr(f"{place2d}.outUvFilterSize", f"{file_node}.uvFilterSize", force=True)

    bump = cmds.shadingNode(
        "bump2d",
        asUtility=True,
        name="Conejo_bump"
    )

    cmds.setAttr(f"{file_node}.fileTextureName", ruta, type="string")
    cmds.setAttr(f"{file_node}.colorSpace", "Raw", type="string")
    cmds.setAttr(f"{bump}.bumpDepth", intensidad)

    cmds.connectAttr(f"{file_node}.outColorR", f"{bump}.bumpValue", force=True)
    cmds.connectAttr(f"{bump}.outNormal", f"{shader}.normalCamera", force=True)

    return bump


def _conectar_displacement(objetos, sg, ruta, altura=0.08):
    file_node = cmds.shadingNode(
        "file",
        asTexture=True,
        isColorManaged=True,
        name="Conejo_displacement_file"
    )

    cmds.setAttr(f"{file_node}.fileTextureName", ruta, type="string")
    cmds.setAttr(f"{file_node}.colorSpace", "Raw", type="string")

    displacement = cmds.shadingNode(
        "displacementShader",
        asShader=True,
        name="Conejo_displacement"
    )

    multiply = cmds.shadingNode(
        "multiplyDivide",
        asUtility=True,
        name="Conejo_displacement_altura"
    )

    cmds.setAttr(f"{multiply}.input2X", altura)
    cmds.connectAttr(f"{file_node}.outColorR", f"{multiply}.input1X", force=True)
    cmds.connectAttr(f"{multiply}.outputX", f"{displacement}.displacement", force=True)
    cmds.connectAttr(f"{displacement}.displacement", f"{sg}.displacementShader", force=True)

    for objeto in objetos:
        if not cmds.objExists(objeto):
            continue

        shapes = cmds.listRelatives(objeto, shapes=True) or []

        for shape in shapes:
            if cmds.attributeQuery("aiSubdivType", node=shape, exists=True):
                cmds.setAttr(f"{shape}.aiSubdivType", 1)

            if cmds.attributeQuery("aiSubdivIterations", node=shape, exists=True):
                cmds.setAttr(f"{shape}.aiSubdivIterations", 2)

            if cmds.attributeQuery("aiDispHeight", node=shape, exists=True):
                cmds.setAttr(f"{shape}.aiDispHeight", altura)

            if cmds.attributeQuery("aiDispPadding", node=shape, exists=True):
                cmds.setAttr(f"{shape}.aiDispPadding", altura)

    return displacement






#===========================================================================
#                 CREAR PROFILE LINE
#===========================================================================


def crear_outline(
        objeto,
        grosor=0.5,
        color_borde=(0, 0, 0),
        color_perfil=(1, 0, 0.5),
        convertir_a_poly=False):

    if not cmds.objExists(objeto):
        cmds.warning(f"No existe {objeto}")
        return None

    cmds.select(objeto, r=True)

    antes = set(cmds.ls(type="pfxToon"))

    mel.eval("assignNewPfxToon;")

    despues = set(cmds.ls(type="pfxToon"))
    nuevos = list(despues - antes)

    if not nuevos:
        cmds.warning("No se pudo crear el pfxToon")
        return None

    toon_shape = nuevos[0]
    toon_transform = cmds.listRelatives(
        toon_shape,
        parent=True
    )[0]

    cmds.setAttr(f"{toon_shape}.lineWidth", grosor)

    cmds.setAttr(
        f"{toon_shape}.borderColor",
        color_borde[0],
        color_borde[1],
        color_borde[2],
        type="double3"
    )

    cmds.setAttr(
        f"{toon_shape}.profileColor",
        color_perfil[0],
        color_perfil[1],
        color_perfil[2],
        type="double3"
    )

    if convertir_a_poly:
        cmds.select(toon_transform, r=True)

        try:
            mel.eval("doPaintEffectsToPoly(1,0,0,1,100000);")
        except Exception as e:
            cmds.warning(f"No se pudo convertir el toon a poligonos: {e}")

    return toon_transform


def aplicar_outline_conejo(color_outline=None):
    color = color_outline or ULTIMO_COLOR_OUTLINE
    piezas_outline = []

    for pieza in crearConejo.piezas_deformables:
        if pieza not in piezas_outline:
            piezas_outline.append(pieza)

    if "Cabeza_Primitiva_001" in piezas_outline:
        piezas_outline.remove("Cabeza_Primitiva_001")

    piezas_outline.append("Cabeza_Primitiva_001")

    for pieza in piezas_outline:
        if cmds.objExists(pieza):
            crear_outline(
                objeto=pieza,
                grosor=0.5,
                color_borde=color,
                color_perfil=color,
                convertir_a_poly=False
            )
# =========================================================
# MATERIAL DEGRADADO CABEZA -> PIES
# =========================================================
def crear_material_degradado(nombre, emocion):
    global ULTIMO_COLOR_OUTLINE

    tipo_shader = _elegir_tipo_shader(emocion)
    colores_ramp, colores_sobrantes = _colores_desde_paleta(emocion)

    material, sg = _crear_ai_shader(f"{nombre}_{emocion}_{tipo_shader}_MAT")

    _configurar_shader_por_tipo(
        material,
        tipo_shader,
        colores_sobrantes
    )

    ramp = cmds.shadingNode(
        "ramp",
        asTexture=True,
        name=f"{nombre}_{emocion}_RAMP"
    )

    _configurar_ramp_por_emocion(ramp, emocion)

    for i, color in enumerate(colores_ramp):
        if len(colores_ramp) == 1:
            posicion = 0.5
        else:
            posicion = float(i) / float(len(colores_ramp) - 1)

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

    cmds.setAttr(f"{place3d}.visibility", 0)

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

    cmds.setAttr(f"{projection}.projType", 1)

    bbox = cmds.exactWorldBoundingBox(
        crearConejo.piezas_deformables
    )

    xmin, ymin, zmin, xmax, ymax, zmax = bbox

    centro_x = (xmin + xmax) / 2
    centro_y = (ymin + ymax) / 2
    centro_z = (zmin + zmax) / 2

    cmds.setAttr(f"{place3d}.translateX", centro_x)
    cmds.setAttr(f"{place3d}.translateY", centro_y)
    cmds.setAttr(f"{place3d}.translateZ", centro_z)

    cmds.setAttr(f"{place3d}.rotateX", 0)
    cmds.setAttr(f"{place3d}.rotateY", 0)
    cmds.setAttr(f"{place3d}.rotateZ", 90)

    ancho = xmax - xmin
    alto = ymax - ymin
    profundo = zmax - zmin

    if crearConejo.morfologia == "vertical":
        cmds.setAttr(f"{place3d}.scaleX", alto * 1.5)
        cmds.setAttr(f"{place3d}.scaleY", ancho * 0.9)
        cmds.setAttr(f"{place3d}.scaleZ", profundo * 1.2)

    else:
        cmds.setAttr(f"{place3d}.scaleX", alto * 0.5)
        cmds.setAttr(f"{place3d}.scaleY", ancho * 0.50)
        cmds.setAttr(f"{place3d}.scaleZ", profundo * 1.2)

    cmds.connectAttr(
        f"{projection}.outColor",
        f"{material}.baseColor",
        force=True
    )

    if tipo_shader == "cristal" and cmds.attributeQuery("transmissionColor", node=material, exists=True):
        cmds.connectAttr(
            f"{projection}.outColor",
            f"{material}.transmissionColor",
            force=True
        )

    textura = _elegir_textura_para_material(tipo_shader)

    if textura:
        _conectar_bump(
            material,
            textura,
            intensidad=random.uniform(0.06, 0.16)
        )

        _conectar_displacement(
            crearConejo.piezas_deformables,
            sg,
            textura,
            altura=random.uniform(0.03, 0.10)
        )

    ULTIMO_COLOR_OUTLINE = colores_sobrantes[-1]

    pintar_cilindro_base(
        color1=(0.4, 0.6, 1),
        color2=(0.9, 0.7, 0.9)
    )

    print(f"Material conejo: {tipo_shader} | textura: {textura if textura else 'sin bump/displacement'}")

    return material


