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
        size=tamano * 0.7
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

    
    return {
        "ikHandle": ik_handle,
        "ikControl": ik_ctrl,
        "poleVector": pv_ctrl,
        "attrShape": shape,
        "constraints": constraints
    }

def bind_skin_cube(mesh, joints):

    # =========================
    # 1. SUBDIVISIÓN DEL MESH
    # =========================
    cmds.polySmooth(mesh, divisions=2)

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

    return ctrl, root, auto

def crear_pv_control(nombre, pv_target, ik_handle, size=1, color=6):

    ctrl = cmds.circle(
        n=nombre,
        normal=[0,1,0],
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

    cmds.scale(
        0.2,
        0.2,
        0.2,
        r=True
    )

    cmds.select(clear=True)

    # grupos
    root = cmds.group(ctrl, n=f"{nombre}_ROOT")
    auto = cmds.group(root, n=f"{nombre}_AUTO")

    # alinear
    cmds.delete(cmds.pointConstraint(pv_target, root))

    # constraint
    cmds.poleVectorConstraint(ctrl, ik_handle)

    # color
    shapes = cmds.listRelatives(ctrl, s=True)

    for s in shapes:
        cmds.setAttr(f"{s}.overrideEnabled", 1)
        cmds.setAttr(f"{s}.overrideColor", color)

    return ctrl, root, auto
