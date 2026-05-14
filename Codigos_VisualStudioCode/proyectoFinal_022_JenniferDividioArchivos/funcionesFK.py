import maya.cmds as cmds
      
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Sistema FK                                                     ║
#                         ╚═════════════════════════════════════════════════════════════════╝

def tamano_desde_geometria(objeto, multiplicador=1.2):

    bbox = cmds.exactWorldBoundingBox(objeto)

    size_x = bbox[3] - bbox[0]
    size_y = bbox[4] - bbox[1]
    size_z = bbox[5] - bbox[2]

    tamano = max(size_x, size_y, size_z)

    return tamano * multiplicador

# region pivotes gizmos
# =========================
# UBICAR PIVOTES EN EL CENTRO DE LAS PRIMITIVAS
# =========================

"""
Como movi los pivotes a la esquina superior izquierda de la cara frontal de cada cubo, 
debo devolverlos al centro para poder obtener las coordenadas del centro en x,y,z de cada forma 
y colocar los joints en el x,y que me de  el z si debe ser en el centro de la profundidad...
todos coplanares 
"""
def mostrar_gizmos_pivotes():
    # Mostramos los gizmos de los pivotes para poder ver donde esta el punto de ancla o pivote 
    # Display → Transform Display → Pivots    
    objetos = [
        "Cabeza_Primitiva_001",
        "Oreja_Izquierda_006", "Oreja_Derecha_007",
        "Tronco_Primitiva_010",
        "ManoIzquierda_Primitiva_011", "ManoDerecha_Primitiva_012",
        "PieIzquierdo_Primitiva_008", "PieDerecho_Primitiva_009",
        "Cola_Primitiva_013"
    ]
    for obj in objetos: 
        if cmds.objExists(obj):
            cmds.setAttr(obj + ".displayLocalAxis", 1)

#Por si en un futuro queremos ocultar los gizmos de los pivotes 
def ocultar_gizmos_pivotes():
    objetos = [
        "Cabeza_Primitiva_001",
        "Oreja_Izquierda_006", "Oreja_Derecha_007",
        "Tronco_Primitiva_010",
        "ManoIzquierda_Primitiva_011", "ManoDerecha_Primitiva_012",
        "PieIzquierdo_Primitiva_008", "PieDerecho_Primitiva_009",
        "Cola_Primitiva_013"
    ]
    
    for obj in objetos:
        if cmds.objExists(obj):
            cmds.setAttr(obj + ".displayLocalAxis", 0)
#endregion

# region Crear Joints
# =========================
# CREAR JOINTS
# =========================

"""
Yo inicie a dibujar la cabeza del conejo en 0,0,0 y tiene una profundidad en z de -m*10/2,
Por lo tanto la mitad de la profundidad de la cabeza es z= -(m*10/2)/2 es decir z= -m*10/4
Ese es el plano central del conejo en z, ahi voy a dibujar los joints de manera coplanar 
Porque es el plano que todas las primitivas comparten.
# """ 

# =========================
# Obtenemos posicion de pivote y caja envolvente con extremos de geometria de cada primitiva.
# =========================

def datos_primitiva(obj, PlanoCoplanarEnZ):
    # Devuelve una lista [X, Y, Z] con la posicion del pivote  de la primitiva,
    #  para colocar joints EXACTAMENTE en el centro x,y en z si es (z= -m*10/4)
    centro = cmds.xform(obj, q=True, ws=True, rp=True) 
    #devuelve una lista de [xmin, ymin, zmin, xmax, ymax, zmax] 
    # para encontrar extremos de la geometría y colocar los 2 joints de las puntas o extremos (orejas, pies, etc.)
    bbox = cmds.exactWorldBoundingBox(obj)     
    return {
        "centro": (centro[0], centro[1], PlanoCoplanarEnZ),
        "xmin": bbox[0],
        "ymin": bbox[1],
        "zmin": bbox[2],
        "xmax": bbox[3],
        "ymax": bbox[4],
        "zmax": bbox[5]
    }

# Crear Y RENOMBRAR  joints 
# =========================
# Crear joints coplanares en z= m/4 (24 JOINTS)
# Renombrar joints (Interno, Medio, end)
# =========================

