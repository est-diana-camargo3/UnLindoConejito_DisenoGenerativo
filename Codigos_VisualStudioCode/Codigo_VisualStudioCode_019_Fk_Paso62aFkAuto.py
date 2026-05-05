
#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║  Generador de Conejos  Aleatorios en Maya                     ║
#                         ║              M I   D U L C E   F O R T U N A                  ║
#                         ║  Desarrollado por: Mayerly Camargo codigo 1202327 y           ║
#                         ║                  Jennifer Lizeth Leiva codigo 1202617         ║                                               
#                         ║                                                               ║
#                         ╚═══════════════════════════════════════════════════════════════╝

import maya.cmds as cmds # Importamos el módulo de comandos de Maya para poder crear y manipular objetos en la escena.
import random # Importamos el módulo random para generar números aleatorios.

#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  PASO 1: Cambiar unidades a centimetros.                        ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝

cmds.currentUnit(linear="centimeter") #Cambiar unidades a centimetros para facilitar la creación de los objetos 
# Windows → Settings/Preferences → Preferences → Settings → Working Units  →"Linear"  → "centimeter"


#                         ╔═══════════════════════════════════════════════════════════════╗
#                         ║  PASO 2: Definir Modulo m. (ancho de Cabeza alearorio)        ║             
#                         ╚═══════════════════════════════════════════════════════════════╝

# ancho de cabeza es un numero entero aleatorio entre 20 y 43 cm
# nuestro modulo sera " m "
# m = ancho de cabeza / 10
ancho_cabeza = random.randint(20, 43) 
m = ancho_cabeza / 10



# region PASO3: Entender Funcion crear_cubo
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  PASO 3: Entender como Maya saca las formas, Funcion crear_cubo ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝

def crear_cubo(nombre, escala, posicion): 
    ancho, alto, profundidad = escala # Definimos como se llamaran los valores de la escala, en lugar de w.h.d que son por defecto.
    #Creamos una función reutilizable para dibujar n cubos.
    # parametros: nombre STRING que llevara el cubo en el ouliner de maya (string), 
    #             escala VECTOR (3 valores para x= ancho, y= alto, z= profundidad),
    #             posicion VECTOR (3 valores para coordenadas x,y,z)
  
    cubo = cmds.polyCube( name=nombre, w=ancho, h=alto, d=profundidad )[0]  
    #Creamos un cubo con el comando polyCube y le asignamos un nombre.  y una escala
    #                                    la razon por la que usamos una lista, es porque polycube devuelve una lista, 
    #                                    En la que el primer elemento es el objeto (la geometria)
    #                                    y el segundo elemento es las transformaciones que se le han hecho
    #                                    nosotros cogemos la primera que es el objeto y le asigamos nombre y escala. 
    
    #Calculamos el offset de la posicion, porque por defcto el cubo se crea con su centro en el origen (0,0,0), y nosotros queremos que siempre el 
    # punto de referencia sea la esquina superior izquierda de la cara frontal del cubo, y que se dibuje de ahi para abajo y hacia la derecha y la sobre el plano xy osea z=0
    # Al finalizar el conejo debemos reubicar los pivotes para que los joints se creen en el centro de las formas.
    offset_x = ancho / 2
    offset_y = -(alto / 2)
    offset_z = -(profundidad / 2)
    cmds.move(posicion[0] + offset_x, posicion[1] + offset_y, posicion[2] + offset_z, cubo)
    
    return cubo
# endregion



# region PASO 4: Crear Conejo Estandar 
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  PASO 4: Crear Conejo Estandar                                  ║
#                         ╚═════════════════════════════════════════════════════════════════╝

