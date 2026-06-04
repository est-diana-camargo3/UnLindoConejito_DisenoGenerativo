import os
import random

import maya.cmds as cmds


RUTA_PROPS = r"D:\descargas\props"

COLORES_CORAZON_POR_EMOCION = {
    "descanso": (0.15, 0.55, 1.00),
    "feo": (0.08, 0.08, 0.08),
    "pequeno": (1.00, 0.35, 0.70),
    "fantasia": (0.70, 0.20, 1.00),
    "odio": (1.00, 0.00, 0.05),
    "infiel": (1.00, 0.78, 0.05),
    "artificial": (0.45, 0.85, 1.00),
    "verdad": (1.00, 1.00, 1.00),
}

COLOR_ESTRELLA = (0.4117, 0.7629, 1.0)


def _bbox(objetos):
    objetos_validos = [obj for obj in objetos if cmds.objExists(obj)]
    if not objetos_validos:
        return None
    return cmds.exactWorldBoundingBox(objetos_validos)


def _centro_bbox(bbox):
    return (
        (bbox[0] + bbox[3]) / 2,
        (bbox[1] + bbox[4]) / 2,
        (bbox[2] + bbox[5]) / 2,
    )


def _mayor_dimension(bbox):
    return max(
        bbox[3] - bbox[0],
        bbox[4] - bbox[1],
        bbox[5] - bbox[2],
    )


def _mover_centro_bbox(objeto, posicion_objetivo):
    bbox_actual = _bbox([objeto])
    if not bbox_actual:
        return

    centro_actual = _centro_bbox(bbox_actual)
    delta = (
        posicion_objetivo[0] - centro_actual[0],
        posicion_objetivo[1] - centro_actual[1],
        posicion_objetivo[2] - centro_actual[2],
    )

    cmds.move(delta[0], delta[1], delta[2], objeto, relative=True, worldSpace=True)


def _distancia_puntos(a, b):
    return (
        (a[0] - b[0]) ** 2 +
        (a[1] - b[1]) ** 2 +
        (a[2] - b[2]) ** 2
    ) ** 0.5


def _posicion_libre(posicion, radio, posiciones_ocupadas, margen):
    for posicion_ocupada, radio_ocupado in posiciones_ocupadas:
        distancia_minima = radio + radio_ocupado + margen

        if _distancia_puntos(posicion, posicion_ocupada) < distancia_minima:
            return False

    return True


def _centrar_pivote(objeto):
    if not cmds.objExists(objeto):
        return

    try:
        cmds.xform(objeto, centerPivots=True)
    except Exception as e:
        cmds.warning(f"No se pudo centrar el pivote de {objeto}: {e}")


def _importar_fbx(ruta, namespace):
    antes = set(cmds.ls(assemblies=True) or [])

    cmds.file(
        ruta,
        i=True,
        type="FBX",
        ignoreVersion=True,
        ra=True,
        mergeNamespacesOnClash=False,
        namespace=namespace,
        options="fbx",
        preserveReferences=True
    )

    despues = set(cmds.ls(assemblies=True) or [])
    return list(despues - antes)


def _agrupar_importados(importados, nombre_grupo):
    if not importados:
        return None

    grupo = cmds.group(em=True, name=nombre_grupo)

    for obj in importados:
        if cmds.objExists(obj):
            try:
                cmds.parent(obj, grupo)
            except Exception as e:
                cmds.warning(f"No se pudo parentar prop {obj}: {e}")

    return grupo


def _crear_material_openpbr(nombre, color):
    shader = cmds.shadingNode("openPBRSurface", asShader=True, name=nombre)
    shading_group = cmds.sets(
        renderable=True,
        noSurfaceShader=True,
        empty=True,
        name=f"{nombre}_SG"
    )

    cmds.setAttr(
        f"{shader}.baseColor",
        color[0],
        color[1],
        color[2],
        type="double3"
    )
    cmds.connectAttr(
        f"{shader}.outColor",
        f"{shading_group}.surfaceShader",
        force=True
    )

    return shading_group


