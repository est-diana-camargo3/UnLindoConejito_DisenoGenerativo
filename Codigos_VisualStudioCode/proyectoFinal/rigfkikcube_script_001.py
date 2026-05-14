import maya.cmds as cmds

# =========================
# VARIABLES GLOBALES
# =========================
created_joints = []
joint_count = 0
job_id = None
is_rig_built = False
cube_mesh = None


# =========================
# UI
# =========================
def create_ui():

    if cmds.window("AutoRigUI", exists=True):
        cmds.deleteUI("AutoRigUI")

    window = cmds.window("AutoRigUI", title="Auto FKIK Rig", widthHeight=(250, 120))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    cmds.text(label="Auto Rig FK/IK", align="center")

    cmds.button(
        label="Crear Rig desde Cubo",
        height=40,
        command=lambda x: create_joints_from_cube()
    )
    cmds.showWindow(window)


def get_primary_axis(bbox):

    xmin, ymin, zmin, xmax, ymax, zmax = bbox

    dx = xmax - xmin
    dy = ymax - ymin
    dz = zmax - zmin

    if dy >= dx and dy >= dz:
        return "Y"
    elif dx >= dy and dx >= dz:
        return "X"
    else:
        return "Z"
    
def get_joint_positions(bbox, axis):

    xmin, ymin, zmin, xmax, ymax, zmax = bbox

    if axis == "Y":

        center_x = (xmin + xmax) / 2
        center_z = (zmin + zmax) / 2

        return [
            (center_x, ymax, center_z),      # top
            (center_x, (ymin + ymax)/2, center_z),  # mid
            (center_x, ymin, center_z)       # bottom
        ]

    elif axis == "X":

        center_y = (ymin + ymax) / 2
        center_z = (zmin + zmax) / 2

        return [
            (xmax, center_y, center_z),
            ((xmin + xmax)/2, center_y, center_z),
            (xmin, center_y, center_z)
        ]

    else:  # Z

        center_x = (xmin + xmax) / 2
        center_y = (ymin + ymax) / 2

        return [
            (center_x, center_y, zmax),
            (center_x, center_y, (zmin + zmax)/2),
            (center_x, center_y, zmin)
        ]
    
# =========================
# CREATE JOINTS FROM CUBE
# =========================
def create_joints_from_cube():

    global created_joints

    selection = cmds.ls(selection=True)

    if not selection:
        cmds.warning("Selecciona un cubo")
        return

    cube = selection[0]

    # bounding box mundial
    bbox = cmds.exactWorldBoundingBox(cube)

    xmin, ymin, zmin, xmax, ymax, zmax = bbox


    axis = get_primary_axis(bbox)
    positions = get_joint_positions(bbox, axis)

    cmds.select(clear=True)
    j1 = cmds.joint(p=positions[0])
    j2 = cmds.joint(p=positions[1])
    j3 = cmds.joint(p=positions[2])

    created_joints = [j1, j2, j3]

    global cube_mesh
    cube_mesh = cube

    # orientar cadena
    cmds.joint(
        j1,
        e=True,
        oj="xyz",
        secondaryAxisOrient="yup",
        ch=True,
        zso=True
    )

    cmds.joint(j3, e=True, oj="none")

    # construir rig completo
    rename_created_joints()
    build_full_rig()

    cmds.inViewMessage(
        amg='RIG CREADO DESDE CUBO',
        pos='midCenter',
        fade=True
    )


# =========================
# CALLBACK
# =========================
def joint_created_callback():
    global joint_count, created_joints, job_id, is_rig_built

    if is_rig_built:
        return

    selection = cmds.ls(selection=True, type="joint")

    if not selection:
        return

    for j in selection:
        if j not in created_joints:
            created_joints.append(j)
            joint_count += 1

    if joint_count == 3 and not is_rig_built:

        is_rig_built = True

        cmds.setToolTo("selectSuperContext")

        if job_id and cmds.scriptJob(exists=job_id):
            cmds.scriptJob(kill=job_id, force=True)

        rename_created_joints()
        build_full_rig()

        cmds.inViewMessage(
            amg='RIG COMPLETO CREADO',
            pos='midCenter',
            fade=True
        )