def crear_joints_coplanares(m):

    #grafica representativa:
    """ 
    .......................................................................
    .....................(22)...................(25).......................
    .......................|.....................|.........................           
    .....................(21)...................(24).......................    <-- Orejas
    .......................|.....................|.........................
    .....................(20)...................(23).......................
    .......................__________(19)_________.........................      <--Frente
    ......................|            |          |........................
    ......................|       O         O     |........................
    ......................|            |          |........................
    ......................|            O          |........................
    ......................|            |          |........................
    ......................|         ___|___       |........................
    ......................|            |          |........................
    ......................._______________________.........................
    ................_________________(18)________________..................       <--Cuello
    ................|                 |                 |..................
    ................|                 |                 |..................
    ................|                 |                 |..................
    ..(14)-(13)-(12)|___________     |      ____________|(15)-(16)-(17)....	      <-- Manos
    ................|           \     |     /           |..................
    ................|               (8)         b       |(9)-(10)-(11).....      <-- Cola
    ................|                 |                 |..................
    ................|                 |                 |..................
    ................|________________(1)________________|.................. 
    ......................(2)....................(5).......................
    .......................|......................|........................           
    ......................(3)....................(6).......................       <-- Orejas
    .......................|......................|........................
    ......................(4)....................(7).......................
    .......................................................................
           
    """
    cmds.select(clear=True)

    PlanoCoplanarEnZ = -(m*10)/4

    # =====================================================
    # DATOS PRIMITIVAS
    # =====================================================

    cabeza = datos_primitiva("Cabeza_Primitiva_001",PlanoCoplanarEnZ)
    tronco = datos_primitiva("Tronco_Primitiva_010",PlanoCoplanarEnZ)
    brazoR = datos_primitiva("ManoDerecha_Primitiva_012", PlanoCoplanarEnZ)
    brazoL = datos_primitiva("ManoIzquierda_Primitiva_011",PlanoCoplanarEnZ)
    pieR = datos_primitiva("PieDerecho_Primitiva_009",PlanoCoplanarEnZ)
    pieL = datos_primitiva("PieIzquierdo_Primitiva_008",PlanoCoplanarEnZ)
    orejaR = datos_primitiva("Oreja_Derecha_007",PlanoCoplanarEnZ)
    orejaL = datos_primitiva("Oreja_Izquierda_006", PlanoCoplanarEnZ)
    cola = datos_primitiva("Cola_Primitiva_013",PlanoCoplanarEnZ)

    # =====================================================
    # ESPINA
    # =====================================================

    raiz = cmds.joint(n="FK_Joint_01_Interno_Columna",
        p=(tronco["centro"][0],tronco["ymin"],PlanoCoplanarEnZ)
    )
    espina = cmds.joint(n="FK_Joint_08_Interno_ColumnaCadera",
        p=(tronco["centro"][0],tronco["centro"][1],PlanoCoplanarEnZ)
    )
    cuello = cmds.joint(n="FK_Joint_18_Medio_ColumnaCuello",
        p=(tronco["centro"][0],tronco["ymax"],PlanoCoplanarEnZ )
    )
    cabeza = cmds.joint(n="FK_Joint_19_ColumnaFrente",
        p=(cabeza["centro"][0], cabeza["ymax"], PlanoCoplanarEnZ)
    )

    # =====================================================
    # BRAZO DERECHO
    # =====================================================

    cmds.select(cuello)

    hombroD = cmds.joint(n="FK_Joint_15_Interno_ManoDerecha",
        p=(brazoR["xmax"],brazoR["centro"][1],PlanoCoplanarEnZ)
    )
    codoD = cmds.joint(n="FK_Joint_16_medio_ManoDerecha",
        p=(brazoR["centro"][0],brazoR["centro"][1], PlanoCoplanarEnZ)
    )
    munecaD = cmds.joint(n="FK_Joint_17_Externo_ManoDerecha",
        p=(brazoR["xmin"], brazoR["centro"][1], PlanoCoplanarEnZ)
    )

    # =====================================================
    # BRAZO IXQUIERDO
    # =====================================================

    cmds.select(cuello)

    hombroI = cmds.joint(n="FK_Joint_12_Interno_ManoIzquierda",
        p=(brazoL["xmin"],brazoL["centro"][1],PlanoCoplanarEnZ)
    )
    codoI = cmds.joint(n="FK_Joint_13_medio_ManoIzquierda",
        p=(brazoL["centro"][0],brazoL["centro"][1],PlanoCoplanarEnZ )
    )
    munecaI = cmds.joint( n="FK_Joint_14_Externo_ManoIzquierda",
        p=( brazoL["xmax"],brazoL["centro"][1], PlanoCoplanarEnZ)
    )

    # =====================================================
    # PIERNA DERECHA
    # =====================================================

    cmds.select(raiz)

    piernaD = cmds.joint(n="FK_Joint_05_Interno_PieDerecho",
        p=(pieR["centro"][0],pieR["ymax"],PlanoCoplanarEnZ)
    )
    rodillaD = cmds.joint(n="FK_Joint_06_medio_PieDerecho",
        p=(pieR["centro"][0],pieR["centro"][1],PlanoCoplanarEnZ)
    )
    pieD = cmds.joint(n="FK_Joint_07_Externo_PieDerecho",
        p=(pieR["centro"][0],pieR["ymin"],PlanoCoplanarEnZ)
    )

    # =====================================================
    # PIERNA IZQUIERDA
    # =====================================================

    cmds.select(raiz)

    piernaI = cmds.joint(n="FK_Joint_02_Interno_PieIzquierdo",
        p=(pieL["centro"][0],pieL["ymax"],PlanoCoplanarEnZ)
    )
    rodillaI = cmds.joint( n="FK_Joint_03_medio_PieIzquierdo",
        p=(pieL["centro"][0],pieL["centro"][1], PlanoCoplanarEnZ )
    )
    pieI = cmds.joint( n="FK_Joint_04_Externo_PieIzquierdo",
        p=(pieL["centro"][0],pieL["ymin"], PlanoCoplanarEnZ)
    )

    # =====================================================
    # OREJA DERECHA
    # =====================================================

    cmds.select(cabeza)

    orejaBaseD = cmds.joint(n="FK_Joint_23_Interno_OrejaDerecha",
        p=(orejaR["centro"][0],orejaR["ymin"], PlanoCoplanarEnZ)
    )
    orejaMidD = cmds.joint(n="FK_Joint_24_Medio_OrejaDerecha",
        p=(orejaR["centro"][0],orejaR["centro"][1],PlanoCoplanarEnZ )
    )
    orejaPuntaD = cmds.joint(n="FK_Joint_25_Externo_OrejaDerecha",
        p=(orejaR["centro"][0],orejaR["ymax"], PlanoCoplanarEnZ)
    )

    # =====================================================
    # OREJA IZQUIERDA
    # =====================================================

    cmds.select(cabeza)

    orejaBaseI = cmds.joint(n="FK_Joint_20_Interno_OrejaIzquierda",
        p=(orejaL["centro"][0],orejaL["ymin"],PlanoCoplanarEnZ )
    )
    orejaMidI = cmds.joint(n="FK_Joint_21_Medio_OrejaIzquierda",
        p=(orejaL["centro"][0],orejaL["centro"][1],PlanoCoplanarEnZ)
    )
    orejaPuntaI = cmds.joint(n="FK_Joint_22_Externo_OrejaIzquierda",
        p=(orejaL["centro"][0],orejaL["ymax"],PlanoCoplanarEnZ)
    )

    # =====================================================
    # COLA
    # =====================================================

    cmds.select(raiz)

    centro_cola = cmds.xform(
        "Cola_Primitiva_013",
        q=True,
        ws=True,
        rp=True
    )

    colaBase = cmds.joint(
        n="FK_Joint_19_Interno_Cola",
        p=(
            centro_cola[0],
            centro_cola[1],
            cola["zmax"]
        )
    )

    colaMid = cmds.joint(
        n="FK_Joint_19_Medio_Cola",
        p=(
            centro_cola[0],
            centro_cola[1],
            centro_cola[2]
        )
    )

    colaFin = cmds.joint(
        n="FK_Joint_19_Externo_Cola",
        p=(
            centro_cola[0],
            centro_cola[1],
            cola["zmin"]
        )
    )
    # =====================================================
    # RIG FINAL
    # =====================================================

    rig = {

        "columna_FK": [raiz,espina,cuello,cabeza],
        "brazoR_FK": [hombroD,codoD, munecaD],
        "brazoL_FK": [hombroI,codoI,munecaI],
        "piernaR_FK": [piernaD,rodillaD,pieD],
        "piernaL_FK": [piernaI,rodillaI,pieI],
        "orejaR_FK": [orejaBaseD,orejaMidD,orejaPuntaD],
        "orejaL_FK": [orejaBaseI,orejaMidI,orejaPuntaI],
        "cola_FK": [colaBase,colaMid,colaFin]
    }

    print("RIG CREADO")
    return rig