def _asignar_material_a_grupo(grupo, shading_group):
    if not grupo or not cmds.objExists(grupo):
        return

    meshes = []
    hijos = cmds.listRelatives(grupo, allDescendents=True, type="transform") or []

    for obj in [grupo] + hijos:
        shapes = cmds.listRelatives(obj, shapes=True, type="mesh") or []

        if shapes:
            meshes.append(obj)

    if meshes:
        cmds.sets(meshes, edit=True, forceElement=shading_group)


def _limpiar_props_personaje():
    patrones = [
        "Gafas_Prop_GRP",
        "Gafas_Prop_*",
        "Mono_Prop_GRP",
        "Mono_Prop_*",
        "CuernoB_Prop_GRP",
        "CuernoB_Prop_*",
        "CuernoB_Derecho_Prop_GRP",
        "CuernoB_Izquierdo_Prop_GRP",
        "CuernosB_Prop_GRP",
        "CuernoM_Prop_GRP",
        "CuernoM_Prop_*",
        "CuernoM_Derecho_Prop_GRP",
        "CuernoM_Izquierdo_Prop_GRP",
        "CuernosM_Prop_GRP",
    ]

    for obj in cmds.ls(*patrones) or []:
        if cmds.objExists(obj):
            try:
                cmds.delete(obj)
            except Exception as e:
                cmds.warning(f"No se pudo borrar prop anterior {obj}: {e}")


def importar_corazon():
    ruta_corazon = os.path.join(RUTA_PROPS, "corazon.fbx")

    if not os.path.exists(ruta_corazon):
        cmds.warning(f"No existe el prop corazon: {ruta_corazon}")
        return None

    try:
        if not cmds.pluginInfo("fbxmaya", q=True, loaded=True):
            cmds.loadPlugin("fbxmaya")
    except Exception as e:
        cmds.warning(f"No se pudo cargar el plugin FBX: {e}")

    importados = _importar_fbx(ruta_corazon, "corazon_prop")

    print(f"Prop corazon importado: {ruta_corazon}")
    return importados


def importar_estrella():
    ruta_estrella = os.path.join(RUTA_PROPS, "estrella.fbx")

    if not os.path.exists(ruta_estrella):
        cmds.warning(f"No existe el prop estrella: {ruta_estrella}")
        return None

    try:
        if not cmds.pluginInfo("fbxmaya", q=True, loaded=True):
            cmds.loadPlugin("fbxmaya")
    except Exception as e:
        cmds.warning(f"No se pudo cargar el plugin FBX: {e}")

    importados = _importar_fbx(ruta_estrella, "estrella_prop")

    print(f"Prop estrella importado: {ruta_estrella}")
    return importados