# =========================
# ORDERED CHAIN
# =========================
def get_ordered_chain(root_joint):

    chain = cmds.listRelatives(root_joint, ad=True, type="joint") or []

    chain.reverse()  # 🔥 IMPORTANTE (ordena de padre → hijo)

    chain.insert(0, root_joint)

    return chain
# =========================
# RENAME
# =========================
def rename_created_joints(prefix="Leg_practice_L"):

    global created_joints

    root = created_joints[0]

    chain = cmds.listRelatives(root, ad=True, type='joint') or []
    chain.reverse()
    chain.insert(0, root)

    names = ["upper", "middle", "end"]

    renamed = []

    for i, j in enumerate(chain):
        new_name = f"{names[i]}{prefix}_joint_001"
        j = cmds.rename(j, new_name)
        renamed.append(j)

    created_joints[:] = renamed


# =========================
# DUPLICATE
# =========================
def duplicate_chain(root_joint, mode):

    # Duplicar jerarquía completa
    duplicated_root = cmds.duplicate(root_joint, rc=True)[0]

    # Obtener cadena ordenada
    chain = cmds.listRelatives(duplicated_root, ad=True, type='joint') or []
    chain.reverse()
    chain.insert(0, duplicated_root)

    names = ["upper", "middle", "end"]

    new_chain = []

    for i, j in enumerate(chain):

        base = root_joint.replace("_joint_001", "")

        new_name = f"{names[i]}{base}_{mode}_001"

        j = cmds.rename(j, new_name)
        new_chain.append(j)

    return new_chain


# =========================
# ROOT AUTO CHAIN
# =========================
def create_root_auto_chain(joint_chain):

    previous_joint = None

    for joint in joint_chain:

        name = joint.replace("_joint_001", "")

        cmds.parent(joint, world=True)

        root = cmds.group(empty=True, name=f"{name}_root_001")
        auto = cmds.group(empty=True, name=f"{name}_auto_001")

        cmds.delete(cmds.parentConstraint(joint, root))
        cmds.delete(cmds.parentConstraint(joint, auto))

        cmds.parent(auto, root)
        cmds.parent(joint, auto)

        if previous_joint:
            cmds.parent(root, previous_joint)

        previous_joint = joint


# =========================
# CONTROL
# =========================
def create_control(joint):

    name = joint.replace("joint", "ctrl")

    ctrl = cmds.circle(name=name, normal=[1,0,0])[0]
    cmds.delete(cmds.parentConstraint(joint, ctrl))
    shape = cmds.listRelatives(ctrl, shapes=True)[0]

    cmds.parent(shape, joint, r=True, s=True)

    cmds.delete(ctrl)


def create_ik_control(ik_handle,bbox,axis):

    xmin, ymin, zmin, xmax, ymax, zmax = bbox

    
    name = ik_handle.replace("IKhandle", "IKctrl")
    if axis == "Y":
        ctrl = cmds.circle(
            name=name,
            normal=[0,1,0],
            radius=1.5
        )[0]
        
    else :
        ctrl = cmds.circle(
            name=name,
            normal=[1,0,0],
            radius=1.5
        )[0]

    # mover control al IK Handle
    cmds.delete(cmds.pointConstraint(ik_handle, ctrl))

    # grupos root/auto
    root = cmds.group(ctrl, name=f"{name}_root")
    auto = cmds.group(root, name=f"{name}_auto")

    cmds.delete(cmds.pointConstraint(ik_handle, root))

    # el control mueve el handle
    cmds.parent(ik_handle, ctrl)

def create_pv_control(pv):

    ctrl = cmds.circle(
        name=pv.replace("IKpoleVector", "PVctrl"),
        normal=[0,1,0],
        radius=1
    )[0]

    # mover al pole vector
    cmds.delete(cmds.pointConstraint(pv, ctrl))

    # rotación como tu ejemplo
    cmds.rotate(-66.359982, 0, 0, ctrl, r=True, ws=True)
    cmds.setAttr(f"{ctrl}.rotateX", 90)

    # obtener cvs
    cvs = [
        f"{ctrl}.cv[0]",
        f"{ctrl}.cv[2]",
        f"{ctrl}.cv[4]",
        f"{ctrl}.cv[6]"
    ]

    # escalar cvs para hacer forma tipo cruz
    cmds.select(cvs)
    cmds.scale(
        0.110958,
        0.110958,
        0.110958,
        r=True
    )

    cmds.scale(
        0.551575,
        0.551575,
        0.551575,
        r=True
    )

    cmds.select(clear=True)

    # freeze
    cmds.makeIdentity(ctrl, apply=True, t=True, r=True, s=True)

    # grupos
    root = cmds.group(ctrl, name=f"{ctrl}_root")
    auto = cmds.group(root, name=f"{ctrl}_auto")

    cmds.delete(cmds.pointConstraint(pv, root))

    # constraint al pole vector
    cmds.parent(pv, ctrl)

    return ctrl


