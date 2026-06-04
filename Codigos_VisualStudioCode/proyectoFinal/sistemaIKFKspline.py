import math
from pickle import GLOBAL

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
            size=tamano,
            fk=True
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
    global IK_CTRL_GLOBAL
    
    ik_ctrl, ik_root, ik_auto = crear_ik_control(
        f"{prefix}_IK_CTRL_001",
        ik_handle,
        ik_chain[-1],
        size=tamano,
        align_to_target=False
    )
    
    IK_CTRL_GLOBAL = ik_ctrl

    print("CONTROL GLOBAL:", IK_CTRL_GLOBAL)
 
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
            size=tamano,
            fk=False
        )

        cmds.parentConstraint(ctrl, cluster, mo=True)

        spine_controls.append(ctrl)

    # Jerarquia IK spline: pelvis -> pecho -> cabeza.
    for i in range(1, len(spine_controls)):
        cmds.parent(
            f"{spine_controls[i]}_OFFSET",
            spine_controls[i - 1]
        )

    if spine_controls:
        try:
            cmds.pointConstraint(spine_controls[0], ik_chain[0], mo=True)
            raiz_point = cmds.pointConstraint(fk_chain[0], ik_chain[0], main_chain[0], mo=False)[0]
            raiz_weights = cmds.pointConstraint(raiz_point, q=True, weightAliasList=True)
            cmds.connectAttr(f"{reverse}.outputX", f"{raiz_point}.{raiz_weights[0]}", force=True)
            cmds.connectAttr(f"{shape}.FKIK", f"{raiz_point}.{raiz_weights[1]}", force=True)
        except Exception as e:
            cmds.warning(f"No se pudo conectar {spine_controls[0]} a la raiz de columna: {e}")

    if spine_controls:
        chest_ctrl = spine_controls[-1]
        cmds.connectAttr(
            f"{chest_ctrl}.rotateY",
            f"{ik_handle}.twist"
        )
    
    # =========================
    # VISIBILIDAD FK / IK
    # =========================

    # FK visibles cuando FKIK = 0
    for ctrl in fk_controls:
        cmds.connectAttr(
            f"{reverse}.outputX",
            f"{ctrl}.visibility",
            force=True
        )

    # Este control es tecnico: guarda FKIK y el ikHandle, pero no se anima.
    cmds.setAttr(f"{ik_ctrl}.visibility", 0)

    shapes_ik = cmds.listRelatives(ik_ctrl, shapes=True) or []
    for shape_ik in shapes_ik:
        cmds.setAttr(f"{shape_ik}.visibility", 0)

    # spine controls visibles en IK
    for ctrl in spine_controls:
        cmds.connectAttr(
            f"{shape}.FKIK",
            f"{ctrl}.visibility",
            force=True
        )

    return {
        "ikHandle": ik_handle,
        "ikControl": ik_ctrl,
        "spineControls": spine_controls,
        "attrShape": shape,
        "constraints": constraints
        
    }

    


def cambiar_fkik(ctrl, valor):

    if not cmds.objExists(ctrl):
        cmds.warning(f"No existe el control: {ctrl}")
        return

    if not cmds.attributeQuery("FKIK", node=ctrl, exists=True):
        cmds.warning(f"{ctrl} no tiene atributo FKIK")
        return

    cmds.setAttr(f"{ctrl}.FKIK", valor)

    print(f"FKIK cambiado a {valor} en {ctrl}")


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