def importar_gafas_cabeza():
    ruta_gafas = os.path.join(RUTA_PROPS, "gafas.fbx")

    if not os.path.exists(ruta_gafas):
        cmds.warning(f"No existe el prop gafas: {ruta_gafas}")
        return None

    bbox_cabeza = _bbox(["Cabeza_Primitiva_001"])

    if not bbox_cabeza:
        cmds.warning("No se encontro la cabeza para ubicar las gafas")
        return None

    try:
        if not cmds.pluginInfo("fbxmaya", q=True, loaded=True):
            cmds.loadPlugin("fbxmaya")
    except Exception as e:
        cmds.warning(f"No se pudo cargar el plugin FBX: {e}")

    for obj in cmds.ls("Gafas_Prop_GRP", "Gafas_Prop_*") or []:
        if cmds.objExists(obj):
            try:
                cmds.delete(obj)
            except Exception as e:
                cmds.warning(f"No se pudo borrar prop anterior {obj}: {e}")

    importados = _importar_fbx(ruta_gafas, "gafas_prop")
    grupo_gafas = _agrupar_importados(importados, "Gafas_Prop_GRP")

    if not grupo_gafas:
        cmds.warning("No se importaron las gafas")
        return None

    _centrar_pivote(grupo_gafas)

    bbox_gafas = _bbox([grupo_gafas])
    ancho_cabeza = bbox_cabeza[3] - bbox_cabeza[0]

    if bbox_gafas and ancho_cabeza > 0:
        ancho_gafas = bbox_gafas[3] - bbox_gafas[0]
        tamano_gafas = _mayor_dimension(bbox_gafas)
        referencia_gafas = ancho_gafas if ancho_gafas > 0 else tamano_gafas

        if referencia_gafas > 0:
            escala = (ancho_cabeza * 0.9) / referencia_gafas
            cmds.scale(escala, escala, escala, grupo_gafas, absolute=True)

    _centrar_pivote(grupo_gafas)

    centro_cabeza = _centro_bbox(bbox_cabeza)
    bbox_gafas = _bbox([grupo_gafas])

    if bbox_gafas:
        mitad_z_gafas = (bbox_gafas[5] - bbox_gafas[2]) / 2
        posicion_gafas = (
            centro_cabeza[0],
            centro_cabeza[1],
            bbox_cabeza[5] - mitad_z_gafas,
        )
        _mover_centro_bbox(grupo_gafas, posicion_gafas)

    _centrar_pivote(grupo_gafas)

    print(f"Prop gafas importado y ubicado en cabeza: {ruta_gafas}")

    try:
        cmds.parent(grupo_gafas, "Cabeza_Primitiva_001", absolute=True)
    except Exception as e:
        cmds.warning(f"No se pudo parentar gafas a cabeza: {e}")

    return grupo_gafas


def importar_mono_torso():
    ruta_mono = os.path.join(RUTA_PROPS, "moño.fbx")

    if not os.path.exists(ruta_mono):
        cmds.warning(f"No existe el prop moño: {ruta_mono}")
        return None

    bbox_torso = _bbox(["Tronco_Primitiva_010"])

    if not bbox_torso:
        cmds.warning("No se encontro el torso para ubicar el moño")
        return None

    try:
        if not cmds.pluginInfo("fbxmaya", q=True, loaded=True):
            cmds.loadPlugin("fbxmaya")
    except Exception as e:
        cmds.warning(f"No se pudo cargar el plugin FBX: {e}")

    for obj in cmds.ls("Mono_Prop_GRP", "Mono_Prop_*") or []:
        if cmds.objExists(obj):
            try:
                cmds.delete(obj)
            except Exception as e:
                cmds.warning(f"No se pudo borrar prop anterior {obj}: {e}")

    importados = _importar_fbx(ruta_mono, "mono_prop")
    grupo_mono = _agrupar_importados(importados, "Mono_Prop_GRP")

    if not grupo_mono:
        cmds.warning("No se importo el moño")
        return None

    _centrar_pivote(grupo_mono)

    bbox_mono = _bbox([grupo_mono])
    ancho_torso = bbox_torso[3] - bbox_torso[0]

    if bbox_mono and ancho_torso > 0:
        ancho_mono = bbox_mono[3] - bbox_mono[0]
        tamano_mono = _mayor_dimension(bbox_mono)
        referencia_mono = ancho_mono if ancho_mono > 0 else tamano_mono

        if referencia_mono > 0:
            escala = (ancho_torso * 0.30) / referencia_mono
            cmds.scale(escala, escala, escala, grupo_mono, absolute=True)

    _centrar_pivote(grupo_mono)

    centro_torso = _centro_bbox(bbox_torso)
    alto_torso = bbox_torso[4] - bbox_torso[1]
    bbox_mono = _bbox([grupo_mono])

    if bbox_mono:
        mitad_z_mono = (bbox_mono[5] - bbox_mono[2]) / 2
        posicion_mono = (
            centro_torso[0],
            bbox_torso[1] + alto_torso * 0.68,
            bbox_torso[5] + mitad_z_mono - ancho_torso * 0.13,
        )
        _mover_centro_bbox(grupo_mono, posicion_mono)

    _centrar_pivote(grupo_mono)

    print(f"Prop moño importado y ubicado en torso: {ruta_mono}")

    try:
        cmds.parent(grupo_mono, "Tronco_Primitiva_010", absolute=True)
    except Exception as e:
        cmds.warning(f"No se pudo parentar moño a torso: {e}")

    return grupo_mono