def crear_conejo(emocion="calma"):
    #MiCubitoDePrueba = crear_cubo("MiCubitoDePrueba", (1, 2, 3), (0, 0, 0)) 
    # #Crea un cubo en 0,0,0 con escala 1 de ancho,2 cm de alto ,3 cm de profundo y nombre "MiCubitoDePrueba"
    # Si queremos ver las medidas del cubo: chanel box → polyCube1 → input NO en escala, la escala siempre dira 1 

    #                            nombre                            escala                            posicion 
    cabeza = crear_cubo("Cabeza_Primitiva_001",          (m*10,   m*10,         (m*10)/2 ),    (0,     0,                  0          )  ) 
    ojo_izq = crear_cubo("OjoIzquierdo_Primitiva_002",   (m,      m,            (m*1.7)  ),    (m*7,   (-(m*10)/3.7),      (m*1.7)-m  )  )
    ojo_der = crear_cubo("OjoDerecho_Primitiva_003",     (m,      m,            (m*1.7)  ),    (m*2,   (-(m*10)/3.7),      (m*1.7)-m  )  )
    nariz = crear_cubo("Nariz_Primitiva_004",            (m,      m,            (m*1.7)  ),    (m*4.5, (-(m*10)/2),        (m*1.7)-m  )  )
    boca = crear_cubo("Boca_Primitiva_005",              (m*3,    m/2,          (m*1.7)  ),    (m*3.5, (-(m*10)/1.33),     (m*1.7)-m  )  )
    oreja_izq = crear_cubo("Oreja_Izquierda_006",        (m*3,    ((m*10)/3)*2, m*2      ),    (m*6,   (((m*10)/3)*2)-m,   (-m*1.5)   )  )
    oreja_der = crear_cubo("Oreja_Derecha_007",          (m*3,    ((m*10)/3)*2, m*2      ),    (m,     (((m*10)/3)*2)-m,   (-m*1.5)   )  )
    

    pie_izq = crear_cubo("PieIzquierdo_Primitiva_008",   (m*3,    m*3,          m*2      ),    (m*6,    (-m*21),              (-m*1.5)))
    pie_der = crear_cubo("PieDerecho_Primitiva_009",     (m*3,    m*3,          m*2      ),    (m,      (-m*21),              (-m*1.5)))
    tronco = crear_cubo("Tronco_Primitiva_010",          (m*13,   m*13,         (m*16)/2 ),    (-m*1.5, (-m*9),            (m*1.5)   )  )
    mano_izq = crear_cubo("ManoIzquierda_Primitiva_011", (m*4,    m*3,          m*2      ),    (m*10.5, (-m*12),           (-m*1.5)   )  )
    mano_der = crear_cubo("ManoDerecha_Primitiva_012",   (m*4,    m*3,          m*2      ),    (-m*4.5, (-m*12),           (-m*1.5)   )  )
    cola = crear_cubo("Cola_Primitiva_013",              (m,      m,            m*2      ),    (m*4.5,  (-m*9)+(-m*7.2),   (-m*5.5)   )  ) 
    
    parte_superior = cmds.group(cabeza, ojo_izq, ojo_der, nariz, boca, oreja_izq, oreja_der, name="ParteSuperior_Grupo")
    parte_inferior = cmds.group(tronco, mano_izq, mano_der, pie_izq, pie_der, cola, name="ParteInferior_Grupo")
    conejo = cmds.group(parte_superior, parte_inferior, name="Conejo_Grupo_001")
# endregion



# region PASO 6: Sistema FK      
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  PASO 6: Sistema FK                                             ║
#                         ╚═════════════════════════════════════════════════════════════════╝

# =========================
# PASO 6.0. UBICAR PIVOTES EN EL CENTRO DE LAS PRIMITIVAS
# =========================

# Como yo movi los pivotes a la esquina superior izquierda de la cara frontal de cada cubo, para dibujar mas fácil , 
# debo devolverlos al centro para poder obtener las coordenadas del centro en x,y,z de cada forma y colocar los joints en el x,y que me de 
# el z si debe ser en el centro de la profundidad...todos coplanares (en el paso 6.1  explico porque coplanares )

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

# region PASO 6.1. Crear Joints
# =========================
# PASO 6.1. CREAR JOINTS
# =========================
# Yo inicie a dibujar la cabeza del conejo en 0,0,0 y tiene una profundidad en z de -m*10/2,
# Por lo tanto la mitad de la profundidad de la cabeza es z= -(m*10/2)/2 es decir z= -m*10/4
# Ese es el plano central del conejo en z, ahi voy a dibujar los joints de manera coplanar 
# Porque es el plano que todas las primitivas comparten. 

# =========================
# Paso 6.1.A.Previo. Obtenemos posicion de pivote y caja envolvente con extremos de geometria de cada primitiva.
# =========================

def datos_primitiva(obj, PlanoCoplanarEnZ):
    # Devuelve una lista [X, Y, Z] con la posicion del pivote  de la primitiva, para colocar joints EXACTAMENTE en el centro x,y en z si es (z= -m*10/4)
    centro = cmds.xform(obj, q=True, ws=True, rp=True) 
    #devuelve una lista de [xmin, ymin, zmin, xmax, ymax, zmax] para encontrar extremos de la geometría y colocar los 2 joints de las puntas o extremos (orejas, pies, etc.)
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