# endregion

# region Orientar Joints
# =========================
# Orientar Joints
# =========================

#Definimos estas funciones para usarlas lineas mas adelante en la función de orientar joints()
def mostrar_gizmos_joints():
    joints = cmds.ls(type="joint")
    for j in joints:
        cmds.setAttr(j + ".displayLocalAxis", 1)

#Por si queremos ocultar los gizmos de los joints en un futuro
def ocultar_gizmos_joints():
    joints = cmds.ls(type="joint")
    for j in joints:
        cmds.setAttr(j + ".displayLocalAxis", 0)

# =========================
# Orientar cadenas
# =========================
#para orientar cadena por cadena, la llamo mas adelante 
def orientar_subcadena_FK(FK_talcadena, miorientJoint, eje_secundario): 
    #cadena, orientacion xyz x apunta al hijo, crece en y, z perpendicular
    # eje secunadario 
    cmds.select(clear=True)
    cmds.select(FK_talcadena[0])

    cmds.joint(
        edit=True,
        orientJoint=miorientJoint,
        secondaryAxisOrient=eje_secundario,
        children=True,
        zeroScaleOrient=True
    )

    # Nos aseguramos que el ultimo joint tenga sus valores de transformacion (rotacion y traslacion) 
    # excepto la escala en 0,0,0
    ultimo = FK_talcadena[-1]
    ultimo = FK_talcadena[-1]
    cmds.setAttr(ultimo + ".jointOrientX", 0)
    cmds.setAttr(ultimo + ".jointOrientY", 0)
    cmds.setAttr(ultimo + ".jointOrientZ", 0)