def importar_cuernoM_cabeza():
    ruta_cuerno = os.path.join(RUTA_PROPS, "cuernoM.fbx")

    if not os.path.exists(ruta_cuerno):
        cmds.warning(f"No existe el prop cuernoM: {ruta_cuerno}")
        return None

    bbox_cabeza = _bbox(["Cabeza_Primitiva_001"])
    bbox_oreja = _bbox(["Oreja_Derecha_007"])

    if not bbox_cabeza:
        cmds.warning("No se encontro la cabeza para ubicar cuernoM")
        return None

    if not bbox_oreja:
        cmds.warning("No se encontro la oreja derecha para ubicar cuernoM")
        return None

    try:
        if not cmds.pluginInfo("fbxmaya", q=True, loaded=True):
            cmds.loadPlugin("fbxmaya")
    except Exception as e:
        cmds.warning(f"No se pudo cargar el plugin FBX: {e}")

    for obj in cmds.ls(
        "CuernoB_Prop_GRP",
        "CuernoB_Prop_*",
        "CuernoB_Derecho_Prop_GRP",
        "CuernoB_Izquierdo_Prop_GRP",
        "CuernosB_Prop_GRP",
        "CuernoM_Prop_GRP",
        "CuernoM_Prop_*",
        "CuernoM_Derecho_Prop_GRP",
        "CuernoM_Izquierdo_Prop_GRP",
        "CuernosM_Prop_GRP"
    ) or []:
        if cmds.objExists(obj):
            try:
                cmds.delete(obj)
            except Exception as e:
                cmds.warning(f"No se pudo borrar prop anterior {obj}: {e}")

    importados = _importar_fbx(ruta_cuerno, "cuernoM_prop")
    grupo_cuerno = _agrupar_importados(importados, "CuernoM_Derecho_Prop_GRP")

    if not grupo_cuerno:
        cmds.warning("No se importo cuernoM")
        return None

    grupo_cuernos = cmds.group(em=True, name="CuernosM_Prop_GRP")
    _centrar_pivote(grupo_cuerno)

    bbox_cuerno = _bbox([grupo_cuerno])
    tamano_cabeza = _mayor_dimension(bbox_cabeza)

    if bbox_cuerno and tamano_cabeza > 0:
        tamano_cuerno = _mayor_dimension(bbox_cuerno)

        if tamano_cuerno > 0:
            escala = (tamano_cabeza * 0.30) / tamano_cuerno
            cmds.scale(escala, escala, escala, grupo_cuerno, absolute=True)

    _centrar_pivote(grupo_cuerno)

    centro_oreja = _centro_bbox(bbox_oreja)
    centro_cabeza = _centro_bbox(bbox_cabeza)
    profundidad_cabeza = bbox_cabeza[5] - bbox_cabeza[2]
    bbox_cuerno = _bbox([grupo_cuerno])

    if bbox_cuerno:
        mitad_y_cuerno = (bbox_cuerno[4] - bbox_cuerno[1]) / 2
        mitad_z_cuerno = (bbox_cuerno[5] - bbox_cuerno[2]) / 2
        posicion_cuerno = (
            centro_oreja[0],
            bbox_cabeza[4] + mitad_y_cuerno*0.45,
            bbox_oreja[5] + mitad_z_cuerno + profundidad_cabeza * 0.04,
        )
        _mover_centro_bbox(grupo_cuerno, posicion_cuerno)

    _centrar_pivote(grupo_cuerno)

    grupo_cuerno_izq = cmds.duplicate(
        grupo_cuerno,
        renameChildren=True,
        name="CuernoM_Izquierdo_Prop_GRP"
    )[0]

    bbox_cuerno_der = _bbox([grupo_cuerno])

    if bbox_cuerno_der:
        centro_cuerno_der = _centro_bbox(bbox_cuerno_der)
        posicion_cuerno_izq = (
            centro_cabeza[0] - (centro_cuerno_der[0] - centro_cabeza[0]),
            centro_cuerno_der[1],
            centro_cuerno_der[2],
        )
        _mover_centro_bbox(grupo_cuerno_izq, posicion_cuerno_izq)

    cmds.scale(
        -1,
        1,
        1,
        grupo_cuerno_izq,
        relative=True,
        objectSpace=True
    )

    _centrar_pivote(grupo_cuerno_izq)

    for cuerno in [grupo_cuerno, grupo_cuerno_izq]:
        try:
            cmds.parent(cuerno, grupo_cuernos)
        except Exception as e:
            cmds.warning(f"No se pudo agrupar cuernoM {cuerno}: {e}")

    print(f"Prop cuernoM importado y ubicado en cabeza: {ruta_cuerno}")

    try:
        cmds.parent(grupo_cuernos, "Cabeza_Primitiva_001", absolute=True)
    except Exception as e:
        cmds.warning(f"No se pudo parentar cuernoM a cabeza: {e}")

    return grupo_cuernos