# region PASO 6.1.ab Crear Y RENOMBRAR  joints 
# =========================
# Paso 6.1.A. Crear joints coplanares en z= m/4 (24 JOINTS)
# Paso 6.1.B.  Renombrar joints (Interno, Medio, end)
# =========================

def crear_joints_coplanares():
    """ 
    .......................................................................
    ......................(3)...................(6)........................
    .......................|.....................|.........................           
    ......................(2)...................(5)........................       <-- Orejas
    .......................|.....................|.........................
    ......................(1)...................(4)........................
    .......................__________(22)_________.........................       <--Frente
    ......................|            |          |........................
    ......................|       O         O     |........................
    ......................|            |          |........................
    ......................|            O          |........................
    ......................|            |          |........................
    ......................|         ___|___       |........................
    ......................|            |          |........................
    ......................._______________________.........................
    ................_________________(23)________________..................       <--Cuello
    ................|                 |                 |..................
    ................|                 |                 |..................
    ................|                 |                 |..................
    ..( 9)-( 8)-( 7)|___________      |      ___________|(10)-(11)-(12)....	      <-- Manos
    ................|           \     |     /           |..................
    ................|               (24)                |(19)-(20)-(21)....       <-- Cola
    ................|                 |                 |..................
    ................|                 |                 |..................
    ................|________________(23)_______________|.................. 
    ......................(13)...................(16)......................
    .......................|......................|........................           
    ......................(14)...................(17)......................       <-- Orejas
    .......................|......................|........................
    ......................(15)...................(18)......................
    .......................................................................
           
    """
    cmds.select(clear=True)

    PlanoCoplanarEnZ = -(m*10)/4

    # =========================
    # COLUMNA Joints (22,23,24)
    # =========================
    cabeza = datos_primitiva("Cabeza_Primitiva_001", PlanoCoplanarEnZ) # extraemos posicion del pivote y box de la caja
    tronco = datos_primitiva("Tronco_Primitiva_010", PlanoCoplanarEnZ)
    cola   = datos_primitiva("Cola_Primitiva_013", PlanoCoplanarEnZ)

    j22 = cmds.joint(name="FK_Joint_22_Interno_ColumnaFrente",  p=(cabeza["centro"][0], cabeza["ymax"], PlanoCoplanarEnZ) ) # centro en x, ymax en y, z en el plano coplanar
    j23 = cmds.joint(name="FK_Joint_23_Medio_ColumnaCuello", p=(tronco["centro"][0], tronco["ymax"], PlanoCoplanarEnZ) )
    j24 = cmds.joint(name="FK_Joint_24_Externo_ColumnaCadera",  p=(cola["centro"][0], cola["ymin"]+((cola["ymax"]-cola["ymin"])/2), PlanoCoplanarEnZ) )

    # =========================
    # OREJA DERECHA Joints (1,2,3)
    # =========================
    cmds.select(j22) #van pegados al j22 que es InternoColumna_Frente_Joint_22
    OrejaR = datos_primitiva("Oreja_Derecha_007", PlanoCoplanarEnZ)
    j1 = cmds.joint(name="FK_Joint_1_Interno_OrejaDerecha",  p=(OrejaR["centro"][0], OrejaR["ymin"]+m, PlanoCoplanarEnZ)) # centro en x, ymin+m en y para que no quede en la interpenetracion de formas, z en el plano coplanar
    j2 = cmds.joint(name="FK_Joint_2_Medio_OrejaDerecha", p=(OrejaR["centro"][0], OrejaR["centro"][1], PlanoCoplanarEnZ)) 
    j3 = cmds.joint(name="FK_Joint_3_Externo_OrejaDerecha",  p=(OrejaR["centro"][0], OrejaR["ymax"], PlanoCoplanarEnZ))

    # =========================
    # OREJA IZQUIERDA (4,5,6)
    # =========================
    cmds.select(j22) #van pegados al j22 que es InternoColumna_Frente_Joint_22
    OrejaL = datos_primitiva("Oreja_Izquierda_006", PlanoCoplanarEnZ)
    j4 = cmds.joint(name="FK_Joint_4_Interno_OrejaIzquierda",  p=(OrejaL["centro"][0], OrejaL["ymin"]+m, PlanoCoplanarEnZ))
    j5 = cmds.joint(name="FK_Joint_5_Medio_OrejaIzquierda", p=(OrejaL["centro"][0], OrejaL["centro"][1], PlanoCoplanarEnZ))
    j6 = cmds.joint(name="FK_Joint_6_Externo_OrejaIzquierda",  p=(OrejaL["centro"][0], OrejaL["ymax"], PlanoCoplanarEnZ))
    
    # =========================
    # MANO DERECHA (7,8,9)
    # =========================
    cmds.select(j23)
    BrazoR = datos_primitiva("ManoDerecha_Primitiva_012", PlanoCoplanarEnZ)
    j7 = cmds.joint(name="FK_Joint_7_Interno_ManoDerecha",  p=(BrazoR["xmax"], BrazoR["centro"][1], PlanoCoplanarEnZ)) # pegada al cuerpo = raiz 
    j8 = cmds.joint(name="FK_Joint_8_Medio_ManoDerecha", p=(BrazoR["centro"][0], BrazoR["centro"][1], PlanoCoplanarEnZ))
    j9 = cmds.joint(name="FK_Joint_9_Externo_ManoDerecha",  p=(BrazoR["xmin"], BrazoR["centro"][1], PlanoCoplanarEnZ)) # Dedos de la mano Fin 

    # =========================
    # MANO IZQUIERDA (10,11,12)
    # =========================
    cmds.select(j23)
    BrazoL = datos_primitiva("ManoIzquierda_Primitiva_011", PlanoCoplanarEnZ)
    j10 = cmds.joint(name="FK_Joint_10_Interno_ManoIzquierda",  p=(BrazoL["xmin"], BrazoL["centro"][1], PlanoCoplanarEnZ)) # pegada al cuerpo = raiz 
    j11 = cmds.joint(name="FK_Joint_11_Medio_ManoIzquierda", p=(BrazoL["centro"][0], BrazoL["centro"][1], PlanoCoplanarEnZ))
    j12 = cmds.joint(name="FK_Joint_12_Externo_ManoIzquierda",  p=(BrazoL["xmax"], BrazoL["centro"][1], PlanoCoplanarEnZ)) # Dedos de la mano Fin 
 
    # =========================
    # PIE DERECHO (13,14,15)
    # =========================
    cmds.select(j24)
    PieR = datos_primitiva("PieDerecho_Primitiva_009", PlanoCoplanarEnZ)
    j13 = cmds.joint(name="FK_Joint_13_Interno_PieDerecho",  p=(PieR["centro"][0], PieR["ymax"], PlanoCoplanarEnZ))
    j14 = cmds.joint(name="FK_Joint_14_Medio_PieDerecho", p=(PieR["centro"][0], PieR["centro"][1], PlanoCoplanarEnZ))
    j15 = cmds.joint(name="FK_Joint_15_Externo_PieDerecho",  p=(PieR["centro"][0], PieR["ymin"], PlanoCoplanarEnZ))

    # =========================
    # PIE IZQUIERDO (16,17,18)
    # =========================
    cmds.select(j24)
    PieL = datos_primitiva("PieIzquierdo_Primitiva_008", PlanoCoplanarEnZ)
    j16 = cmds.joint(name="FK_Joint_16_Interno_PieIzquierdo",  p=(PieL["centro"][0], PieL["ymax"], PlanoCoplanarEnZ))
    j17 = cmds.joint(name="FK_Joint_17_Medio_PieIzquierdo", p=(PieL["centro"][0], PieL["centro"][1], PlanoCoplanarEnZ))
    j18 = cmds.joint(name="FK_Joint_18_Externo_PieIzquierdo",  p=(PieL["centro"][0], PieL["ymin"], PlanoCoplanarEnZ))

    # =========================
    # COLA (19,20,21) 
    # =========================
    # la cola no crece verticalmente sino hacia -z  por eso no pueden quedar en el mismo plano coplanar que el resto del cuerpo 
    cola = datos_primitiva("Cola_Primitiva_013", PlanoCoplanarEnZ)
    centro_cola = cmds.xform("Cola_Primitiva_013", q=True, ws=True, rp=True) #medida de centro de la cola 
    # Devueleve una lista de 3 valores "centroenx": centro[0], "centroeny": centro[1], "centroenz": centro[2]),
    bboxcola = cmds.exactWorldBoundingBox("Cola_Primitiva_013") #limites de la cola para colocar joints en los extremos
    # Devuelve una lista de 5 valores "xmin": bbox[0], "ymin": bbox[1], "zmin": bbox[2], "xmax": bbox[3], "ymax": bbox[4], "zmax": bbox[5], zmin = bbox[2]
    zmin = bboxcola[2]  
    zmax = bboxcola[5] 
    zcentro = centro_cola[2]

    cmds.select(j24)

    j19 = cmds.joint(name="FK_Joint_19_Interno_Cola",  p=(centro_cola[0], centro_cola[1], zmax)) #  Raiz pegada al cuerpo 
    j20 = cmds.joint(name="FK_Joint_20_Medio_Cola", p=(centro_cola[0], centro_cola[1], zcentro))
    j21 = cmds.joint(name="FK_Joint_21_Externo_Cola",  p=(centro_cola[0], centro_cola[1], zmin)) # Fin de la cola
    print("✅ 24 JOINTS CREADOS - COPLANARES, JERÁRQUICOS Y LIMPIOS")

    # guardo mi 8 sistemas Fk 
    # 1 es la cadena principal (columna)
    # Las otras 7 son ramas (subcadenas) conectadas a esa
    # Aunque tenga varias listas: SIGUEN siendo una sola jerarquía en Maya Porque hicimos esto:
    # cmds.select(j22)  # orejas cuelgan de la columna
    orejaR_FK = [j1, j2, j3]
    orejaL_FK = [j4, j5, j6]
    brazoR_FK = [j7, j8, j9]
    brazoL_FK = [j10, j11, j12]
    piernaR_FK = [j13, j14, j15]
    piernaL_FK = [j16, j17, j18]
    cola_FK = [j19, j20, j21]
    columna_FK = [j22, j23, j24] #guardo la lista de la columna 

    lista_del_sistema_FK = {
        "orejaR_FK": orejaR_FK,
        "orejaL_FK": orejaL_FK,
        "brazoR_FK": brazoR_FK,
        "brazoL_FK": brazoL_FK,
        "piernaR_FK": piernaR_FK,
        "piernaL_FK": piernaL_FK,                
        "cola_FK": cola_FK,
        "columna_FK": columna_FK
    }

    return lista_del_sistema_FK

