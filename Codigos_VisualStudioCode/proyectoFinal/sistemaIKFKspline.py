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
    # =========================
    # IK HANDLE
    # =========================
    ik_result = cmds.ikHandle(
        sj=ik_chain[0],
        ee=ik_chain[-1],
        solver="ikSplineSolver",
        createCurve=True,
        parentCurve=False
    )

    ik_handle = ik_result[0]
    effector = ik_result[1] if len(ik_result) > 1 else None
    curve = ik_result[2] if len(ik_result) > 2 else None

    ik_handle = cmds.rename(ik_handle, f"{prefix}_IKHandle_001")
    if curve:
        curve = cmds.rename(curve, f"{prefix}_IKCurve_001")

    # =========================
    # IK CONTROL
    # =========================

    ik_ctrl, ik_root, ik_auto = crear_ik_control(
        f"{prefix}_IK_CTRL_001",
        ik_handle,
        ik_chain[-1],
        size=tamano,
        align_to_target=False
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
    # CONTROLES DE CURVA SPLINE
    # =========================

    clusters = []
    if curve and cmds.objExists(curve):
        num_cvs = cmds.getAttr(f"{curve}.spans") + cmds.getAttr(f"{curve}.degree")

        for i in range(num_cvs):
            cluster = cmds.cluster(f"{curve}.cv[{i}]")[1]
            clusters.append(cluster)

    spine_controls = []

    for i, cluster in enumerate(clusters):

        ctrl, offset = crear_control(
            f"{prefix}_SPINE_CTRL_{i+1:03}",
            cluster,
            size=tamano
        )

        cmds.parentConstraint(ctrl, cluster, mo=True)

        spine_controls.append(ctrl)

    if spine_controls:
        chest_ctrl = spine_controls[-1]
        cmds.connectAttr(
            f"{chest_ctrl}.rotateY",
            f"{ik_handle}.twist"
        )

    return {
        "ikHandle": ik_handle,
        "ikControl": ik_ctrl,
        "attrShape": shape,
        "constraints": constraints
    }

def bind_skin_cube(mesh, joints):

    if not cmds.objExists(mesh):
        cmds.warning(f"bind_skin_cube: mesh no existe -> {mesh}")
        return None

    valid_joints = [j for j in joints if cmds.objExists(j)]
    if not valid_joints:
        cmds.warning(f"bind_skin_cube: no existen joints válidos -> {joints}")
        return None

    shapes = cmds.listRelatives(mesh, shapes=True, noIntermediate=True)
    if not shapes:
        cmds.warning(f"bind_skin_cube: el objeto no tiene forma -> {mesh}")
        return None

    # =========================
    # 1. SUBDIVISIÓN DEL MESH
    # =========================
    try:
        cmds.polySmooth(mesh, divisions=2)
    except Exception as e:
        cmds.warning(f"polySmooth falló en {mesh}: {e}")

    # =========================
    # 2. LIMPIEZA BASE
    # =========================
    try:
        cmds.makeIdentity(mesh, apply=True, t=True, r=True, s=True, n=False)
        cmds.delete(mesh, ch=True)
    except Exception as e:
        cmds.warning(f"Limpieza de mesh falló en {mesh}: {e}")

    # =========================
    # 3. SMOOTH BIND
    # =========================
    cmds.select(valid_joints, replace=True)
    try:
        skin_result = cmds.skinCluster(
            valid_joints,
            mesh,
            toSelectedBones=True,
            bindMethod=0,
            skinMethod=0,
            normalizeWeights=1,
            maximumInfluences=3,
            dropoffRate=4.0
        )
    except Exception as e:
        cmds.warning(f"skinCluster falló en {mesh}: {e}")
        cmds.select(clear=True)
        return None

    skin = skin_result[0] if isinstance(skin_result, (list, tuple)) else skin_result

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
    except Exception:
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

    return ctrl, offset

def crear_ik_control(nombre, ik_handle, target, size=1.5, color=13, align_to_target=True):

    ctrl = cmds.circle(
        n=nombre,
        normal=[1,0,0],
        radius=size
    )[0]

    root = cmds.group(ctrl, n=f"{nombre}_ROOT")
    auto = cmds.group(root, n=f"{nombre}_AUTO")

    # alinear posición
    cmds.delete(cmds.pointConstraint(target, root))
    if align_to_target:
        cmds.delete(cmds.orientConstraint(target, root))
    else:
        cmds.xform(root, ws=True, rotation=(0, 0, 0))

    # color
    shapes = cmds.listRelatives(ctrl, s=True)

    for s in shapes:
        cmds.setAttr(f"{s}.overrideEnabled", 1)
        cmds.setAttr(f"{s}.overrideColor", color)

    # mover handle con ctrl
    cmds.parent(ik_handle, ctrl)

    return ctrl, root, auto
