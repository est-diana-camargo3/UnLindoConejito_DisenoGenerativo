
import importlib
import maya.cmds as cmds
import proyectofinal02.funcionesFK as funcionesFK
import proyectofinal02.sistemaIKFKleg as sistemaIKFKleg
import proyectofinal02.sistemaIKFKleg as sistemaIKFKspline
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
def crear_master_control():

    ctrl = cmds.circle(
        n="MASTER_CTRL",
        nr=(0,1,0),
        r=40
    )[0]

    root = cmds.group(ctrl, n="MASTER_CTRL_ROOT")

    cmds.parent("RIG_GRP", ctrl)
    cmds.parent("GEO_GRP", ctrl)

    print("✅ MASTER CTRL creado")

    return ctrl

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

def crear_controles_anatomicos():

    controles = {}

    # =========================
    # COG / PELVIS
    # =========================

    size = funcionesFK.tamano_desde_geometria(
        "Tronco_Primitiva_010",
        1.3
    )

    cog = cmds.circle(
        n="COG_CTRL",
        nr=(0,1,0),
        r=size
    )[0]

    cog_offset = cmds.group(
        cog,
        n="COG_CTRL_OFFSET"
    )

    cmds.delete(
        cmds.parentConstraint(
            "FK_Joint_08_Interno_ColumnaCadera",
            cog_offset
        )
    )

    controles["cog"] = cog

    # =========================
    # CHEST
    # =========================

    chest = cmds.circle(
        n="CHEST_CTRL",
        nr=(0,1,0),
        r=size * 0.8
    )[0]

    chest_offset = cmds.group(
        chest,
        n="CHEST_CTRL_OFFSET"
    )

    cmds.delete(
        cmds.parentConstraint(
            "FK_Joint_18_Medio_ColumnaCuello",
            chest_offset
        )
    )

    controles["chest"] = chest

    # =========================
    # HEAD
    # =========================

    head_size = funcionesFK.tamano_desde_geometria(
        "Cabeza_Primitiva_001"
    )

    head = cmds.circle(
        n="HEAD_CTRL",
        nr=(0,1,0),
        r=head_size
    )[0]

    head_offset = cmds.group(
        head,
        n="HEAD_CTRL_OFFSET"
    )

    cmds.delete(
        cmds.parentConstraint(
            "FK_Joint_19_ColumnaFrente",
            head_offset
        )
    )

    controles["head"] = head

    print("✅ Controles anatómicos creados")

    return controles

def crear_jerarquia_anatomica():

    # =========================
    # MASTER -> COG
    # =========================

    cmds.parent(
        "COG_CTRL_OFFSET",
        "MASTER_CTRL"
    )

    # =========================
    # COG -> CHEST
    # =========================

    cmds.parent(
        "CHEST_CTRL_OFFSET",
        "COG_CTRL"
    )

    # =========================
    # CHEST -> HEAD
    # =========================

    cmds.parent(
        "HEAD_CTRL_OFFSET",
        "CHEST_CTRL"
    )

    print("✅ Jerarquía anatómica creada")

def conectar_columna_a_controles():

    cmds.parentConstraint(
        "COG_CTRL",
        "FK_root_08_Interno_ColumnaCadera",
        mo=True
    )

    cmds.parentConstraint(
        "CHEST_CTRL",
        "FK_root_18_Medio_ColumnaCuello",
        mo=True
    )

    cmds.parentConstraint(
        "HEAD_CTRL",
        "FK_root_19_ColumnaFrente",
        mo=True
    )

    print("✅ Columna conectada")


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

    sistemas = [
        {
            "fk": lista_fk["brazoR_FK"],
            "ik": [
                "IK_Joint_15_Interno_ManoDerecha",
                "IK_Joint_16_medio_ManoDerecha",
                "IK_Joint_17_Externo_ManoDerecha"
            ],
            "main": [
                "MAIN_Joint_15_Interno_ManoDerecha",
                "MAIN_Joint_16_medio_ManoDerecha",
                "MAIN_Joint_17_Externo_ManoDerecha"
            ],
            "meshes": [
                "ManoDerecha_Primitiva_012"
            ],
            "prefix": "BrazoR"
        }
    ]

    resultados = {}
    for s in sistemas:

        meshes_sistema = s.get("meshes", meshes)
        resultado = sistemaIKFKspline.crear_sistema_ikfk(
            fk_chain=s["fk"],
            ik_chain=s["ik"],
            main_chain=s["main"],
            meshes=meshes_sistema,
            prefix=s["prefix"],
            joint_attr=s["main"][0]
        )

        resultados[s["prefix"]] = resultado

        for mesh in meshes_sistema:
            if not cmds.objExists(mesh):
                cmds.warning(f"bind_skin_cube: mesh no existe -> {mesh}")
                continue

            sistemaIKFKspline.bind_skin_cube(
                mesh,
                s["main"]
            )

    print("✅ FKIK GENERAL COMPLETO")

    return resultados
# endregion