def orientar_joints_de_toda_la_cadena_FK(ListaDelSistemaFK):

    """
    la cola no tienen la misma orientacion que el resto del cuerpo porque no crecen verticalmente 
        sino hacia -z, por eso la orientamos al final y de manera independiente para que no afecte 
        la orientacion del resto del cuerpo.

        la razon por la que se parento y desemparento es para que las transformaciones del padre osea de la columna 
        no afecten al hijo osea  a la cola  y ya al final vuelvo vemos a conectar el padre con el hijo
          para no perder jerarquia 
    lo mismo pasa con los pies que no crecen verticalmente hcaia arriba  sino hacia abajo, 
    por eso parentmos y desemparentamos al final y de manera independiente para que no se vean afectados 
    por la la orientacion del papa columna.
    """
    cola = ListaDelSistemaFK["cola_FK"]
    piernaR = ListaDelSistemaFK["piernaR_FK"]
    piernaL = ListaDelSistemaFK["piernaL_FK"]
    orejaR = ListaDelSistemaFK["orejaR_FK"]
    orejaL = ListaDelSistemaFK["orejaL_FK"]


    raiz_cola = cola[0]
    raiz_piernaR = piernaR[0]
    raiz_piernaL = piernaL[0]
    raiz_orejaR = orejaR[0]
    raiz_orejaL = orejaL[0]


    # 1. Guardar padre original
    padre_Cola = cmds.listRelatives(raiz_cola, parent=True)
    padre_piernaR = cmds.listRelatives(raiz_piernaR, parent=True)
    padre_piernaL = cmds.listRelatives(raiz_piernaL, parent=True)
    padre_orejaR = cmds.listRelatives(raiz_orejaR, parent=True)
    padre_orejaL = cmds.listRelatives(raiz_orejaL, parent=True)


    # Desparentar cola y pies
    cmds.parent(raiz_cola, world=True)
    cmds.parent(raiz_piernaR, world=True)
    cmds.parent(raiz_piernaL, world=True)
    cmds.parent(raiz_orejaR, world=True)
    cmds.parent(raiz_orejaL, world=True)


    # 3. Orientar TODO menos la cola ni los pies 
    orientar_subcadena_FK(ListaDelSistemaFK["brazoR_FK"], "xyz", "ydown")
    orientar_subcadena_FK(ListaDelSistemaFK["brazoL_FK"], "xyz", "ydown")

    orientar_subcadena_FK(ListaDelSistemaFK["piernaR_FK"], "xyz", "yup")
    orientar_subcadena_FK(ListaDelSistemaFK["piernaL_FK"], "xyz", "ydown")

    orientar_subcadena_FK(ListaDelSistemaFK["orejaR_FK"], "xyz", "yup")
    orientar_subcadena_FK(ListaDelSistemaFK["orejaL_FK"], "xyz", "yup")

    orientar_subcadena_FK(ListaDelSistemaFK["cola_FK"], "xzy", "yup")
    orientar_subcadena_FK(ListaDelSistemaFK["columna_FK"], "xyz", "ydown")

    """
    la razon por la que se parento y desemparento es para que las transformaciones del padre no afecten al hijo.
    pero luego volvemos a conectar el padre con el hijo para no perder jerarquia 
    """

    # 5. Volver a parentar
    if padre_Cola:
        cmds.parent(raiz_cola, padre_Cola[0])
    if padre_piernaR:
        cmds.parent(raiz_piernaR, padre_piernaR[0])
    if padre_piernaL:
        cmds.parent(raiz_piernaL, padre_piernaL[0])
    if padre_orejaR:
        cmds.parent(raiz_orejaR, padre_orejaR[0])
    if padre_orejaL:
        cmds.parent(raiz_orejaL, padre_orejaL[0])

    mostrar_gizmos_joints()
    ocultar_gizmos_pivotes()

    print("✅ JOINTS ORIENTADOS POR SISTEMAS")