# endregion

# region Paso 6.1.C. Orientar Joints
# =========================
# Paso 6.1.C. Orientar Joints
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

#para orientar cadena por cadena, la llamo mas adelante 
def orientar_subcadena_FK(FK_talcadena, miorientJoint, eje_secundario): #cadena, orientacion xyz x apunta al hijo, crece en y, z perpendicular
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

    # Nos aseguramos que el ultimo joint tenga sus valores de transformacion (rotacion y traslacion) excepto la escala en 0,0,0
    ultimo = FK_talcadena[-1]
    ultimo = FK_talcadena[-1]
    cmds.setAttr(ultimo + ".jointOrientX", 0)
    cmds.setAttr(ultimo + ".jointOrientY", 0)
    cmds.setAttr(ultimo + ".jointOrientZ", 0)


def orientar_joints_de_toda_la_cadena_FK(ListaDelSistemaFK):

    # la cola no tienen la misma orientacion que el resto del cuerpo porque no crecen verticalmente 
                # sino hacia -z, por eso la orientamos al final y de manera independiente para que no afecte la orientacion del resto del cuerpo.
                # la razon por la que se parento y desemparento es para que las transformaciones del padre osea de la columna 
                # no afecten al hijo osea  a la cola  y ya al final vuelvo vemos a conectar el padre con el hijo para no perder jerarquia 
    # lo mismo pasa con los pies que no crecen verticalmente hcaia arriba  sino hacia abajo, 
    # por eso parentmos y desemparentamos al final y de manera independiente para que no se vean afectados por la la orientacion del papa columna.
    
    cola = ListaDelSistemaFK["cola_FK"]
    piernaR = ListaDelSistemaFK["piernaR_FK"]
    piernaL = ListaDelSistemaFK["piernaL_FK"]


    raiz_cola = cola[0]
    raiz_piernaR = piernaR[0]
    raiz_piernaL = piernaL[0]


    # 1. Guardar padre original
    padre_Cola = cmds.listRelatives(raiz_cola, parent=True)
    padre_piernaR = cmds.listRelatives(raiz_piernaR, parent=True)
    padre_piernaL = cmds.listRelatives(raiz_piernaL, parent=True)


    # Desparentar cola y pies
    cmds.parent(raiz_cola, world=True)
    cmds.parent(raiz_piernaR, world=True)
    cmds.parent(raiz_piernaL, world=True)


   
    # 3. Orientar TODO menos la cola ni los pies 
    orientar_subcadena_FK(ListaDelSistemaFK["columna_FK"], "xyz", "yup")
    orientar_subcadena_FK(ListaDelSistemaFK["orejaR_FK"], "xyz", "yup")
    orientar_subcadena_FK(ListaDelSistemaFK["orejaL_FK"], "xyz", "yup")
    orientar_subcadena_FK(ListaDelSistemaFK["brazoR_FK"], "xyz", "yup")
    orientar_subcadena_FK(ListaDelSistemaFK["brazoL_FK"], "xyz", "ydown")

    # 4. Limpiar cola SIN orientación automática
    orientar_subcadena_FK(ListaDelSistemaFK["cola_FK"], "xzy", "yup")
    orientar_subcadena_FK(ListaDelSistemaFK["piernaR_FK"], "xyz", "yup")
    orientar_subcadena_FK(ListaDelSistemaFK["piernaL_FK"], "xyz", "yup")

    # la razon por la que se parento y desemparento es para que las transformaciones del padre
    # no afecten al hijo.
    # pero luego volvemos a conectar el padre con el hijo para no perder jerarquia 
    # 5. Volver a parentar
    if padre_Cola:
        cmds.parent(raiz_cola, padre_Cola[0])
    if padre_piernaR:
        cmds.parent(raiz_piernaR, padre_piernaR[0])
    if padre_piernaL:
        cmds.parent(raiz_piernaL, padre_piernaL[0])

    ocultar_gizmos_pivotes()
    mostrar_gizmos_joints()

    print("✅ JOINTS ORIENTADOS POR SISTEMAS")

