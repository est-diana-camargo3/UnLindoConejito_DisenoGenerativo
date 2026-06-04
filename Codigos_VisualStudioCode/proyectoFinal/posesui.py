import maya.cmds as cmds


VENTANA_POSES = "posesConejitoUI"
SUAVIDAD_POSE = 0.55
POSES_CLOSE_SCRIPTJOB = None


def _set_radiobotones_fkik(activos):
    for radio in ("radio_fk", "radio_ik"):
        if cmds.control(radio, exists=True):
            cmds.radioButton(radio, edit=True, enable=activos)


def _seleccionar_radio_fk():
    if cmds.control("radio_fk", exists=True):
        cmds.radioButton("radio_fk", edit=True, select=True)


def _bloquear_fkik_mientras_poses(*args):
    cambiar_fkik(0)
    _seleccionar_radio_fk()
    _set_radiobotones_fkik(False)


def _reactivar_fkik_al_cerrar_poses(*args):
    global POSES_CLOSE_SCRIPTJOB

    cambiar_fkik(0)
    _seleccionar_radio_fk()
    _set_radiobotones_fkik(True)
    POSES_CLOSE_SCRIPTJOB = None


def _objeto(nombre):
    if cmds.objExists(nombre):
        return nombre

    coincidencias = cmds.ls("*:" + nombre) or []
    if coincidencias:
        return coincidencias[0]

    return None


def _set_attr_seguro(objeto, atributo, valor):
    obj = _objeto(objeto)

    if not obj:
        cmds.warning(f"No existe {objeto}")
        return

    attr = obj + "." + atributo

    if not cmds.objExists(attr):
        cmds.warning(f"No existe {attr}")
        return

    try:
        cmds.setAttr(attr, valor)
    except Exception as e:
        cmds.warning(f"No se pudo cambiar {attr}: {e}")


def _set_vector(objeto, atributos, valores):
    for atributo, valor in zip(atributos, valores):
        _set_attr_seguro(objeto, atributo, valor)


def _mover(objeto, x=0, y=0, z=0):
    _set_vector(objeto, ("translateX", "translateY", "translateZ"), (x, y, z))


def _rotar(objeto, x=0, y=0, z=0):
    _set_vector(objeto, ("rotateX", "rotateY", "rotateZ"), (x, y, z))


def _mover_suave(objeto, x=0, y=0, z=0):
    _mover(objeto, x * SUAVIDAD_POSE, y * SUAVIDAD_POSE, z * SUAVIDAD_POSE)


def _rotar_suave(objeto, x=0, y=0, z=0):
    _rotar(objeto, x * SUAVIDAD_POSE, y * SUAVIDAD_POSE, z * SUAVIDAD_POSE)


def _controles_animables():
    patrones = [
        "*_FK_CTRL_*",
        "*_PROXY_LOC_*",
    ]

    controles = []

    for patron in patrones:
        for obj in cmds.ls(patron, type="transform") or []:
            nombre = obj.split(":")[-1]

            if nombre.endswith("_OFFSET") or nombre.endswith("_AUTO"):
                continue

            if nombre.endswith("_GRP") or nombre == "CTRL_GRP":
                continue

            if obj not in controles:
                controles.append(obj)

    return controles


def cambiar_fkik(valor):
    for obj in cmds.ls(type="transform") or []:
        if cmds.attributeQuery("FKIK", node=obj, exists=True):
            try:
                cmds.setAttr(obj + ".FKIK", valor)
                print(f"FKIK cambiado a {valor} en {obj}")
            except Exception as e:
                cmds.warning(f"No se pudo cambiar FKIK en {obj}: {e}")


def pose_default(*args):
    for obj in _controles_animables():
        for attr in ("translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"):
            if cmds.objExists(obj + "." + attr):
                try:
                    cmds.setAttr(obj + "." + attr, 0)
                except Exception:
                    pass

        for attr in ("scaleX", "scaleY", "scaleZ"):
            if cmds.objExists(obj + "." + attr):
                try:
                    cmds.setAttr(obj + "." + attr, 1)
                except Exception:
                    pass

    cambiar_fkik(0)
    _seleccionar_radio_fk()
    cmds.select(clear=True)
    print("Pose default aplicada")


def pose_1(*args):
    pose_default()

    _mover_suave("OrejaL_PROXY_LOC_001", 0, 0, 5.30309)
    _mover_suave("BrazoL_PROXY_LOC_001", 0, 9.227746, 11.3734)
    _mover_suave("BrazoR_PROXY_LOC_001", 0, -7.617509, 0)
    _mover_suave("PiernaL_PROXY_LOC_001", 0, 0, 9.77873)
    _mover_suave("PiernaR_PROXY_LOC_001", 0, 0, -5.89242)

    cmds.select(clear=True)
    print("Pose 1 aplicada")


def pose_2(*args):
    pose_default()

    _mover_suave("BrazoR_PROXY_LOC_001", -3.785839, -8.227251, -7.619854)
    _mover_suave("BrazoL_PROXY_LOC_001", 0, -7.927215, -4.935207)
    _mover_suave("OrejaR_PROXY_LOC_001", 8.861044, 0, -10.941882)
    _mover_suave("OrejaL_PROXY_LOC_001", -9.45153, 0, -8.763433)
    _mover_suave("PiernaR_PROXY_LOC_001", -3.185315, 0, 0)
    _mover_suave("PiernaL_PROXY_LOC_001", 2.435349, 0, 0)

    cmds.select(clear=True)
    print("Pose 2 aplicada")


def abrir_ui(*args):
    global POSES_CLOSE_SCRIPTJOB

    if cmds.window(VENTANA_POSES, exists=True):
        cmds.deleteUI(VENTANA_POSES)

    if POSES_CLOSE_SCRIPTJOB and cmds.scriptJob(exists=POSES_CLOSE_SCRIPTJOB):
        cmds.scriptJob(kill=POSES_CLOSE_SCRIPTJOB, force=True)
        POSES_CLOSE_SCRIPTJOB = None

    _bloquear_fkik_mientras_poses()

    ventana = cmds.window(
        VENTANA_POSES,
        title="Poses del conejito",
        sizeable=False,
        widthHeight=(220, 170)
    )

    POSES_CLOSE_SCRIPTJOB = cmds.scriptJob(
        uiDeleted=[VENTANA_POSES, _reactivar_fkik_al_cerrar_poses],
        protected=True
    )

    cmds.columnLayout(adjustableColumn=True, rowSpacing=8, columnOffset=("both", 12))
    cmds.separator(h=8, style="none")
    cmds.button(label="Pose 1", height=30, command=pose_1)
    cmds.button(label="Pose 2", height=30, command=pose_2)
    cmds.separator(h=6, style="in")
    cmds.button(label="Pose default", height=30, command=pose_default)
    cmds.separator(h=8, style="none")

    cmds.showWindow(ventana)
    return ventana