# endregion

# region Duplicar cadenas y renombrarlas de FK a IK y a MAIN
# =========================
# Duplicar cadenas y renombrarlas de FK a IK y a MAIN
# =========================

def duplicar_y_renombrar_cadenas_IK_y_MAIN():
    """
    Duplica la cadena FK del conejo y crea:
    - cadena IK
    - cadena MAIN
    SOLO cambia el prefijo FK_
    """

    raiz_fk = "FK_Joint_01_Interno_Columna"

    if not cmds.objExists(raiz_fk):
        cmds.warning("No existe la cadena FK del conejo")
        return

    def procesar(prefijo):
        dup = cmds.duplicate(raiz_fk, renameChildren=True)[0]

        jerarquia = cmds.listRelatives(dup, allDescendents=True, type="joint") or []
        jerarquia.append(dup)

        nueva_lista = []
        for j in jerarquia:
            base = j.replace("FK_", prefijo + "_")

            # quitar el 1 automático del duplicate
            if base.endswith("1"):
                base = base[:-1]

            nuevo_nombre = cmds.rename(j, base)
            nueva_lista.append(nuevo_nombre)

        return nueva_lista

    cadena_IK = procesar("IK")
    cadena_MAIN = procesar("MAIN")

    print("Cadenas IK y MAIN creadas y renombradas")

    return {
        "IK": cadena_IK,
        "MAIN": cadena_MAIN
    }


def ocultar_cadenas_IK_y_MAIN():
    joints = cmds.ls(type="joint")

    for j in joints:
        if j.startswith("IK_") or j.startswith("MAIN_"):
            cmds.setAttr(j + ".visibility", 0)

    print("🙈 IK y MAIN ocultas")

def mostrar_cadenas_IK_y_MAIN():
    joints = cmds.ls(type="joint")

    for j in joints:
        if j.startswith("IK_") or j.startswith("MAIN_"):
            cmds.setAttr(j + ".visibility", 1)

    print("👀 IK y MAIN visibles")