def _importar_cuernos_cabeza(tipo_cuerno):
    prefijo = "Cuerno" + tipo_cuerno[-1].upper()
    ruta_cuerno = os.path.join(RUTA_PROPS, f"{tipo_cuerno}.fbx")

    if not os.path.exists(ruta_cuerno):
        cmds.warning(f"No existe el prop {tipo_cuerno}: {ruta_cuerno}")
        return None

    bbox_cabeza = _bbox(["Cabeza_Primitiva_001"])
    bbox_oreja = _bbox(["Oreja_Derecha_007"])

    if not bbox_cabeza:
        cmds.warning(f"No se encontro la cabeza para ubicar {tipo_cuerno}")
        return None

    if not bbox_oreja:
        cmds.warning(f"No se encontro la oreja derecha para ubicar {tipo_cuerno}")
        return None

    try:
        if not cmds.pluginInfo("fbxmaya", q=True, loaded=True):
            cmds.loadPlugin("fbxmaya")
    except Exception as e:
        cmds.warning(f"No se pudo cargar el plugin FBX: {e}")

    for obj in cmds.ls(
        "CuernoB_Prop_GRP",
        "CuernoB_Prop_*",
        "CuernoB_Derecho_Prop_GRP",
        "CuernoB_Izquierdo_Prop_GRP",
        "CuernosB_Prop_GRP",
        "CuernoM_Prop_GRP",
        "CuernoM_Prop_*",
        "CuernoM_Derecho_Prop_GRP",
        "CuernoM_Izquierdo_Prop_GRP",
        "CuernosM_Prop_GRP"
    ) or []:
        if cmds.objExists(obj):
            try:
                cmds.delete(obj)
            except Exception as e:
                cmds.warning(f"No se pudo borrar prop anterior {obj}: {e}")

    importados = _importar_fbx(ruta_cuerno, f"{tipo_cuerno}_prop")
    grupo_cuerno = _agrupar_importados(importados, f"{prefijo}_Derecho_Prop_GRP")

    if not grupo_cuerno:
        cmds.warning(f"No se importo {tipo_cuerno}")
        return None

    grupo_cuernos = cmds.group(em=True, name=f"Cuernos{tipo_cuerno[-1].upper()}_Prop_GRP")
    _centrar_pivote(grupo_cuerno)

    bbox_cuerno = _bbox([grupo_cuerno])
    tamano_cabeza = _mayor_dimension(bbox_cabeza)

    if bbox_cuerno and tamano_cabeza > 0:
        tamano_cuerno = _mayor_dimension(bbox_cuerno)

        if tamano_cuerno > 0:
            escala = (tamano_cabeza * 0.30) / tamano_cuerno
            cmds.scale(escala, escala, escala, grupo_cuerno, absolute=True)

    _centrar_pivote(grupo_cuerno)

    centro_oreja = _centro_bbox(bbox_oreja)
    centro_cabeza = _centro_bbox(bbox_cabeza)
    profundidad_cabeza = bbox_cabeza[5] - bbox_cabeza[2]
    bbox_cuerno = _bbox([grupo_cuerno])

    if bbox_cuerno:
        mitad_y_cuerno = (bbox_cuerno[4] - bbox_cuerno[1]) / 2
        mitad_z_cuerno = (bbox_cuerno[5] - bbox_cuerno[2]) / 2
        posicion_cuerno = (
            centro_oreja[0],
            bbox_cabeza[4] + mitad_y_cuerno * 0.45,
            bbox_oreja[5] + mitad_z_cuerno + profundidad_cabeza * 0.04,
        )
        _mover_centro_bbox(grupo_cuerno, posicion_cuerno)

    _centrar_pivote(grupo_cuerno)

    grupo_cuerno_izq = cmds.duplicate(
        grupo_cuerno,
        renameChildren=True,
        name=f"{prefijo}_Izquierdo_Prop_GRP"
    )[0]

    bbox_cuerno_der = _bbox([grupo_cuerno])

    if bbox_cuerno_der:
        centro_cuerno_der = _centro_bbox(bbox_cuerno_der)
        posicion_cuerno_izq = (
            centro_cabeza[0] - (centro_cuerno_der[0] - centro_cabeza[0]),
            centro_cuerno_der[1],
            centro_cuerno_der[2],
        )
        _mover_centro_bbox(grupo_cuerno_izq, posicion_cuerno_izq)

    cmds.scale(
        -1,
        1,
        1,
        grupo_cuerno_izq,
        relative=True,
        objectSpace=True
    )

    _centrar_pivote(grupo_cuerno_izq)

    for cuerno in [grupo_cuerno, grupo_cuerno_izq]:
        try:
            cmds.parent(cuerno, grupo_cuernos)
        except Exception as e:
            cmds.warning(f"No se pudo agrupar {tipo_cuerno} {cuerno}: {e}")

    print(f"Prop {tipo_cuerno} importado y ubicado en cabeza: {ruta_cuerno}")

    try:
        cmds.parent(grupo_cuernos, "Cabeza_Primitiva_001", absolute=True)
    except Exception as e:
        cmds.warning(f"No se pudo parentar {tipo_cuerno} a cabeza: {e}")

    return grupo_cuernos


