import maya.cmds as cmds

# =========================
# 2. CREAR SPLINE
# =========================
def create_spline_from_joints(joints):
    points = [cmds.xform(j, q=True, ws=True, t=True) for j in joints]
    
    curve = cmds.curve(d=3, p=points, name="splineCurve_001")
    
    cmds.rebuildCurve(
    curve,
    s=len(joints)-1,
    d=3,
    ch=False
)
    
    shape = cmds.listRelatives(curve, s=True)[0]
    cmds.setAttr(f"{shape}.dispCV", 1)
    
    return curve, shape


# =========================
# 3. LOCATORS + CV CONNECTION
# =========================
def create_locators_and_connect(shape, positions):
    locators = []
    
    for i, pos in enumerate(positions):
        loc = cmds.spaceLocator(name=f"spineLoc_ctrl_{i+1:03}")[0]
        cmds.xform(loc, ws=True, t=pos)
        
        cmds.connectAttr(f"{loc}.translate", f"{shape}.controlPoints[{i}]")
        
        locators.append(loc)
    
    return locators


# =========================
# 4. DECOMPOSE MATRIX (PRO)
# =========================
def connect_with_decompose(locators, shape):
    for i, loc in enumerate(locators):
        node = cmds.createNode("decomposeMatrix", name=f"decomposeMatrix_{i+1:03}")
        
        cmds.connectAttr(f"{loc}.worldMatrix[0]", f"{node}.inputMatrix")
        cmds.connectAttr(f"{node}.outputTranslate", f"{shape}.controlPoints[{i}]", force=True)


# =========================
# 5. CREAR CONTROLES (CIRCULOS)
# =========================
def create_controls(locators):
    ctrls = []
    
    for i, loc in enumerate(locators):
        ctrl = cmds.circle(name=f"ctrlShape_{i+1:03}", nr=(0,1,0))[0]
        
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.parent(shape, loc, r=True, s=True)
        cmds.delete(ctrl)
        
        ctrls.append(loc)
    
    return ctrls


# =========================
# 6. JERARQUIA ROOT
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
# 7. TARGETS + POC
# =========================
def create_targets(shape):
    targets = []
    
    for i in range(NUM_JOINTS):
        t = cmds.spaceLocator(name=f"spineTarget_ctrl_{i+1:03}")[0]
        
        poc = cmds.createNode("pointOnCurveInfo", name=f"poc_{i+1:03}")
        
        cmds.connectAttr(f"{shape}.worldSpace[0]", f"{poc}.inputCurve")
        cmds.connectAttr(f"{poc}.position", f"{t}.translate")
        
        param = i / (NUM_JOINTS - 1)
        cmds.setAttr(f"{poc}.parameter", param)
        
        targets.append(t)
    
    return targets


# =========================
# 8. AIM CONSTRAINTS
# =========================
def create_aim_constraints(targets):
    for i in range(len(targets)-1):
        cmds.aimConstraint(
            targets[i+1], targets[i],
            aimVector=(1,0,0),
            upVector=(0,1,0),
            worldUpType="vector"
        )


# =========================
# 9. JOINTS FOLLOW TARGETS
# =========================
def connect_joints_to_targets(joints, targets):
    for j, t in zip(joints, targets):
        cmds.parentConstraint(t, j, mo=True)



