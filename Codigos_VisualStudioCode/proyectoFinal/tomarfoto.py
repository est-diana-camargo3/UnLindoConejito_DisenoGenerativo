import os

import maya.cmds as cmds
import maya.mel as mel


ANCHO_RENDER = 1280
ALTO_RENDER = 720
_JOB_GUARDADO_RENDER = None


def _set_attr_si_existe(attr, valor, tipo=None):
    if not cmds.objExists(attr):
        return

    try:
        if tipo:
            cmds.setAttr(attr, valor, type=tipo)
        else:
            cmds.setAttr(attr, valor)
    except Exception as e:
        cmds.warning(f"No se pudo configurar {attr}: {e}")


def _cargar_arnold():
    try:
        if not cmds.pluginInfo("mtoa", q=True, loaded=True):
            cmds.loadPlugin("mtoa", quiet=True)
    except Exception as e:
        cmds.warning(f"No se pudo cargar Arnold/mtoa: {e}")
        return False

    try:
        import mtoa.core as mtoa_core
        mtoa_core.createOptions()
    except Exception as e:
        cmds.warning(f"No se pudieron crear opciones Arnold: {e}")

    return True


def _camara_actual():
    panel = cmds.getPanel(withFocus=True)

    if panel and cmds.getPanel(typeOf=panel) == "modelPanel":
        camara = cmds.modelEditor(panel, q=True, camera=True)

        if camara and cmds.objExists(camara):
            return camara

    paneles = cmds.getPanel(type="modelPanel") or []

    for panel in paneles:
        camara = cmds.modelEditor(panel, q=True, camera=True)

        if camara and cmds.objExists(camara):
            return camara

    return "persp"


def _shape_camara(camara):
    if not camara or not cmds.objExists(camara):
        return "perspShape"

    if cmds.nodeType(camara) == "camera":
        return camara

    shapes = cmds.listRelatives(camara, shapes=True, type="camera") or []

    if shapes:
        return shapes[0]

    return camara


def _configurar_arnold(camara):
    cmds.setAttr(
        "defaultRenderGlobals.currentRenderer",
        "arnold",
        type="string"
    )

    _set_attr_si_existe("defaultResolution.width", ANCHO_RENDER)
    _set_attr_si_existe("defaultResolution.height", ALTO_RENDER)
    _set_attr_si_existe("defaultResolution.deviceAspectRatio", float(ANCHO_RENDER) / ALTO_RENDER)
    _set_attr_si_existe("defaultRenderGlobals.imageFormat", 8)
    _set_attr_si_existe("defaultArnoldRenderOptions.AASamples", 3)
    _set_attr_si_existe("defaultArnoldRenderOptions.abortOnError", 0)

    for shape in cmds.ls(type="camera") or []:
        _set_attr_si_existe(shape + ".renderable", 0)

    shapes = cmds.listRelatives(camara, shapes=True, type="camera") or []

    if shapes:
        _set_attr_si_existe(shapes[0] + ".renderable", 1)
    elif cmds.nodeType(camara) == "camera":
        _set_attr_si_existe(camara + ".renderable", 1)

    try:
        mel.eval("updateRenderOverride;")
    except Exception:
        pass


def _abrir_render_view():
    try:
        mel.eval("RenderViewWindow;")
    except Exception:
        pass

    cmds.refresh(force=True)

    try:
        cmds.pause(seconds=0.75)
    except Exception:
        pass


def _renderizar_arnold(camara):
    camara_shape = _shape_camara(camara)

    _abrir_render_view()

    try:
        mel.eval(
            f'renderWindowEditor -e -currentCamera "{camara_shape}" renderView;'
        )
    except Exception as e:
        cmds.warning(f"No se pudo asignar la camara al Render View: {e}")

    try:
        mel.eval("renderWindowRender redoPreviousRender renderView;")
        print(f"Render View Arnold ejecutado con {camara_shape}")
        return True
    except Exception as e:
        cmds.warning(f"No funciono renderWindowRender: {e}")

    try:
        mel.eval(
            f'arnoldRender -cam "{camara_shape}" '
            f'-w {ANCHO_RENDER} -h {ALTO_RENDER};'
        )
        _abrir_render_view()
        print(f"Arnold render ejecutado con {camara_shape}")
        return True
    except Exception as e:
        cmds.warning(f"No funciono arnoldRender con shape: {e}")

    return False


def _ruta_foto():
    carpeta_actual = os.path.dirname(__file__)
    carpeta_fotos = os.path.join(carpeta_actual, "fotos")

    if not os.path.exists(carpeta_fotos):
        os.makedirs(carpeta_fotos)

    return os.path.join(carpeta_fotos, "render.jpg")


def _esta_renderizando():
    try:
        condiciones = cmds.scriptJob(listConditions=True) or []

        if "rendering" not in condiciones:
            return False

        return bool(cmds.isTrue("rendering"))
    except Exception:
        return False






def tomar_foto(*args):
    if not _cargar_arnold():
        return

    camara = _camara_actual()
    _configurar_arnold(camara)
    cmds.lookThru(camara)
    cmds.refresh(force=True)

    try:
        cmds.pause(seconds=0.5)
    except Exception:
        pass

    if not _renderizar_arnold(camara):
        cmds.warning("No se pudo iniciar el render Arnold")
        return

    print(f"Render Arnold iniciado con camara: {camara}")