# endregion

# region CONSTRUCCION DE LA CADENA FK (AUTO, ROOT )
# =========================
# CONSTRUCCION DE LA CADENA FK (AUTO, ROOT )
# =========================


def crear_fk_auto_root_control(ListaDelSistemaFK):

    # =========================
    # AUTO 
    # =========================

    def crear_autos_FK(fk_joints):

        autos = []

        for i, joint in enumerate(fk_joints):

            nombre_auto = joint.replace("FK_Joint_", "FK_auto_")
            auto = cmds.group(em=True, n=nombre_auto)

            # SNAP
            cmds.delete(cmds.parentConstraint(joint, auto))

            # PARENT TEMPORAL
            cmds.parent(auto, joint)

            # RESET TRANSFORMS
            for attr in ["translateX","translateY","translateZ",
                         "rotateX","rotateY","rotateZ"]:
                cmds.setAttr(f"{auto}.{attr}", 0)

            for attr in ["scaleX","scaleY","scaleZ"]:
                cmds.setAttr(f"{auto}.{attr}", 1)

            # SACAR A WORLD
            cmds.parent(auto, world=True)

            # GUARDAR PADRE
            parent = cmds.listRelatives(joint, parent=True)

            # METER JOINT EN AUTO
            cmds.parent(joint, auto)

            # RESTAURAR JERARQUÍA
            if parent:
                cmds.parent(auto, parent[0])

            autos.append(auto)

        return autos
    

    # =========================
    # ROOTS 
    # =========================
    
    def crear_roots_FK(fk_joints, autos):

        roots = []

        for i, joint in enumerate(fk_joints):

            auto = autos[i]

            nombre_root = joint.replace("FK_Joint_", "FK_root_")
            root = cmds.group(em=True, n=nombre_root)
            # SNAP root al auto
            cmds.delete(cmds.parentConstraint(auto, root))
            # guardar padre del auto
            parent = cmds.listRelatives(auto, parent=True)
            # 1. meter auto dentro del root
            cmds.parent(auto, root)

            # =========================
            # JERARQUÍA FK 
            # =========================

            # 2. restaurar jerarquía
            if parent:
                cmds.parent(root, parent[0])
            else:
                cmds.parent(root, world=True)

            roots.append(root)

        print("🔥 Roots creados SIN romper jerarquía")
        return roots



    # =========================
    # APLICAR A EL SISTEMA
    # =========================

    resultado_fk = {}

    for nombre_cadena, fk_joints in ListaDelSistemaFK.items():

        autos = crear_autos_FK(fk_joints)
        roots = crear_roots_FK(fk_joints, autos)

        resultado_fk[nombre_cadena] = {
            "autos": autos,
            "roots": roots,
        }

    print("FK COMPLETO CREADO (AUTOS + ROOTS)")
    return resultado_fk

# endregion



   # =========================
    # Curvas de control 
    # =========================
    def crear_curvas_de_control_FK(fk_joints):

        ctrls = []

        for joint in fk_joints:

            nombre_ctrl = joint.replace("FK_Joint_", "FK_ctrl_")

            if "Columna" in joint:
                radio = 23

            else:
                radio = 7

            # crear ctrl
            ctrl = cmds.circle(
                n=nombre_ctrl,
                nr=(1,0,0),
                r=radio
            )[0]

            # 2. snap
            cmds.delete(cmds.parentConstraint(joint, ctrl))

            # 3. sacar shape
            shape = cmds.listRelatives(ctrl, s=True, fullPath=True)[0]

            # 🔥 4. parent shape al joint (esto está BIEN)
            cmds.parent(shape, joint, r=True, s=True)

            # 5. borrar transform
            cmds.delete(ctrl)

            # 🔥 6. rotar SOLO ese shape
            cvs = cmds.ls(shape + ".cv[*]", fl=True)
            if cvs:
                cmds.rotate(90, 0, 0, cvs, os=True, r=True)

            # 🔥 IMPORTANTE: guardar el joint, no el shape
            ctrls.append(joint)

        print("🔥 CONTROLES FK OK")
        return ctrls
