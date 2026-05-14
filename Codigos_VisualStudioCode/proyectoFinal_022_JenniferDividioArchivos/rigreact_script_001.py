import maya.cmds as cmds

# =========================
# CONFIG
# =========================
NUM_JOINTS = 4


# =========================
# 1. LEER CUBO Y GENERAR POSICIONES
# =========================
def get_positions_from_cube(cube):
    xmin, ymin, zmin, xmax, ymax, zmax = cmds.exactWorldBoundingBox(cube)

    positions = []

    for i in range(NUM_JOINTS):
        t = i / float(NUM_JOINTS - 1)
        y = ymax + (ymin - ymax) * t

        pos = [
            (xmin + xmax) * 0.5,
            y,
            (zmin + zmax) * 0.5
        ]

        positions.append(pos)

    return positions


# =========================
# 2. CREAR JOINTS
# =========================
def create_joints_from_positions(positions):
    joints = []

    cmds.select(clear=True)

    for i, pos in enumerate(positions):
        j = cmds.joint(p=pos, name=f"joint_{i+1:03}")
        joints.append(j)

    cmds.joint(joints[0], e=True, oj="xyz", sao="yup", ch=True, zso=True)

    return joints


# =========================
# 3. SPLINE (IGUAL QUE TU SISTEMA)
# =========================
def create_spline_from_joints(joints):
    points = [cmds.xform(j, q=True, ws=True, t=True) for j in joints]

    curve = cmds.curve(d=3, p=points, name="splineCurve_001")

    cmds.rebuildCurve(curve, s=2, d=3, ch=False)

    shape = cmds.listRelatives(curve, s=True)[0]
    cmds.setAttr(f"{shape}.dispCV", 1)

    return curve, shape


# =========================
# 4. LOCATORS + CONTROL POINTS
# =========================
def create_locators_and_connect(shape, positions):
    locators = []

    for i, pos in enumerate(positions):
        loc = cmds.spaceLocator(name=f"spineLoc_ctrl_{i+1:03}")[0]
        cmds.xform(loc, ws=True, t=pos)

        cmds.connectAttr(
            f"{loc}.translate",
            f"{shape}.controlPoints[{i}]"
        )

        locators.append(loc)

    return locators


# =========================
# 5. DECOMPOSE MATRIX (PRO)
# =========================
def connect_with_decompose(locators, shape):
    for i, loc in enumerate(locators):
        node = cmds.createNode(
            "decomposeMatrix",
            name=f"decomposeMatrix_{i+1:03}"
        )

        cmds.connectAttr(f"{loc}.worldMatrix[0]", f"{node}.inputMatrix")
        cmds.connectAttr(
            f"{node}.outputTranslate",
            f"{shape}.controlPoints[{i}]",
            force=True
        )


# =========================
# 6. CONTROLES (CIRCLES)
# =========================
def create_controls(locators):
    ctrls = []

    for i, loc in enumerate(locators):
        ctrl = cmds.circle(
            name=f"ctrlShape_{i+1:03}",
            nr=(0, 1, 0)
        )[0]

        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.parent(shape, loc, r=True, s=True)
        cmds.delete(ctrl)

        ctrls.append(loc)

    return ctrls


# =========================
# 7. ROOTS
# =========================
def create_root_groups(ctrls):
    roots = []

    for ctrl in ctrls:
        root = cmds.group(em=True, name=ctrl.replace("ctrl", "root"))
        cmds.delete(cmds.parentConstraint(ctrl, root))
        cmds.parent(ctrl, root)
        roots.append(root)

    return roots


# =========================
# 8. TARGETS (POINT ON CURVE)
# =========================
def create_targets(shape):
    targets = []

    for i in range(NUM_JOINTS):
        t = cmds.spaceLocator(name=f"spineTarget_ctrl_{i+1:03}")[0]

        poc = cmds.createNode(
            "pointOnCurveInfo",
            name=f"poc_{i+1:03}"
        )

        cmds.connectAttr(
            f"{shape}.worldSpace[0]",
            f"{poc}.inputCurve"
        )

        cmds.connectAttr(
            f"{poc}.position",
            f"{t}.translate"
        )

        param = i / float(NUM_JOINTS - 1)
        cmds.setAttr(f"{poc}.parameter", param)

        targets.append(t)

    return targets


# =========================
# 9. AIM CHAIN
# =========================
def create_aim_constraints(targets):
    for i in range(len(targets) - 1):
        cmds.aimConstraint(
            targets[i + 1],
            targets[i],
            aimVector=(1, 0, 0),
            upVector=(0, 1, 0),
            worldUpType="vector"
        )


# =========================
# 10. JOINT FOLLOW
# =========================
def connect_joints_to_targets(joints, targets):
    for j, t in zip(joints, targets):
        cmds.parentConstraint(t, j, mo=True)



def drive_mesh_orientation(mesh, top_joint, bottom_joint):

    # crea constraint directo (más estable)
    cmds.orientConstraint(top_joint, bottom_joint, mesh, mo=True)

# =========================
# 11. BUILD FINAL (CUBO → RIG)
# =========================
def build_cube_spine_rig():
    sel = cmds.ls(sl=True)

    if not sel:
        cmds.warning("Selecciona un cubo")
        return

    cube = sel[0]

    positions = get_positions_from_cube(cube)

    joints = create_joints_from_positions(positions)

    curve, shape = create_spline_from_joints(joints)

    locators = create_locators_and_connect(shape, positions)

    connect_with_decompose(locators, shape)

    create_controls(locators)

    create_root_groups(locators)

    targets = create_targets(shape)

    create_aim_constraints(targets)

    connect_joints_to_targets(joints, targets)

    drive_mesh_orientation(cube, joints[0], joints[-1])
    

    print("✅ Rig spline desde cubo creado correctamente")
    print("MESH FINAL:", cube)
    print(cmds.listRelatives(cube , s=True))


# =========================
# UI SIMPLE
# =========================
def create_ui():
    if cmds.window("SpineRigUI", exists=True):
        cmds.deleteUI("SpineRigUI")

    cmds.window("SpineRigUI", title="Auto Spine Cube Rig")
    cmds.columnLayout(adj=True)

    cmds.button(
        label="Seleccionar cubo → Build Rig",
        c=lambda x: build_cube_spine_rig()
    )

    cmds.showWindow()

create_ui()