def crear_squash_spine(prefix, driver_ctrl, meshes, ik_chain):
    if not driver_ctrl or not cmds.objExists(driver_ctrl):
        cmds.warning(f"No existe control para squash spine: {driver_ctrl}")
        return None

    if not meshes:
        cmds.warning(f"No hay meshes para squash spine: {prefix}")
        return None

    mesh = None

    for candidato in meshes:
        if cmds.objExists(candidato) and "Tronco" in candidato:
            mesh = candidato
            break

    if not mesh:
        for candidato in meshes:
            if cmds.objExists(candidato):
                mesh = candidato
                break

    if not mesh:
        cmds.warning(f"No existe mesh para squash spine: {meshes}")
        return None

    for obj in cmds.ls(f"{prefix}_spine_squash*") or []:
        if cmds.objExists(obj):
            try:
                cmds.delete(obj)
            except Exception:
                pass

    cmds.select(f"{mesh}.vtx[*]", replace=True)

    squash_def, squash_handle = cmds.nonLinear(
        type="squash",
        n=f"{prefix}_spine_squash"
    )

    bbox = cmds.exactWorldBoundingBox(mesh)

    centro_x = (bbox[0] + bbox[3]) / 2
    centro_y = (bbox[1] + bbox[4]) / 2
    centro_z = (bbox[2] + bbox[5]) / 2
    alto = max(bbox[4] - bbox[1], 0.001)

    cmds.xform(
        squash_handle,
        ws=True,
        t=(centro_x, centro_y, centro_z)
    )

    cmds.setAttr(f"{squash_handle}.scaleX", 1)
    cmds.setAttr(f"{squash_handle}.scaleY", alto)
    cmds.setAttr(f"{squash_handle}.scaleZ", 1)

    cmds.setAttr(f"{squash_def}.lowBound", -0.75)
    cmds.setAttr(f"{squash_def}.highBound", 0.85)
    cmds.setAttr(f"{squash_def}.factor", 0)

    attr_name = "SpineSquash"
    if not cmds.attributeQuery(attr_name, node=driver_ctrl, exists=True):
        cmds.addAttr(
            driver_ctrl,
            longName=attr_name,
            attributeType="double",
            min=-2,
            max=2,
            defaultValue=0,
            keyable=True
        )

    cmds.connectAttr(
        f"{driver_ctrl}.{attr_name}",
        f"{squash_def}.factor",
        force=True
    )

    if ik_chain and len(ik_chain) >= 2:
        start_loc = cmds.spaceLocator(n=f"{prefix}_spine_squash_start_LOC")[0]
        end_loc = cmds.spaceLocator(n=f"{prefix}_spine_squash_end_LOC")[0]

        cmds.delete(cmds.pointConstraint(ik_chain[0], start_loc))
        cmds.delete(cmds.pointConstraint(driver_ctrl, end_loc))

        cmds.pointConstraint(ik_chain[0], start_loc, mo=False)
        cmds.pointConstraint(driver_ctrl, end_loc, mo=False)

        start_dcm = cmds.shadingNode(
            "decomposeMatrix",
            asUtility=True,
            n=f"{prefix}_spine_squash_start_DCM"
        )

        end_dcm = cmds.shadingNode(
            "decomposeMatrix",
            asUtility=True,
            n=f"{prefix}_spine_squash_end_DCM"
        )

        delta_pma = cmds.shadingNode(
            "plusMinusAverage",
            asUtility=True,
            n=f"{prefix}_spine_squash_delta_PMA"
        )

        cmds.connectAttr(f"{start_loc}.worldMatrix[0]", f"{start_dcm}.inputMatrix")
        cmds.connectAttr(f"{end_loc}.worldMatrix[0]", f"{end_dcm}.inputMatrix")

        cmds.setAttr(f"{delta_pma}.operation", 2)
        cmds.connectAttr(f"{end_dcm}.outputTranslateY", f"{delta_pma}.input1D[0]")
        cmds.connectAttr(f"{start_dcm}.outputTranslateY", f"{delta_pma}.input1D[1]")

        cmds.dgdirty(delta_pma)
        cmds.refresh()

        delta_inicial = cmds.getAttr(f"{delta_pma}.output1D")

        neutral_pma = cmds.shadingNode(
            "plusMinusAverage",
            asUtility=True,
            n=f"{prefix}_spine_squash_neutral_PMA"
        )

        move_md = cmds.shadingNode(
            "multiplyDivide",
            asUtility=True,
            n=f"{prefix}_spine_squash_move_MD"
        )

        cmds.setAttr(f"{neutral_pma}.operation", 2)
        cmds.connectAttr(f"{delta_pma}.output1D", f"{neutral_pma}.input1D[0]")
        cmds.setAttr(f"{neutral_pma}.input1D[1]", delta_inicial)

        cmds.setAttr(f"{move_md}.input2X", -0.04)
        cmds.connectAttr(f"{neutral_pma}.output1D", f"{move_md}.input1X", force=True)
        cmds.connectAttr(f"{move_md}.outputX", f"{driver_ctrl}.{attr_name}", force=True)

        if cmds.objExists("LOCATORS_GRP"):
            cmds.parent(start_loc, end_loc, "LOCATORS_GRP")

    if cmds.objExists("SYSTEMS_GRP"):
        cmds.parent(squash_handle, "SYSTEMS_GRP")

    cmds.select(clear=True)

    print(f"Squash spine creado: {prefix} -> {mesh}")

    return {
        "deformer": squash_def,
        "handle": squash_handle,
        "attr": f"{driver_ctrl}.{attr_name}"
    }


