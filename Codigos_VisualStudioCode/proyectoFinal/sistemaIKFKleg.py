import math

import maya.cmds as cmds



def obtener_tamano_mesh(meshes, factor=0):

    bbox = cmds.exactWorldBoundingBox(meshes)

    width = bbox[3] - bbox[0]
    height = bbox[4] - bbox[1]
    depth = bbox[5] - bbox[2]

    # diagonal 3D (lo más estable)
    diagonal = math.sqrt(width**2 + height**2 + depth**2)

    return diagonal * factor


def _restar_vectores(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def _sumar_vectores(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def _multiplicar_vector(v, factor):
    return [v[0] * factor, v[1] * factor, v[2] * factor]


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _normalizar(v):
    largo = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)

    if largo < 0.0001:
        return [0, 0, 1]

    return [v[0] / largo, v[1] / largo, v[2] / largo]


def _posicion_pole_vector(inicio, medio, fin, distancia, prefijo):
    p_inicio = cmds.xform(inicio, q=True, ws=True, t=True)
    p_medio = cmds.xform(medio, q=True, ws=True, t=True)
    p_fin = cmds.xform(fin, q=True, ws=True, t=True)

    linea = _restar_vectores(p_fin, p_inicio)
    medio_vec = _restar_vectores(p_medio, p_inicio)
    linea_len_sq = max(_dot(linea, linea), 0.0001)
    proyeccion = _multiplicar_vector(linea, _dot(medio_vec, linea) / linea_len_sq)
    punto_en_linea = _sumar_vectores(p_inicio, proyeccion)
    direccion = _normalizar(_restar_vectores(p_medio, punto_en_linea))

    if prefijo.startswith("Oreja"):
        direccion = [0, 0, 1]

    return _sumar_vectores(p_medio, _multiplicar_vector(direccion, distancia))

def crear_sistema_ikfk(fk_chain,ik_chain,main_chain,meshes,prefix,joint_attr,pv_offset=5):

# =========================
    # CALCULAR TAMAÑO
    # =========================
    tamano = obtener_tamano_mesh(meshes, factor=0.3)

    # =========================
    # FK CONTROLS
    # =========================

    fk_controls = []

    for i, jnt in enumerate(fk_chain[:-1]):

        ctrl, offset = crear_control(
            f"{prefix}_FK_CTRL_{i+1:03}",
            jnt,
            size=tamano
        )

        cmds.parentConstraint(ctrl, jnt, mo=True)

        fk_controls.append(ctrl)
    # jerarquía FK
    for i in range(1, len(fk_controls)):
        cmds.parent(
            f"{fk_controls[i]}_OFFSET",
            fk_controls[i-1]
        )
    

    proxy_fk = crear_proxy_fk_locator(
        prefix=prefix,
        fk_chain=fk_chain,
        fk_controls=fk_controls,
        size=tamano * 0.5,
        color=17
    )
        
    # =========================
    # IK HANDLE
    # =========================
    ik_handle, effector = cmds.ikHandle(sj=ik_chain[0],ee=ik_chain[-1],
        solver="ikRPsolver"
    )
    ik_handle = cmds.rename(ik_handle,f"{prefix}_IKHandle_001")

    # =========================
    # IK CONTROL
    # =========================

    ik_ctrl, ik_root, ik_auto = crear_ik_control(
        f"{prefix}_IK_CTRL_001",
        ik_handle,
        ik_chain[-1],
        size=tamano 
    )


    # =========================
    # POLE VECTOR
    # =========================

    pv_ctrl, pv_root, pv_auto = crear_pv_control(
        f"{prefix}_PV_CTRL_001",
        ik_chain[1],
        ik_handle,
        size=tamano * 0.7,
        pv_offset=pv_offset,
        ik_chain=ik_chain,
        meshes=meshes,
        prefix=prefix
    )

    # =========================
    # CONSTRAINTS FK IK -> MAIN
    # =========================
    constraints = []

    for fk, ik, main in zip(fk_chain[:-1],ik_chain[:-1],main_chain[:-1]):

        c = cmds.orientConstraint(fk,ik,main,mo=False)[0]
        constraints.append(c)

    # =========================
    # FKIK ATTRIBUTE
    # =========================
    if not cmds.attributeQuery("FKIK", node=ik_ctrl, exists=True):

        cmds.addAttr(
            ik_ctrl,
            longName="FKIK",
            attributeType='double',
            min=0,
            max=1,
            defaultValue=0,
            keyable=True
        )

    shape = ik_ctrl

    # =========================
    # REVERSE NODE
    # =========================
    reverse = cmds.shadingNode('reverse', asUtility=True,n=f"{prefix}_FKIK_reverse")
    cmds.connectAttr(f"{shape}.FKIK",f"{reverse}.inputX")

    # =========================
    # SQUASH STRETCH DE EXTREMIDAD 
    # =========================

    # =========================
    # CONEXIONES
    # =========================
    for c in constraints:

        weights = cmds.orientConstraint(c,q=True,weightAliasList=True)
        # FK
        cmds.connectAttr(f"{reverse}.outputX",f"{c}.{weights[0]}",force=True)
        # IK
        cmds.connectAttr(f"{shape}.FKIK",f"{c}.{weights[1]}",force=True)

    print(f"✅ Sistema IKFK creado -> {prefix}")

    # =========================
    # VISIBILIDAD FK / IK
    # =========================

    # FK visibles cuando FKIK = 0.
    # El control interno/base queda oculto porque lo maneja el proxy.
    for i, ctrl in enumerate(fk_controls):

        if i == 0:
            # No ocultar el transform, porque sus hijos FK dependen de el.
            # Solo ocultamos la curva/shape visible del control interno.
            shapes = cmds.listRelatives(ctrl, shapes=True) or []
            for shape_ctrl in shapes:
                cmds.setAttr(f"{shape_ctrl}.visibility", 0)
            continue

        cmds.connectAttr(
            f"{reverse}.outputX",
            f"{ctrl}.visibility",
            force=True
        )

    # Proxy visible solo en FK
    if proxy_fk:
        cmds.connectAttr(
            f"{reverse}.outputX",
            f"{proxy_fk['offset']}.visibility",
            force=True
        )

    # IK visibles cuando FKIK = 1
    cmds.connectAttr(
        f"{shape}.FKIK",
        f"{ik_ctrl}.visibility",
        force=True
    )

    # Pole Vector visible en IK
    cmds.connectAttr(
        f"{shape}.FKIK",
        f"{pv_ctrl}.visibility",
        force=True
    )

    return {
        "ikHandle": ik_handle,
        "ikControl": ik_ctrl,
        "poleVector": pv_ctrl,
        "proxyFK": proxy_fk,
        "attrShape": shape,
        "constraints": constraints
    }


def cambiar_fkik_leg(valor):

    controles_fkik = []

    # buscar todos los transforms
    transforms = cmds.ls(type="transform")

    for obj in transforms:

        if cmds.attributeQuery("FKIK", node=obj, exists=True):
            controles_fkik.append(obj)

    if not controles_fkik:
        cmds.warning("No se encontraron controles FKIK")
        return

    # cambiar todos
    for ctrl in controles_fkik:

        try:
            cmds.setAttr(f"{ctrl}.FKIK", valor)
            print(f"FKIK cambiado a {valor} en {ctrl}")

        except:
            cmds.warning(f"No se pudo cambiar FKIK en {ctrl}")

def bind_skin_cube(mesh, joints):

    # =========================
    # 1. SUBDIVISIÓN DEL MESH
    # =========================
    # Suavizado aplicado en el rig FKIK. Esta intensidad es la que
    # queremos replicar en suavizar_geometria_de_conejo().
    #cmds.polySmooth(mesh, divisions=2)

    # =========================
    # 2. LIMPIEZA BASE
    # =========================
    cmds.makeIdentity(mesh, apply=True, t=True, r=True, s=True, n=False)

    cmds.delete(mesh, ch=True)

    # =========================
    # 3. SMOOTH BIND
    # =========================
    skin = cmds.skinCluster(
        joints,
        mesh,
        toSelectedBones=True,
        bindMethod=0,        # Closest Distance (estable)
        skinMethod=0,        # Linear
        normalizeWeights=1,
        maximumInfluences=3,
        dropoffRate=4.0
    )[0]

    # =========================
    # 4. MEJORA DE DEFORMACIÓN (OPCIONAL PERO RECOMENDADO)
    # =========================
    try:
        cmds.deformer(mesh, type="deltaMush")
        cmds.deltaMush(mesh,
            smoothingIterations=10,
            smoothingStep=0.5,
            pinBorderVertices=1
        )
    except:
        cmds.warning("Delta Mush no disponible o falló")

    # =========================
    # 5. LIMPIEZA FINAL
    # =========================
    cmds.select(clear=True)

    return skin


def distancia_entre(a, b):

    p1 = cmds.xform(a, q=True, ws=True, t=True)
    p2 = cmds.xform(b, q=True, ws=True, t=True)

    return math.sqrt(
        (p2[0]-p1[0])**2 +
        (p2[1]-p1[1])**2 +
        (p2[2]-p1[2])**2
    )


def crear_squash_extremidad(prefix, ik_ctrl, mesh, ik_chain):
    if not cmds.objExists(mesh):
        cmds.warning(f"No existe mesh para squash: {mesh}")
        return None

    config = {
        "BrazoR":  {"axis": "X", "rotateZ": -90, "mult":  0.05},
        "BrazoL":  {"axis": "X", "rotateZ": -90, "mult": -0.05},

        "PiernaR": {"axis": "Y", "mult": -0.05},
        "PiernaL": {"axis": "Y", "mult": -0.05},

        "OrejaR":  {"axis": "Y", "mult":  0.05},
        "OrejaL":  {"axis": "Y", "mult":  0.05},

        "Cola":    {"axis": "Z", "rotateX": 90, "mult": -0.05},
    }

    cfg = config.get(prefix)
    if not cfg:
        cmds.warning(f"No hay configuracion squash para {prefix}")
        return None

    for obj in cmds.ls(f"{prefix}_squash*") or []:
        if cmds.objExists(obj):
            try:
                cmds.delete(obj)
            except:
                pass

    cmds.select(f"{mesh}.vtx[*]", replace=True)

    squash_def, squash_handle = cmds.nonLinear(
        type="squash",
        n=f"{prefix}_squash"
    )

    bbox = cmds.exactWorldBoundingBox(mesh)

    centro_x = (bbox[0] + bbox[3]) / 2
    centro_y = (bbox[1] + bbox[4]) / 2
    centro_z = (bbox[2] + bbox[5]) / 2

    largo_x = bbox[3] - bbox[0]
    largo_y = bbox[4] - bbox[1]
    largo_z = bbox[5] - bbox[2]

    mayor_largo = max(largo_x, largo_y, largo_z)

    # Centrado: mas estable para brazos, piernas, orejas y cola.
    cmds.xform(
        squash_handle,
        ws=True,
        t=(centro_x, centro_y, centro_z)
    )

    if "rotateX" in cfg:
        cmds.setAttr(f"{squash_handle}.rotateX", cfg["rotateX"])
    if "rotateY" in cfg:
        cmds.setAttr(f"{squash_handle}.rotateY", cfg["rotateY"])
    if "rotateZ" in cfg:
        cmds.setAttr(f"{squash_handle}.rotateZ", cfg["rotateZ"])

    cmds.setAttr(f"{squash_handle}.scaleX", 1)
    cmds.setAttr(f"{squash_handle}.scaleY", mayor_largo)
    cmds.setAttr(f"{squash_handle}.scaleZ", 1)

    # Bounds completos para que toda la malla quede dentro del deformer.
    cmds.setAttr(f"{squash_def}.lowBound", -0.55)
    cmds.setAttr(f"{squash_def}.highBound", 0.75)
    cmds.setAttr(f"{squash_def}.factor", 0)

    start_attr = "SquashStart"
    if not cmds.attributeQuery(start_attr, node=ik_ctrl, exists=True):
        cmds.addAttr(
            ik_ctrl,
            longName=start_attr,
            attributeType="double",
            min=-1,
            max=0.5,
            defaultValue=-0.45,
            keyable=True
        )

    cmds.connectAttr(
        f"{ik_ctrl}.{start_attr}",
        f"{squash_def}.lowBound",
        force=True
    )

    end_attr = "SquashEnd"
    if not cmds.attributeQuery(end_attr, node=ik_ctrl, exists=True):
        cmds.addAttr(
            ik_ctrl,
            longName=end_attr,
            attributeType="double",
            min=-0.5,
            max=1,
            defaultValue=0.75,
            keyable=True
        )

    cmds.connectAttr(
        f"{ik_ctrl}.{end_attr}",
        f"{squash_def}.highBound",
        force=True
    )

    attr_name = "Squash"

    attr_name = "Squash"
    if not cmds.attributeQuery(attr_name, node=ik_ctrl, exists=True):
        cmds.addAttr(
            ik_ctrl,
            longName=attr_name,
            attributeType="double",
            min=-2,
            max=2,
            defaultValue=0,
            keyable=True
        )

    cmds.connectAttr(
        f"{ik_ctrl}.{attr_name}",
        f"{squash_def}.factor",
        force=True
    )

    move_md = cmds.shadingNode(
        "multiplyDivide",
        asUtility=True,
        n=f"{prefix}_squash_move_MD"
    )

    start_loc = cmds.spaceLocator(n=f"{prefix}_squash_start_LOC")[0]
    end_loc = cmds.spaceLocator(n=f"{prefix}_squash_end_LOC")[0]

    cmds.delete(cmds.pointConstraint(ik_chain[0], start_loc))
    cmds.delete(cmds.pointConstraint(ik_ctrl, end_loc))

    cmds.pointConstraint(ik_chain[0], start_loc, mo=False)
    cmds.pointConstraint(ik_ctrl, end_loc, mo=False)

    start_dcm = cmds.shadingNode(
        "decomposeMatrix",
        asUtility=True,
        n=f"{prefix}_squash_start_DCM"
    )

    end_dcm = cmds.shadingNode(
        "decomposeMatrix",
        asUtility=True,
        n=f"{prefix}_squash_end_DCM"
    )

    delta_pma = cmds.shadingNode(
        "plusMinusAverage",
        asUtility=True,
        n=f"{prefix}_squash_delta_PMA"
    )

    move_md = cmds.shadingNode(
        "multiplyDivide",
        asUtility=True,
        n=f"{prefix}_squash_move_MD"
    )

    cmds.connectAttr(f"{start_loc}.worldMatrix[0]", f"{start_dcm}.inputMatrix")
    cmds.connectAttr(f"{end_loc}.worldMatrix[0]", f"{end_dcm}.inputMatrix")

    cmds.setAttr(f"{delta_pma}.operation", 2)

    axis_attr = {
        "X": "outputTranslateX",
        "Y": "outputTranslateY",
        "Z": "outputTranslateZ",
    }[cfg["axis"]]

    cmds.connectAttr(f"{end_dcm}.{axis_attr}", f"{delta_pma}.input1D[0]")
    cmds.connectAttr(f"{start_dcm}.{axis_attr}", f"{delta_pma}.input1D[1]")

    # Guardar delta inicial para que el squash arranque en 0.
    cmds.dgdirty(delta_pma)
    cmds.refresh()

    delta_inicial = cmds.getAttr(f"{delta_pma}.output1D")

    neutral_pma = cmds.shadingNode(
        "plusMinusAverage",
        asUtility=True,
        n=f"{prefix}_squash_neutral_PMA"
    )

    cmds.setAttr(f"{neutral_pma}.operation", 2)
    cmds.connectAttr(f"{delta_pma}.output1D", f"{neutral_pma}.input1D[0]")
    cmds.setAttr(f"{neutral_pma}.input1D[1]", delta_inicial)

    cmds.setAttr(f"{move_md}.input2X", cfg["mult"])
    cmds.connectAttr(f"{neutral_pma}.output1D", f"{move_md}.input1X", force=True)
    cmds.connectAttr(f"{move_md}.outputX", f"{ik_ctrl}.{attr_name}", force=True)

    if cmds.objExists("LOCATORS_GRP"):
        cmds.parent(start_loc, end_loc, "LOCATORS_GRP")



    if cmds.objExists("SYSTEMS_GRP"):
        cmds.parent(squash_handle, "SYSTEMS_GRP")

    cmds.select(clear=True)

    print(f"Squash creado: {prefix} -> {mesh}")

    return {
        "deformer": squash_def,
        "handle": squash_handle,
        "attr": f"{ik_ctrl}.{attr_name}"
    }
def crear_control(nombre, target, size=1, color=17):

    # círculo controlador
    ctrl = cmds.circle(
        n=nombre,
        normal=[1,0,0],
        radius=size
    )[0]

    # grupo offset
    offset = cmds.group(ctrl, n=f"{nombre}_OFFSET")

    # mover al joint
    cmds.delete(cmds.parentConstraint(target, offset))

    # color
    shapes = cmds.listRelatives(ctrl, s=True)

    for s in shapes:
        cmds.setAttr(f"{s}.overrideEnabled", 1)
        cmds.setAttr(f"{s}.overrideColor", color)

       # FK controls: solo rotacion.
    for attr in ["translateX", "translateY", "translateZ",
                 "scaleX", "scaleY", "scaleZ"]:
        cmds.setAttr(f"{ctrl}.{attr}", lock=True, keyable=False, channelBox=False)
    cmds.setAttr(f"{ctrl}.visibility", keyable=False, channelBox=False)

    return ctrl, offset

#
# =========================
# CREAR IK CTRL
# =========================

def crear_ik_control(nombre, ik_handle, target, size=1.5, color=13):

    ctrl = cmds.circle(
        n=nombre,
        normal=[1,0,0],
        radius=size
    )[0]

    root = cmds.group(ctrl, n=f"{nombre}_ROOT")
    auto = cmds.group(root, n=f"{nombre}_AUTO")

    # alinear
    cmds.delete(cmds.pointConstraint(target, root))
    cmds.delete(cmds.orientConstraint(target, root))

    # color
    shapes = cmds.listRelatives(ctrl, s=True)

    for s in shapes:
        cmds.setAttr(f"{s}.overrideEnabled", 1)
        cmds.setAttr(f"{s}.overrideColor", color)

    # mover handle con ctrl
    cmds.parent(ik_handle, ctrl)

    # IK controls: solo traslacion.
    for attr in ["rotateX", "rotateY", "rotateZ",
                 "scaleX", "scaleY", "scaleZ"]:
        cmds.setAttr(f"{ctrl}.{attr}", lock=True, keyable=False, channelBox=False)
    cmds.setAttr(f"{ctrl}.visibility", keyable=False, channelBox=False)

    return ctrl, root, auto

def crear_pv_control(nombre, pv_target, ik_handle, size=1, color=6, pv_offset=5, ik_chain=None, meshes=None, prefix=""):

    ctrl = cmds.circle(
        n=nombre,
        normal=[1,0,0],
        radius=size
    )[0]

    # Forma cruz
    cvs = [
        f"{ctrl}.cv[0]",
        f"{ctrl}.cv[2]",
        f"{ctrl}.cv[4]",
        f"{ctrl}.cv[6]"
    ]

    cmds.select(cvs)

    cmds.scale(0.2,0.2,0.2,r=True)
    cmds.rotate(0, 90, 0, f"{ctrl}.cv[*]", relative=True, objectSpace=True)

    cmds.select(clear=True)

    # grupos
    root = cmds.group(ctrl, n=f"{nombre}_ROOT")
    auto = cmds.group(root, n=f"{nombre}_AUTO")

    # Alinear fuera de la geometria usando la direccion real del pole vector.
    if ik_chain and len(ik_chain) >= 3:
        distancia = abs(pv_offset)

        if meshes:
            distancia = max(distancia, obtener_tamano_mesh(meshes, factor=0.45) + size)

        posicion_pv = _posicion_pole_vector(
            ik_chain[0],
            ik_chain[1],
            ik_chain[-1],
            distancia,
            prefix
        )
        cmds.xform(root, ws=True, t=posicion_pv)
    else:
        cmds.delete(cmds.pointConstraint(pv_target, root))
        cmds.move(0, 0, pv_offset, root, relative=True, objectSpace=True)

    # constraint
    cmds.poleVectorConstraint(ctrl, ik_handle)

    # color
    shapes = cmds.listRelatives(ctrl, s=True)

    for s in shapes:
        cmds.setAttr(f"{s}.overrideEnabled", 1)
        cmds.setAttr(f"{s}.overrideColor", color)

    # Pole vector controls: solo traslacion.
    for attr in ["rotateX", "rotateY", "rotateZ",
                 "scaleX", "scaleY", "scaleZ"]:
        cmds.setAttr(f"{ctrl}.{attr}", lock=True, keyable=False, channelBox=False)
    cmds.setAttr(f"{ctrl}.visibility", keyable=False, channelBox=False)

    return ctrl, root, auto


def crear_proxy_fk_locator(prefix, fk_chain, fk_controls, size=1, color=17):
    """
    Crea un locator proxy afuera de la punta de la extremidad.
    El borde interno del locator queda cerca del borde de la extremidad.
    Su movimiento afecta la rotacion de los controles FK internos.
    """

    if not fk_chain or not fk_controls:
        cmds.warning(f"No se pudo crear proxy FK para {prefix}")
        return None

    punta = fk_chain[-1]
    anterior = fk_chain[-2]

    locator = cmds.spaceLocator(n=f"{prefix}_PROXY_LOC_001")[0]
    offset = cmds.group(locator, n=f"{prefix}_PROXY_LOC_001_OFFSET")

    cmds.delete(cmds.parentConstraint(punta, offset))

    # Direccion desde el joint anterior hacia la punta.
    p_punta = cmds.xform(punta, q=True, ws=True, t=True)
    p_anterior = cmds.xform(anterior, q=True, ws=True, t=True)

    direccion = [
        p_punta[0] - p_anterior[0],
        p_punta[1] - p_anterior[1],
        p_punta[2] - p_anterior[2]
    ]

    largo = math.sqrt(
        direccion[0] ** 2 +
        direccion[1] ** 2 +
        direccion[2] ** 2
    )

    if largo != 0:
        direccion = [
            direccion[0] / largo,
            direccion[1] / largo,
            direccion[2] / largo
        ]
    else:
        direccion = [0, 0, 1]

    # Mueve el centro del locator hacia afuera.
    # Asi el borde interno queda en la punta de la extremidad.
    cmds.move(
        direccion[0] * size,
        direccion[1] * size,
        direccion[2] * size,
        offset,
        relative=True,
        worldSpace=True
    )

    shape = cmds.listRelatives(locator, shapes=True)[0]

    cmds.setAttr(f"{shape}.localScaleX", size)
    cmds.setAttr(f"{shape}.localScaleY", size)
    cmds.setAttr(f"{shape}.localScaleZ", size)

    # Color del proxy
    cmds.setAttr(f"{shape}.overrideEnabled", 1)
    cmds.setAttr(f"{shape}.overrideColor", color)


    # Proxy locators: solo traslacion.
    for attr in ["rotateX", "rotateY", "rotateZ",
                 "scaleX", "scaleY", "scaleZ",
                 "visibility"]:
        cmds.setAttr(f"{locator}.{attr}", lock=True, keyable=False, channelBox=False)

    # Movimiento del locator -> rotacion FK
    md_y = cmds.shadingNode(
        "multiplyDivide",
        asUtility=True,
        n=f"{prefix}_PROXY_translateY_to_rotateZ_MD"
    )

    cmds.setAttr(f"{md_y}.input2X", 5)
    cmds.connectAttr(f"{locator}.translateY", f"{md_y}.input1X", force=True)
    cmds.connectAttr(f"{md_y}.outputX", f"{fk_controls[0]}.rotateZ", force=True)

    md_z = cmds.shadingNode(
        "multiplyDivide",
        asUtility=True,
        n=f"{prefix}_PROXY_translateZ_to_rotateY_MD"
    )

    # Estaba invertido en Z: por eso este valor va negativo.
    cmds.setAttr(f"{md_z}.input2X", -5)
    cmds.connectAttr(f"{locator}.translateZ", f"{md_z}.input1X", force=True)
    cmds.connectAttr(f"{md_z}.outputX", f"{fk_controls[0]}.rotateY", force=True)

    if cmds.objExists("LOCATORS_GRP"):
        cmds.parent(offset, "LOCATORS_GRP")
    elif cmds.objExists("CTRL_GRP"):
        cmds.parent(offset, "CTRL_GRP")

    return {
        "locator": locator,
        "offset": offset
    }
