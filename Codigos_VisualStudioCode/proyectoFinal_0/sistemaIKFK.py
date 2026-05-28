import maya.cmds as cmds
import math


def crear_sistema_ikfk(fk_chain,ik_chain,main_chain,prefix,joint_attr,pv_offset=5):

# =========================
    # CALCULAR TAMAÑO
    # =========================

    tamano = distancia_entre(main_chain[0], main_chain[1]) * 0.5

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

    ik_ctrl, ik_offset = crear_control(
        f"{prefix}_IK_CTRL_001",
        ik_chain[-1],
        size=tamano * 1.3,
        color=13
    )

    cmds.parent(ik_handle, ik_ctrl)

    # =========================
    # POLE VECTOR
    # =========================

    pv_ctrl, pv_offset_grp = crear_control(
        f"{prefix}_PV_CTRL_001",
        ik_chain[1],
        size=tamano * 0.7,
        color=6
    )

    cmds.move(
        0,
        0,
        pv_offset,
        pv_offset_grp,
        relative=True
    )

    cmds.poleVectorConstraint(
        pv_ctrl,
        ik_handle
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
    locator = cmds.spaceLocator()[0]

    shape = cmds.listRelatives(locator,shapes=True)[0]
    shape = cmds.rename(shape,f"{prefix}_FKIK_attributes")

    cmds.addAttr(shape,longName="FKIK",attributeType='double', min=0,max=1,
        keyable=True)
    cmds.setAttr(f"{shape}.visibility",0)
    cmds.parent(shape,joint_attr,r=True,s=True)
    cmds.delete(locator)

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