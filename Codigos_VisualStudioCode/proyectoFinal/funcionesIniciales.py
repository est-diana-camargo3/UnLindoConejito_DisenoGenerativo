
import importlib
import maya.cmds as cmds
import proyectoFinal.funcionesFK as funcionesFK
import proyectoFinal.sistemaIKFKleg as sistemaIKFKleg
import proyectoFinal.sistemaIKFKspline as sistemaIKFKspline
importlib.reload(funcionesFK)
importlib.reload(sistemaIKFKleg)
importlib.reload(sistemaIKFKspline)
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Cambiar unidades a centimetros.                                ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝

cmds.currentUnit(linear="centimeter") #Cambiar unidades a centimetros, facilita la creación de los objetos 
# Windows → Settings/Preferences → Preferences → Settings → Working Units  →"Linear"  → "centimeter"

#region jerarquia
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Crear una jerarquia general                                    ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝

def crear_jerarquia_general():

    grupos = {

        "master": "Conejo_RIG_GRP",

        "geo": "GEO_GRP",
        "rig": "RIG_GRP",

        "fk": "FK_GRP",
        "ik": "IK_GRP",
        "main": "MAIN_GRP",

        "ctrl": "CTRL_GRP",
        "loc": "LOCATORS_GRP",
        "spline": "SPLINE_GRP",
        "systems": "SYSTEMS_GRP"
    }

    for g in grupos.values():
        if not cmds.objExists(g):
            cmds.group(em=True, n=g)

    # =========================
    # PARENTS
    # =========================

    cmds.parent(grupos["geo"], grupos["master"])
    cmds.parent(grupos["rig"], grupos["master"])

    cmds.parent(
        grupos["fk"],
        grupos["ik"],
        grupos["main"],
        grupos["ctrl"],
        grupos["loc"],
        grupos["spline"],
        grupos["systems"],
        grupos["rig"]
    )

    print("✅ Jerarquía general creada")

    return grupos

def organizar_cadenas_principales():

    joints = cmds.ls(type="joint")

    for j in joints:

        raiz = cmds.listRelatives(j, parent=True)

        # SOLO raíces
        if raiz:
            continue

        if j.startswith("FK_"):
            cmds.parent(j, "FK_GRP")

        elif j.startswith("IK_"):
            cmds.parent(j, "IK_GRP")

        elif j.startswith("MAIN_"):
            cmds.parent(j, "MAIN_GRP")

    print("✅ Cadenas organizadas")

def crear_grupo_sistema(nombre):

    grp = f"{nombre}_SYSTEM_GRP"

    if not cmds.objExists(grp):
        grp = cmds.group(em=True, n=grp)

        cmds.parent(grp, "SYSTEMS_GRP")

    return grp

def organizar_chain_system(
        nombre,
        curve,
        locators,
        targets,
        roots
    ):

    sistema_grp = crear_grupo_sistema(nombre)

    # =========================
    # SUBGRUPOS
    # =========================

    curve_grp = cmds.group(em=True, n=f"{nombre}_CURVES_GRP")
    loc_grp = cmds.group(em=True, n=f"{nombre}_LOCATORS_GRP")
    ctrl_grp = cmds.group(em=True, n=f"{nombre}_CTRLS_GRP")
    target_grp = cmds.group(em=True, n=f"{nombre}_TARGETS_GRP")

    cmds.parent(
        curve_grp,
        loc_grp,
        ctrl_grp,
        target_grp,
        sistema_grp
    )

    # =========================
    # PARENT
    # =========================

    cmds.parent(curve, curve_grp)

    if locators:
        cmds.parent(locators, loc_grp)

    if targets:
        cmds.parent(targets, target_grp)

    if roots:
        cmds.parent(roots, ctrl_grp)

    print(f"✅ Sistema organizado -> {nombre}")


# endregion




def conectar_extremidades():

    # =========================
    # BRAZOS
    # =========================

    cmds.parent(
        "BrazoL_IK_CTRL_001_OFFSET",
        "CHEST_CTRL"
    )

    cmds.parent(
        "BrazoR_IK_CTRL_001_OFFSET",
        "CHEST_CTRL"
    )

    # =========================
    # PIERNAS
    # =========================

    cmds.parent(
        "PiernaL_IK_CTRL_001_OFFSET",
        "COG_CTRL"
    )

    cmds.parent(
        "PiernaR_IK_CTRL_001_OFFSET",
        "COG_CTRL"
    )

    print("✅ Extremidades conectadas")