# endregion


# region Paso 6.1.d. Duplicar cadenas y renombrarlas de FK a IK y a MAIN
# =========================
# Paso 6.1.d. Duplicar cadenas y renombrarlas de FK a IK y a MAIN
# =========================

def duplicar_y_renombrar_cadenas_IK_y_MAIN():
    """
    Duplica la cadena FK del conejo y crea:
    - cadena IK
    - cadena MAIN
    SOLO cambia el prefijo FK_
    """

    raiz_fk = "FK_Joint_22_Interno_ColumnaFrente"

    if not cmds.objExists(raiz_fk):
        cmds.warning("No existe la cadena FK del conejo")
        return

    def procesar(prefijo):
        dup = cmds.duplicate(raiz_fk, renameChildren=True)[0]

        jerarquia = cmds.listRelatives(dup, allDescendents=True, type="joint") or []
        jerarquia.append(dup)

        nueva_lista = []
        for j in jerarquia:
            nuevo_nombre = j.replace("FK_", prefijo + "_")
            nuevo_nombre = cmds.rename(j, nuevo_nombre)
            nueva_lista.append(nuevo_nombre)

        return nueva_lista

    cadena_IK = procesar("IK")
    cadena_MAIN = procesar("MAIN")

    print("✅ Cadenas IK y MAIN creadas y renombradas")

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