def crear_squash_cabeza(prefix, driver_ctrl, meshes, base_ctrl=None):
    if not driver_ctrl or not cmds.objExists(driver_ctrl):
        cmds.warning(f"No existe control para squash cabeza: {driver_ctrl}")
        return None

    mesh = None

    for candidato in meshes or []:
        if cmds.objExists(candidato) and "Cabeza" in candidato:
            mesh = candidato
            break

    if not mesh:
        cmds.warning(f"No existe mesh de cabeza para squash: {meshes}")
        return None

    shapes_mesh = cmds.listRelatives(mesh, shapes=True, noIntermediate=True, type="mesh") or []

    if not shapes_mesh:
        cmds.warning(f"Squash cabeza omitido: {mesh} no tiene forma mesh")
        return None

    for obj in cmds.ls(f"{prefix}_head_squash*") or []:
        if cmds.objExists(obj):
            try:
                cmds.delete(obj)
            except Exception:
                pass

    cmds.select(f"{mesh}.vtx[*]", replace=True)

    squash_def, squash_handle = cmds.nonLinear(
        type="squash",
        n=f"{prefix}_head_squash"
    )

    bbox = cmds.exactWorldBoundingBox(mesh)
    centro_x = (bbox[0] + bbox[3]) / 2
    centro_y = (bbox[1] + bbox[4]) / 2
    centro_z = (bbox[2] + bbox[5]) / 2
    alto = max(bbox[4] - bbox[1], 0.001)

    cmds.xform(
        squash_handle,
        ws=True,
        t=(centro_x, centro_y, centro_z)
    )

    cmds.setAttr(f"{squash_handle}.scaleX", 1)
    cmds.setAttr(f"{squash_handle}.scaleY", alto)
    cmds.setAttr(f"{squash_handle}.scaleZ", 1)

    cmds.setAttr(f"{squash_def}.lowBound", -0.9)
    cmds.setAttr(f"{squash_def}.highBound", 0.9)
    cmds.setAttr(f"{squash_def}.factor", 0)

    attr_name = "HeadSquash"
    if not cmds.attributeQuery(attr_name, node=driver_ctrl, exists=True):
        cmds.addAttr(
            driver_ctrl,
            longName=attr_name,
            attributeType="double",
            min=-2,
            max=2,
            defaultValue=0,
            keyable=True
        )

    if base_ctrl and cmds.objExists(base_ctrl) and not cmds.attributeQuery(attr_name, node=base_ctrl, exists=True):
        cmds.addAttr(
            base_ctrl,
            longName=attr_name,
            attributeType="double",
            min=-2,
            max=2,
            defaultValue=0,
            keyable=True
        )

    squash_sum = cmds.shadingNode(
        "plusMinusAverage",
        asUtility=True,
        n=f"{prefix}_head_squash_sum_PMA"
    )

    cmds.connectAttr(
        f"{driver_ctrl}.{attr_name}",
        f"{squash_sum}.input1D[0]",
        force=True
    )

    if base_ctrl and cmds.objExists(base_ctrl):
        cmds.connectAttr(
            f"{base_ctrl}.{attr_name}",
            f"{squash_sum}.input1D[1]",
            force=True
        )

    cmds.connectAttr(
        f"{squash_sum}.output1D",
        f"{squash_def}.factor",
        force=True
    )

    if base_ctrl and cmds.objExists(base_ctrl):
        start_loc = cmds.spaceLocator(n=f"{prefix}_head_squash_start_LOC")[0]
        end_loc = cmds.spaceLocator(n=f"{prefix}_head_squash_end_LOC")[0]

        cmds.delete(cmds.pointConstraint(base_ctrl, start_loc))
        cmds.delete(cmds.pointConstraint(driver_ctrl, end_loc))

        cmds.pointConstraint(base_ctrl, start_loc, mo=False)
        cmds.pointConstraint(driver_ctrl, end_loc, mo=False)

        start_dcm = cmds.shadingNode(
            "decomposeMatrix",
            asUtility=True,
            n=f"{prefix}_head_squash_start_DCM"
        )

        end_dcm = cmds.shadingNode(
            "decomposeMatrix",
            asUtility=True,
            n=f"{prefix}_head_squash_end_DCM"
        )

        delta_pma = cmds.shadingNode(
            "plusMinusAverage",
            asUtility=True,
            n=f"{prefix}_head_squash_delta_PMA"
        )

        neutral_pma = cmds.shadingNode(
            "plusMinusAverage",
            asUtility=True,
            n=f"{prefix}_head_squash_neutral_PMA"
        )

        move_md = cmds.shadingNode(
            "multiplyDivide",
            asUtility=True,
            n=f"{prefix}_head_squash_move_MD"
        )

        cmds.connectAttr(f"{start_loc}.worldMatrix[0]", f"{start_dcm}.inputMatrix")
        cmds.connectAttr(f"{end_loc}.worldMatrix[0]", f"{end_dcm}.inputMatrix")

        cmds.setAttr(f"{delta_pma}.operation", 2)
        cmds.connectAttr(f"{end_dcm}.outputTranslateY", f"{delta_pma}.input1D[0]")
        cmds.connectAttr(f"{start_dcm}.outputTranslateY", f"{delta_pma}.input1D[1]")

        cmds.dgdirty(delta_pma)
        cmds.refresh()

        delta_inicial = cmds.getAttr(f"{delta_pma}.output1D")

        cmds.setAttr(f"{neutral_pma}.operation", 2)
        cmds.connectAttr(f"{delta_pma}.output1D", f"{neutral_pma}.input1D[0]")
        cmds.setAttr(f"{neutral_pma}.input1D[1]", delta_inicial)

        cmds.setAttr(f"{move_md}.input2X", -0.05)
        cmds.connectAttr(f"{neutral_pma}.output1D", f"{move_md}.input1X", force=True)
        cmds.connectAttr(f"{move_md}.outputX", f"{driver_ctrl}.{attr_name}", force=True)

        base_start_loc = None
        base_end_loc = None
        base_offset = f"{base_ctrl}_OFFSET"
        base_padre = None

        if cmds.objExists(base_offset):
            padres = cmds.listRelatives(base_offset, parent=True) or []
            if padres:
                base_padre = padres[0]

        if base_padre and cmds.objExists(base_padre):
            base_start_loc = cmds.spaceLocator(n=f"{prefix}_head_base_squash_start_LOC")[0]
            base_end_loc = cmds.spaceLocator(n=f"{prefix}_head_base_squash_end_LOC")[0]

            cmds.delete(cmds.pointConstraint(base_padre, base_start_loc))
            cmds.delete(cmds.pointConstraint(base_ctrl, base_end_loc))

            cmds.pointConstraint(base_padre, base_start_loc, mo=False)
            cmds.pointConstraint(base_ctrl, base_end_loc, mo=False)

            base_start_dcm = cmds.shadingNode(
                "decomposeMatrix",
                asUtility=True,
                n=f"{prefix}_head_base_squash_start_DCM"
            )

            base_end_dcm = cmds.shadingNode(
                "decomposeMatrix",
                asUtility=True,
                n=f"{prefix}_head_base_squash_end_DCM"
            )

            base_delta_pma = cmds.shadingNode(
                "plusMinusAverage",
                asUtility=True,
                n=f"{prefix}_head_base_squash_delta_PMA"
            )

            base_neutral_pma = cmds.shadingNode(
                "plusMinusAverage",
                asUtility=True,
                n=f"{prefix}_head_base_squash_neutral_PMA"
            )

            base_move_md = cmds.shadingNode(
                "multiplyDivide",
                asUtility=True,
                n=f"{prefix}_head_base_squash_move_MD"
            )

            cmds.connectAttr(f"{base_start_loc}.worldMatrix[0]", f"{base_start_dcm}.inputMatrix")
            cmds.connectAttr(f"{base_end_loc}.worldMatrix[0]", f"{base_end_dcm}.inputMatrix")

            cmds.setAttr(f"{base_delta_pma}.operation", 2)
            cmds.connectAttr(f"{base_end_dcm}.outputTranslateY", f"{base_delta_pma}.input1D[0]")
            cmds.connectAttr(f"{base_start_dcm}.outputTranslateY", f"{base_delta_pma}.input1D[1]")

            cmds.dgdirty(base_delta_pma)
            cmds.refresh()

            base_delta_inicial = cmds.getAttr(f"{base_delta_pma}.output1D")

            cmds.setAttr(f"{base_neutral_pma}.operation", 2)
            cmds.connectAttr(f"{base_delta_pma}.output1D", f"{base_neutral_pma}.input1D[0]")
            cmds.setAttr(f"{base_neutral_pma}.input1D[1]", base_delta_inicial)

            cmds.setAttr(f"{base_move_md}.input2X", -0.04)
            cmds.connectAttr(f"{base_neutral_pma}.output1D", f"{base_move_md}.input1X", force=True)
            cmds.connectAttr(f"{base_move_md}.outputX", f"{base_ctrl}.{attr_name}", force=True)

        if cmds.objExists("LOCATORS_GRP"):
            cmds.parent(start_loc, end_loc, "LOCATORS_GRP")
            if base_start_loc and base_end_loc:
                cmds.parent(base_start_loc, base_end_loc, "LOCATORS_GRP")

    if cmds.objExists("SYSTEMS_GRP"):
        cmds.parent(squash_handle, "SYSTEMS_GRP")

    cmds.select(clear=True)

    print(f"Squash cabeza creado: {prefix} -> {mesh}")

    return {
        "deformer": squash_def,
        "handle": squash_handle,
        "attr": f"{driver_ctrl}.{attr_name}"
    }