def conectar_partes_secundarias():

    # =========================
    # OREJAS
    # =========================

    cmds.parent(
        "EarL_SYSTEM_GRP",
        "HEAD_CTRL"
    )

    cmds.parent(
        "EarR_SYSTEM_GRP",
        "HEAD_CTRL"
    )

    # =========================
    # COLA
    # =========================

    cmds.parent(
        "Tail_SYSTEM_GRP",
        "COG_CTRL"
    )

    print("✅ Orejas y cola conectadas")


#region fkik
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  generar sistema FKIK general                                   ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝


def crear_sistema_fkik(lista_fk, resultado_dup, meshes):

    def rename_chain(joints, prefix):
        return [j.replace("FK_", prefix + "_", 1) for j in joints]

    sistemas = [
        # extremidades con IK-RP
        {
            "module": sistemaIKFKleg,
            "fk": lista_fk["brazoR_FK"],
            "ik": rename_chain(lista_fk["brazoR_FK"], "IK"),
            "main": rename_chain(lista_fk["brazoR_FK"], "MAIN"),
            "meshes": ["ManoDerecha_Primitiva_012"],
            "prefix": "BrazoR"
        },
        {
            "module": sistemaIKFKleg,
            "fk": lista_fk["brazoL_FK"],
            "ik": rename_chain(lista_fk["brazoL_FK"], "IK"),
            "main": rename_chain(lista_fk["brazoL_FK"], "MAIN"),
            "meshes": ["ManoIzquierda_Primitiva_011"],
            "prefix": "BrazoL"
        },
        {
            "module": sistemaIKFKleg,
            "fk": lista_fk["piernaR_FK"],
            "ik": rename_chain(lista_fk["piernaR_FK"], "IK"),
            "main": rename_chain(lista_fk["piernaR_FK"], "MAIN"),
            "meshes": ["PieDerecho_Primitiva_009"],
            "prefix": "PiernaR"
        },
        {
            "module": sistemaIKFKleg,
            "fk": lista_fk["piernaL_FK"],
            "ik": rename_chain(lista_fk["piernaL_FK"], "IK"),
            "main": rename_chain(lista_fk["piernaL_FK"], "MAIN"),
            "meshes": ["PieIzquierdo_Primitiva_008"],
            "prefix": "PiernaL"
        },
        {
            "module": sistemaIKFKleg,
            "fk": lista_fk["orejaR_FK"],
            "ik": rename_chain(lista_fk["orejaR_FK"], "IK"),
            "main": rename_chain(lista_fk["orejaR_FK"], "MAIN"),
            "meshes": ["Oreja_Derecha_007"],
            "prefix": "OrejaR"
        },
        {
            "module": sistemaIKFKleg,
            "fk": lista_fk["orejaL_FK"],
            "ik": rename_chain(lista_fk["orejaL_FK"], "IK"),
            "main": rename_chain(lista_fk["orejaL_FK"], "MAIN"),
            "meshes": ["Oreja_Izquierda_006"],
            "prefix": "OrejaL"
        },
        {
            "module": sistemaIKFKleg,
            "fk": lista_fk["cola_FK"],
            "ik": rename_chain(lista_fk["cola_FK"], "IK"),
            "main": rename_chain(lista_fk["cola_FK"], "MAIN"),
            "meshes": ["Cola_Primitiva_013"],
            "prefix": "Cola"
        },
        # cabeza + tronco con IK spline
        {
            "module": sistemaIKFKspline,
            "fk": lista_fk["columna_FK"],
            "ik": rename_chain(lista_fk["columna_FK"], "IK"),
            "main": rename_chain(lista_fk["columna_FK"], "MAIN"),
            "meshes": ["Tronco_Primitiva_010", "Cabeza_Primitiva_001"],
            "prefix": "Columna"
        }
    ]

    resultados = {}
    for s in sistemas:

        missing = [obj for obj in (s["fk"] + s["ik"] + s["main"]) if not cmds.objExists(obj)]
        if missing:
            cmds.warning(f"No se puede crear el sistema {s['prefix']}: faltan joints -> {missing}")
            continue

        meshes_sistema = s.get("meshes", meshes)
        resultado = s["module"].crear_sistema_ikfk(
            fk_chain=s["fk"],
            ik_chain=s["ik"],
            main_chain=s["main"],
            meshes=meshes_sistema,
            prefix=s["prefix"],
            joint_attr=s["main"][0]
        )
       

        resultados[s["prefix"]] = resultado

        # este suavizado se hizo con el boton de suavizar desde el main directamente 
        for mesh in meshes_sistema:
            if not cmds.objExists(mesh):
                cmds.warning(f"bind_skin_cube: mesh no existe -> {mesh}")
                continue

            s["module"].bind_skin_cube(
                mesh,
                s["main"]
            )

    print("✅ FKIK GENERAL COMPLETO")

    return resultados




# endregion