# =========================
# IK SYSTEM
# =========================
def create_ik(chain, prefix):

    ik_handle, effector = cmds.ikHandle(
        sj=chain[0],
        ee=chain[-1],
        solver="ikRPsolver"
    )

    ik_handle = cmds.rename(ik_handle, f"{prefix}_IKhandle_001")

    pv = cmds.group(empty=True, name=f"{prefix}_IKpoleVector_001")

    cmds.delete(cmds.pointConstraint(chain[1], pv))
    cmds.move(0, 0, 5, pv, relative=True)

    cmds.poleVectorConstraint(pv, ik_handle)

    return ik_handle, pv


# =========================
# CONSTRAINTS
# =========================
def create_constraints(fk_chain, ik_chain, main_chain):

    constraints = []

    for fk, ik, main in zip(fk_chain[:-1], ik_chain[:-1], main_chain[:-1]):
        c = cmds.orientConstraint(fk, ik, main, mo=False)[0]
        constraints.append(c)

    return constraints


# =========================
# FKIK ATTR
# =========================
def create_fkik_attr(joint):

    locator = cmds.spaceLocator()[0]
    shape = cmds.listRelatives(locator, shapes=True)[0]

    shape = cmds.rename(shape, "FKIK_attributes")

    cmds.addAttr(shape,
                 longName="FKIK",
                 attributeType='double',
                 min=0,
                 max=1,
                 keyable=True)

    cmds.setAttr(f"{shape}.visibility", 0)

    cmds.parent(shape, joint, r=True, s=True)
    cmds.delete(locator)

    return shape


# =========================
# CONNECTION SYSTEM (NODE EDITOR STYLE)
# =========================
def connect_fkik(attr_node, constraints):

    reverse = cmds.shadingNode('reverse', asUtility=True)

    # FKIK → reverse
    cmds.connectAttr(f"{attr_node}.FKIK", f"{reverse}.inputX")

    for c in constraints:
        weights = cmds.orientConstraint(c, q=True, weightAliasList=True)

        # FK directo
        cmds.connectAttr(f"{attr_node}.FKIK", f"{c}.{weights[0]}", force=True)

        # IK invertido (como en Node Editor)
        cmds.connectAttr(f"{reverse}.outputX", f"{c}.{weights[1]}", force=True)


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

# =========================
# BUILD
# =========================
def build_full_rig():

    global created_joints

    if len(created_joints) != 3:
        cmds.warning("Necesitas 3 joints")
        return

    fk_chain = created_joints
    root = fk_chain[0]
    prefix = root.replace("_joint_001", "")

    # Duplicados
    ik_chain = duplicate_chain(root, "IK")
    main_chain = duplicate_chain(root, "MAIN")
    fk_chain = get_ordered_chain(root)

    # Root/Auto en cascada
    create_root_auto_chain(fk_chain)

    # Controles
    for j in fk_chain:
        create_control(j)

    # IK
    ik_handle, pv = create_ik(ik_chain, prefix)

    bbox = cmds.exactWorldBoundingBox(cube_mesh)
    axis = get_primary_axis(bbox)
    create_ik_control(ik_handle, bbox, axis)
    create_pv_control(pv)

    # Constraints
    constraints = create_constraints(fk_chain, ik_chain, main_chain)

    # FKIK attr
    attr = create_fkik_attr(root)

    # Conexiones tipo node editor
    connect_fkik(attr, constraints)

    bind_skin_cube(cube_mesh, main_chain)


# =========================
# RUN
# =========================
create_ui()