def importar_cuernoB_cabeza():
    return _importar_cuernos_cabeza("cuernoB")


def importar_cuernoM_cabeza():
    return _importar_cuernos_cabeza("cuernoM")


def importar_prop_aleatorio_personaje():
    _limpiar_props_personaje()

    opciones = [
        ("ninguno", None),
        ("gafas", importar_gafas_cabeza),
        ("mono", importar_mono_torso),
        ("cuernoB", importar_cuernoB_cabeza),
        ("cuernoM", importar_cuernoM_cabeza),
    ]

    nombre, funcion = random.choice(opciones)

    if funcion is None:
        print("Prop aleatorio: ninguno")
        return None

    print(f"Prop aleatorio: {nombre}")
    return funcion()


def importar_corazones_decorativos(piezas_conejo=None, emocion="descanso", minimo=2, maximo=4):
    ruta_corazon = os.path.join(RUTA_PROPS, "corazon.fbx")
    ruta_estrella = os.path.join(RUTA_PROPS, "estrella.fbx")

    if not os.path.exists(ruta_corazon):
        cmds.warning(f"No existe el prop corazon: {ruta_corazon}")
    if not os.path.exists(ruta_estrella):
        cmds.warning(f"No existe el prop estrella: {ruta_estrella}")

    if not os.path.exists(ruta_corazon) and not os.path.exists(ruta_estrella):
        return []

    try:
        if not cmds.pluginInfo("fbxmaya", q=True, loaded=True):
            cmds.loadPlugin("fbxmaya")
    except Exception as e:
        cmds.warning(f"No se pudo cargar el plugin FBX: {e}")

    for obj in cmds.ls(
        "Decorativos_Props_GRP",
        "Corazones_Props_GRP",
        "Corazon_Prop_*",
        "Estrella_Prop_*",
    ) or []:
        if cmds.objExists(obj):
            try:
                cmds.delete(obj)
            except Exception as e:
                cmds.warning(f"No se pudo borrar prop anterior {obj}: {e}")

    piezas_conejo = piezas_conejo or []
    bbox_conejo = _bbox(piezas_conejo)
    bbox_cabeza = _bbox(["Cabeza_Primitiva_001"])

    if not bbox_conejo:
        cmds.warning("No se pudo calcular el espacio del conejo para ubicar props")
        return []

    if not bbox_cabeza:
        bbox_cabeza = bbox_conejo

    centro_conejo = _centro_bbox(bbox_conejo)

    ancho_conejo = bbox_conejo[3] - bbox_conejo[0]
    alto_conejo = bbox_conejo[4] - bbox_conejo[1]
    profundidad_conejo = bbox_conejo[5] - bbox_conejo[2]
    tamano_cabeza = _mayor_dimension(bbox_cabeza)

    cantidad_corazones = random.randint(minimo, maximo) if os.path.exists(ruta_corazon) else 0
    cantidad_estrellas = random.randint(1, 3) if os.path.exists(ruta_estrella) else 0

    grupo_general = cmds.group(em=True, name="Decorativos_Props_GRP")
    decorativos = []
    posiciones_ocupadas = []

    zonas = ["izquierda", "derecha", "detras"]
    color_corazon = COLORES_CORAZON_POR_EMOCION.get(
        emocion,
        (1.0, 0.0, 1.0)
    )

    def crear_grupo_base(ruta, namespace, nombre_grupo):
        importados = _importar_fbx(ruta, namespace)

        if not importados:
            return None

        grupo = cmds.group(em=True, name=nombre_grupo)

        for obj in importados:
            if cmds.objExists(obj):
                padre = cmds.listRelatives(obj, parent=True)
                if not padre:
                    try:
                        cmds.parent(obj, grupo)
                    except Exception:
                        pass

        return grupo

    def crear_copias(grupo_base, prefijo, cantidad):
        if not grupo_base or cantidad <= 0:
            return []

        grupos = [grupo_base]

        for i in range(cantidad - 1):
            duplicado = cmds.duplicate(
                grupo_base,
                renameChildren=True,
                name=f"{prefijo}_{i + 2:02}_GRP"
            )[0]
            grupos.append(duplicado)

        return grupos

    def posicion_decorativa(mitad_x, mitad_y, mitad_z, radio):
        margen = tamano_cabeza * 0.18
        ultima_posicion = centro_conejo

        for intento in range(40):
            zona = random.choice(zonas)
            separacion = random.uniform(tamano_cabeza * 0.35, tamano_cabeza * 1.15)

            if zona == "izquierda":
                x = bbox_conejo[0] - mitad_x - separacion
                z = centro_conejo[2] + random.uniform(-profundidad_conejo * 0.45, profundidad_conejo * 0.45)

            elif zona == "derecha":
                x = bbox_conejo[3] + mitad_x + separacion
                z = centro_conejo[2] + random.uniform(-profundidad_conejo * 0.45, profundidad_conejo * 0.45)

            else:
                x = centro_conejo[0] + random.uniform(-ancho_conejo * 0.45, ancho_conejo * 0.45)
                z = bbox_conejo[2] - mitad_z - separacion

            y_min = bbox_conejo[1] + mitad_y + alto_conejo * 0.05
            y_max = bbox_conejo[4] - mitad_y - alto_conejo * 0.05

            if y_min >= y_max:
                y = centro_conejo[1]
            else:
                y = random.uniform(y_min, y_max)

            posicion = (x, y, z)
            ultima_posicion = posicion

            if _posicion_libre(posicion, radio, posiciones_ocupadas, margen):
                return posicion

        return ultima_posicion

    def preparar_y_ubicar(grupo, tipo):
        bbox_prop = _bbox([grupo])
        mitad_x = tamano_cabeza * 0.25
        mitad_y = tamano_cabeza * 0.25
        mitad_z = tamano_cabeza * 0.25

        if bbox_prop:
            tamano_prop = _mayor_dimension(bbox_prop)

            if tamano_prop > 0:
                escala = (tamano_cabeza * random.uniform(0.45, 0.75)) / tamano_prop
                cmds.scale(escala, escala, escala, grupo, absolute=True)

            bbox_prop = _bbox([grupo])
            if bbox_prop:
                mitad_x = (bbox_prop[3] - bbox_prop[0]) / 2
                mitad_y = (bbox_prop[4] - bbox_prop[1]) / 2
                mitad_z = (bbox_prop[5] - bbox_prop[2]) / 2

        radio = max(mitad_x, mitad_y, mitad_z)
        posicion = posicion_decorativa(mitad_x, mitad_y, mitad_z, radio)

        _mover_centro_bbox(grupo, posicion)

        cmds.rotate(
            random.uniform(-12, 12),
            random.uniform(-25, 25),
            random.uniform(-18, 18),
            grupo,
            relative=True,
            objectSpace=True
        )

        cmds.parent(grupo, grupo_general)
        posiciones_ocupadas.append((posicion, radio))
        decorativos.append(grupo)

    if cantidad_corazones:
        grupo_corazon_base = crear_grupo_base(
            ruta_corazon,
            "corazon_prop_base",
            "Corazon_Prop_01_GRP"
        )
        grupos_corazon = crear_copias(
            grupo_corazon_base,
            "Corazon_Prop",
            cantidad_corazones
        )

        for grupo in grupos_corazon:
            preparar_y_ubicar(grupo, "corazon")

    if cantidad_estrellas:
        grupo_estrella_base = crear_grupo_base(
            ruta_estrella,
            "estrella_prop_base",
            "Estrella_Prop_01_GRP"
        )
        grupos_estrella = crear_copias(
            grupo_estrella_base,
            "Estrella_Prop",
            cantidad_estrellas
        )

        material_estrella = _crear_material_openpbr(
            "Estrella_Azul_MAT",
            COLOR_ESTRELLA
        )

        for grupo in grupos_estrella:
            _asignar_material_a_grupo(grupo, material_estrella)
            preparar_y_ubicar(grupo, "estrella")

    print(
        f"Decorativos importados: {len(decorativos)} "
        f"({cantidad_corazones} corazones, {cantidad_estrellas} estrellas)"
    )
    return decorativos



def _combinar_prop_con_objeto(prop_grupo, objeto_base, nombre_final):
    if not cmds.objExists(prop_grupo) or not cmds.objExists(objeto_base):
        return objeto_base

    padre = cmds.listRelatives(objeto_base, parent=True)

    hijos_mesh = cmds.listRelatives(
        prop_grupo,
        allDescendents=True,
        type="transform"
    ) or []

    meshes_prop = []
    for obj in hijos_mesh:
        shapes = cmds.listRelatives(obj, shapes=True, type="mesh") or []
        if shapes:
            meshes_prop.append(obj)

    if not meshes_prop:
        meshes_prop = [prop_grupo]

    combinado = cmds.polyUnite(
        [objeto_base] + meshes_prop,
        ch=False,
        name=nombre_final + "_COMBINADO"
    )[0]

    cmds.xform(combinado, centerPivots=True)

    if padre:
        cmds.parent(combinado, padre[0])

    if cmds.objExists(prop_grupo):
        cmds.delete(prop_grupo)

    if cmds.objExists(nombre_final):
        cmds.delete(nombre_final)

    combinado = cmds.rename(combinado, nombre_final)

    return combinado