def crear_control(nombre, target, size=1, color=17, fk=True):

    # círculo controlador
    ctrl = cmds.circle(
        n=nombre,
        normal=[0,1,0],
        radius=size
    )[0]

    # grupo offset
    offset = cmds.group(ctrl, n=f"{nombre}_OFFSET")

    # mover al joint
    cmds.delete(cmds.parentConstraint(target, offset))

    # orientación mundial
    cmds.xform(offset, ws=True, rotation=(0,0,0))

    # color
    shapes = cmds.listRelatives(ctrl, s=True)

    for s in shapes:
        cmds.setAttr(f"{s}.overrideEnabled", 1)
        cmds.setAttr(f"{s}.overrideColor", color)

        #  BLOQUEO AUTOMÁTICO
    if fk:
        # FK → solo rotate
        for a in ["tx","ty","tz","sx","sy","sz"]:
            cmds.setAttr(f"{ctrl}.{a}", lock=True, keyable=False, channelBox=False)

    else:
        # IK → sin scale
        for a in ["rx","ry","rz","sx","sy","sz"]:
            cmds.setAttr(f"{ctrl}.{a}", lock=True, keyable=False, channelBox=False)
        

    return ctrl, offset


def crear_ik_control(nombre, ik_handle, target, size=1.5, color=13, align_to_target=True):

    ctrl = cmds.circle(
        n=nombre,
        normal=[0,1,0],
        radius=size
    )[0]

    root = cmds.group(ctrl, n=f"{nombre}_ROOT")
    auto = cmds.group(root, n=f"{nombre}_AUTO")

    # alinear posición
    # SOLO posición
    cmds.delete(cmds.pointConstraint(target, root))

    # orientación mundial
    cmds.xform(root, ws=True, rotation=(0,0,0))

    # color
    shapes = cmds.listRelatives(ctrl, s=True)

    for s in shapes:
        cmds.setAttr(f"{s}.overrideEnabled", 1)
        cmds.setAttr(f"{s}.overrideColor", color)

    # mover handle con ctrl
    cmds.parent(ik_handle, ctrl)

    # IK controls: solo traslacion.
    for a in ["rx", "ry", "rz", "sx", "sy", "sz"]:
        cmds.setAttr(f"{ctrl}.{a}", lock=True, keyable=False, channelBox=False)
    cmds.setAttr(f"{ctrl}.visibility", keyable=False, channelBox=False)

    return ctrl, root, auto