# endregion
# endregion

 

# region # Paso 6.2. CONSTRUCCION DE LA CADENA FK (AUTO, ROOT Y CONTROL)
# =========================
# Paso Paso 6.2. CONSTRUCCION DE LA CADENA FK (AUTO, ROOT Y CONTROL)
# =========================
    # 2.a. AUTO
    # 2.b. ROOT
    # 2.c. CONTROL 

def crear_fk_auto_root_control(ListaDelSistemaFK):

    # =========================
    # Paso 6.2.a. AUTO 
    # =========================

    def crear_autos(fk_joints):

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


    def crear_roots(fk_joints, autos):

        roots = []

        for i, joint in enumerate(fk_joints):

            auto = autos[i]

            nombre_root = joint.replace("FK_Joint_", "FK_root_")
            root = cmds.group(em=True, n=nombre_root)

            # SNAP
            cmds.delete(cmds.parentConstraint(auto, root))

            # A WORLD
            if cmds.listRelatives(root, parent=True):
                cmds.parent(root, world=True)

            if i == 0:
                cmds.parent(auto, root)

            else:
                parent_joint = fk_joints[i - 1]

                child = cmds.listRelatives(parent_joint, c=True, type="transform")

                if child:
                    child = child[0]

                    cmds.parent(root, parent_joint)
                    cmds.parent(child, root)

            roots.append(root)

        return roots


    def crear_controles(fk_joints):

        controles = []

        for joint in fk_joints:

            nombre_ctrl = joint.replace("FK_Joint_", "FK_ctrl_")

            ctrl = cmds.circle(n=nombre_ctrl, nr=(0,1,0), r=2)[0]
            shape = cmds.listRelatives(ctrl, shapes=True)[0]

            # PARENT SHAPE AL JOINT 🔥
            cmds.parent(shape, joint, r=True, s=True)
            cmds.delete(ctrl)

            controles.append(shape)

        return controles


    # =========================
    # APLICAR A TODO EL SISTEMA
    # =========================

    resultado_fk = {}

    for nombre_cadena, fk_joints in ListaDelSistemaFK.items():

        autos = crear_autos(fk_joints)
        #roots = crear_roots(fk_joints, autos)
        #ctrls = crear_controles(fk_joints)

        resultado_fk[nombre_cadena] = {
            "autos": autos,
            #"roots": roots,
            #"ctrls": ctrls
        }

   
    #print("🔥 FK COMPLETO CREADO (AUTOS + ROOTS + CONTROLES)")
    return resultado_fk
    

# endregion







# region PASO 5: Interfaz UI 
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  PASO 5: Interfaz UI                                            ║
#                         ╚═════════════════════════════════════════════════════════════════╝


# =========================
# COLORES para interfaz (RGB normalizados 0–1)
# =========================
fondorosado = (236/255, 188/255, 251/255)   # #ecbcfb
morado = (204/255, 79/255, 252/255)   # #cc4ffc
lila = (204/255, 153/255, 255/255)   # CC99FF
gris = (116/255, 116/255, 116/255)    # #747474
blanco = (1,1,1)

# =========================
# FUNCIÓN DEL BOTÓN GENERAR
# =========================
def generar_conejo_ui(*args):
    
    seleccion = cmds.radioCollection("emociones", q=True, select=True)
    
    crear_conejo(seleccion)
    mostrar_gizmos_pivotes()
    ListaDelSistemaFK = crear_joints_coplanares()
    orientar_joints_de_toda_la_cadena_FK(ListaDelSistemaFK)
    duplicar_y_renombrar_cadenas_IK_y_MAIN()
    ocultar_cadenas_IK_y_MAIN()
    crear_fk_auto_root_control(ListaDelSistemaFK)



# =========================
# FUNCIÓN BOTÓN BORRAR
# =========================
def borrar_escena(*args):
    cmds.select(all=True)
    cmds.delete()

def crear_ui():
    
    if cmds.window("miVentanaConejo", exists=True):
        cmds.deleteUI("miVentanaConejo")
  
    ventana = cmds.window("miVentanaConejo", title="MI DULCE FORTUNA", widthHeight=(600, 400))

    # =========================
    # LAYOUT PRINCIPAL (2 COLUMNAS)
    # =========================
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)

    # =========================
    # 🖼️ COLUMNA IZQUIERDA (IMAGEN)
    # =========================
    ruta_imagen = "C:/Users/USUARIO/Documents/GitHub/UnLindoConejito_DisenoGenerativo/Imagenes/ImagenMenu.png"

    cmds.columnLayout(width=300)
    cmds.image(image=ruta_imagen)
    cmds.setParent('..')

    # =========================
    # 🎛️ COLUMNA DERECHA (MENÚ)
    # =========================
    cmds.columnLayout(adjustableColumn=True, bgc=fondorosado)

    cmds.separator(h=20, style="none")

    cmds.text(label="MI DULCE FORTUNA",
              height=30,
              bgc=fondorosado,
              font="boldLabelFont",
              align="center")
    cmds.separator(h=10, style="none") #espacio vacio
    
    # Raya division
    cmds.text(label="", height=6, bgc=lila)
    cmds.separator(h=1, style="in")

    cmds.separator(h=10, style="none") #espacio vacio
    cmds.text(label="Selecciona una emoción y da clic a generar", bgc=fondorosado)
    cmds.separator(h=10, style="none") #espacio vacio

    # =========================
    # EMOCIONES (DESPLAZADAS)
    # =========================
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(100, 200))  # ← 30 px espacio

    cmds.text(label="", bgc=fondorosado)  # ← espacio vacío izquierda

    cmds.columnLayout(adjustableColumn=True, bgc=fondorosado)

    cmds.radioCollection("emociones")
    cmds.radioButton("calma", label="Calma 😌", select=True)
    cmds.radioButton("tristeza", label="Tristeza 😞")
    cmds.radioButton("aPieria", label="APiería 😊")
    cmds.radioButton("ternura", label="Ternura 😍")
    cmds.radioButton("enojo", label="Enojo 😠")

    cmds.setParent('..')  # cerrar columnLayout
    cmds.setParent('..')  # cerrar rowLayout

    cmds.separator(h=15, style="none")

    # =========================
    # 4. BOTONES
    # =========================
    cmds.rowLayout(numberOfColumns=3,columnWidth3=(80, 120, 100)) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(
        label="Generar Conejito 🐰",
        command=generar_conejo_ui,
        bgc=(1,1,1),
        height=40
    )
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este
    cmds.separator(h=10, style="none")


    cmds.rowLayout(numberOfColumns=3,columnWidth3=(90, 120, 100)) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(
        label="Borrar Escena 🧹",
        command=borrar_escena,
        bgc=(1,1,1),
        height=40
    )
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este
    cmds.separator(h=10, style="none") #espacio vacio

    # Raya division
    cmds.text(label="", bgc=lila,height=6) 
    cmds.separator(h=1, style="in")

    cmds.separator(h=10, style="none") #espacio vacio
    cmds.text(label="Mayerly Camargo Pedraza Código 1202327", bgc=fondorosado)
    cmds.text(label="Jennifer Lizeth Leiva Código 1202617", bgc=fondorosado)
    cmds.text(label="Docente: Diego Felipe Beltrán Cardona", bgc=fondorosado)
    cmds.text(label="UMNG 2026", bgc=fondorosado)
   
    cmds.separator(h=20, style="none") #espacio vacio

    cmds.setParent('..')  # ← cerrar columnLayout derecha
    cmds.setParent('..')  # ← cerrar rowLayout principal

    cmds.showWindow(ventana)

# =========================
# EJECUTAR UI
# =========================
crear_ui()

# endregion









# region Notas

#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Notas                                                          ║
#                         ╚═════════════════════════════════════════════════════════════════╝

# Cambiar una variable en donde este 
# ctrl + shift +l

"""Comentario"""
""" # region Notas
# código aquí
# endregion
"""

# Linea a copiar en el script editor de maya en la seccion python para ejecutar aplicacion de conejos
# Solo es cambiarle el numero el nombre

#import sys
#import importlib
#sys.path.append("C:/Users/USUARIO/Documents/GitHub/UnLindoConejito_DisenoGenerativo/Codigos_VisualStudioCode")
#import Codigo_VisualStudioCode_019_Fk_Paso62aFkAuto
#importlib.reload(Codigo_VisualStudioCode_019_Fk_Paso62aFkAuto)
#Codigo_VisualStudioCode_019_Fk_Paso62aFkAuto.crear_ui()
# endregion





# region Codigo sin usar
#hola
"""

def obtener_color(emocion):
    colores = {
        "calma": (0.88, 0.98, 0.92),
        "tristeza": (0.0, 0.41, 0.54),
        "aPieria": (1.0, 0.85, 0.6),
        "ternura": (0.96, 0.8, 1.0),
        "enojo": (1.0, 0.58, 0.58)
    }
    return colores.get(emocion, (1,1,1))

def crear_material(nombre, color):
    shader = cmds.shadingNode('lambert', asShader=True, name=nombre)
    cmds.setAttr(shader + ".color", color[0], color[1], color[2], type="double3")
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=nombre + "SG")
    cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True)
    return shader, sg


def crear_conejo(emocion="calma"):
    
    cmds.select(all=True)
    cmds.delete()
    
    color = obtener_color(emocion)
    shader, sg = crear_material("conejo_mat", color)
    
  
    
    
    
    
    
    
    
    
    partes = [cabeza, ojo_izq, ojo_der, nariz, boca, oreja_izq, oreja_der,
              tronco, mano_izq, mano_der, pie_izq, pie_der, cola]
    
    for p in partes:
        cmds.sets(p, edit=True, forceElement=sg)
    

    
    
    conejo = cmds.group(parte_superior, parte_inferior, name="Conejo_Grupo_001")

crear_conejo("ternura") """
# endregion










