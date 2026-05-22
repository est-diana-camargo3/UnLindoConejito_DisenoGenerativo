import maya.cmds as cmds
import random



# Variable global para modulo
m = 1
global morfologia
morfologia= "estandar"
piezas_deformables = []



#  region Funcion crear_cubo
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Entender como Maya saca las formas, Funcion crear_cubo         ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝

def crear_cubo(nombre, escala, posicion, tipo="default"):
    

    ancho, alto, profundidad = escala

    # -------------------------
    # 1. REGLAS POR EXTREMIDAD
    # -------------------------
    if tipo == "cabeza" or tipo == "tronco" or tipo == "nariz" or tipo == "piernas":
        subdivisiones = (1,2,1)
    elif tipo == "orejas":
        subdivisiones = (1,2,2)
    elif tipo == "ojos":
        subdivisiones = (1,1,2)
    elif tipo == "cola":
        subdivisiones = (1,1,1)
    elif tipo == "manos":
        subdivisiones = (2,1,1)
    else:
        subdivisiones = (2,2,2)

    sx, sy, sz = subdivisiones

    # -------------------------
    # 2. CREAR CUBO
    # -------------------------
    cubo = cmds.polyCube( name=nombre, w=ancho, h=alto, d=profundidad, sx=sx, sy=sy, sz=sz)[0]

    # -------------------------
    # 3. OFFSET POSICIÓN
    # -------------------------
    offset_x = ancho / 2
    offset_y = -(alto / 2)
    offset_z = -(profundidad / 2)

    cmds.move(posicion[0] + offset_x, posicion[1] + offset_y, posicion[2] + offset_z,cubo)

    # -------------------------
    # 4. DEFORMACIONES SEGÚN TIPO
    # -------------------------
    bbox = cmds.exactWorldBoundingBox(cubo)
    cx = (bbox[0] + bbox[3]) / 2
    cy = (bbox[1] + bbox[4]) / 2
    cz = (bbox[2] + bbox[5]) / 2

    if tipo == "tronco":
        cara = cubo + ".f[5]"
        cmds.select(cara)
        cmds.scale(1.5, 1,1.5,pivot=(cx, cy, cz),relative=True)

    elif tipo == "piernas":
            
        edges = [f"{cubo}.e[1]",f"{cubo}.e[4]",f"{cubo}.e[18]",f"{cubo}.e[19]" ]
        cmds.move(0, -m*2, 0, edges, r=True)

    elif tipo == "orejas":

        # -------------------------
        # 1. ESCALAR CARAS BASE
        # -------------------------
        faces_scale = [f"{cubo}.f[2]",f"{cubo}.f[3]", f"{cubo}.f[6]",f"{cubo}.f[7]"]
        cmds.select(faces_scale, r=True)
        cmds.scale(0.5, 1, 1,pivot=(cx, cy, cz),r=True)

        # -------------------------
        # 2. MOVER EDGES (FORMA OREJA)
        # -------------------------
        edges = [f"{cubo}.e[27]", f"{cubo}.e[26]", f"{cubo}.e[3]", f"{cubo}.e[7]", f"{cubo}.e[26:27]", f"{cubo}.e[30:31]"]
        cmds.select(edges, r=True)
        cmds.move(0, 0, 1.5, r=True)

        # -------------------------
        # 3. DEFORMACIÓN EXTRA CON FACES
        # -------------------------
        faces_move = [f"{cubo}.f[2]", f"{cubo}.f[3]"]
        cmds.select(faces_move, r=True)
        cmds.move(0, 0, 3.341989, r=True)

    elif tipo == "nariz":
            
        face = f"{cubo}.f[5]"
        cmds.select(face, r=True)
        cmds.scale(0.3, 1, 0.3,pivot=(cx, cy, cz),r=True)

    return cubo
# endregion


# region Crear Conejo Estandar 
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Crear Conejo Estandar                                          ║
#                         ╚═════════════════════════════════════════════════════════════════╝

def crear_conejo(emocion="calma"):
    """
    MiCubitoDePrueba = crear_cubo("MiCubitoDePrueba", (1, 2, 3), (0, 0, 0)) 
    Crea un cubo en 0,0,0 con escala 1 de ancho,2 cm de alto ,3 cm de profundo y nombre "MiCubitoDePrueba"
    Si queremos ver las medidas del cubo: chanel box → polyCube1 → input NO en escala, la escala siempre dira 1 
    """
    #                         ╔═══════════════════════════════════════════════════════════════╗
    #                         ║   Definir Modulo m. (ancho de Cabeza alearorio)               ║             
    #                         ╚═══════════════════════════════════════════════════════════════╝


    global m
    global piezas_deformables
    global ancho_cabeza
  

    # =========================
    # NUEVO MODULO ALEATORIO
    # =========================
    ancho_cabeza = random.randint(20, 43)
    m = ancho_cabeza / 10

    print(" 📐 ancho_Cabeza :", ancho_cabeza)
    print(" 📐 Nuevo módulo m:", m)

    # =========================
    # Establecer morfología del conejo según el ancho de la cabeza
    # =========================

    morfologia = "vertical"

    if 20 <= ancho_cabeza <= 27:
        morfologia = "vertical"

    elif 28 <= ancho_cabeza <= 35:
        morfologia = "estandar"

    elif 36 <= ancho_cabeza <= 43:
        morfologia = "horizontal"

    print(" 📐🐰 Morfología:", morfologia)

    if morfologia == "vertical":
        ancho_cabeza = m * 10
        ancho_oreja = m * 3

        mitad_cabeza = ancho_cabeza / 2
        mitad_oreja = ancho_oreja / 2

        offset_oreja_x = mitad_cabeza - mitad_oreja
        
        #                            nombre                            escala                            posicion 
        oreja_izq = crear_cubo("Oreja_Izquierda_006",        (m*3,    m*9,   m*2      ),    ((-m*1)+(-m*3), (m*9)-m, m         ),  tipo="orejas")
        oreja_der = crear_cubo("Oreja_Derecha_007",          (m*3,    m*9,   m*2      ),    ((m*1), (m*9)-m, m         ),  tipo="orejas")
        cabeza = crear_cubo("Cabeza_Primitiva_001",          (m*10,   m*10,  m*10     ),    ((-m*5),      0,               (m*5)      ),  tipo="cabeza") 
        ojo_izq = crear_cubo("OjoIzquierdo_Primitiva_002",   (m*1.5,  m*1.5,        (m)  ), ((-m*1.25)+(-m*1.5), (-(m*10)/3.7),       (m*5.5)),  tipo="ojos")#CAMBIÓ
        ojo_der = crear_cubo("OjoDerecho_Primitiva_003",     (m*1.5,  m*1.5,        (m)  ), ((m*1.25), (-(m*10)/3.7),      (m*5.5) ),  tipo="ojos")#CAMBIÓ
        nariz = crear_cubo("Nariz_Primitiva_004",            (m,      m,     (m)    ),    ((-m/2),      (-(m*10)/2),     (m*5.5)   ),  tipo="nariz")#CAMBIÓ
        
        tronco = crear_cubo("Tronco_Primitiva_010",          (m*13,   m*20,  (m*16)/2 ),    ((-m*6.5),    (-m*8.5),          (m*8)/2    ),  tipo="tronco") #CAMBIÓ
        mano_izq = crear_cubo("ManoIzquierda_Primitiva_011", (m*6,    m*4,          m*4      ),    ((-m*6.5)+(-m*4.5), (-m*11.5),         (m*2)      ),  tipo="manos")
        mano_der = crear_cubo("ManoDerecha_Primitiva_012",   (m*6,    m*4,          m*4      ),    ((m*5), (-m*11.5),         (m*2)      ),  tipo="manos")
        pie_izq = crear_cubo("PieIzquierdo_Primitiva_008",   (m*4,    m*12,   m*4      ),    ((-m*2)-10,   (-m*27.3),       (m*2)      ),  tipo="piernas") #CAMBIÓ
        pie_der = crear_cubo("PieDerecho_Primitiva_009",     (m*4,    m*12,   m*4      ),    ((-m*2)+10,   (-m*27.3),       (m*2)      ),  tipo="piernas") #CAMBIÓ
        cola = crear_cubo("Cola_Primitiva_013",              (m*3,    m*3,          m*4      ),    ((-m*1.5),    (-m*9)+(-m*12), (-m*3.5 )),  tipo="cola") #CAMBIÓ

    
    elif morfologia == "estandar":
        #                            nombre                            escala                            posicion 
        oreja_izq = crear_cubo("Oreja_Izquierda_006",        (m*3,    ((m*10)/3)*2, m*2    ),    ((-m*1.5)-10, (((m*10)/3)*2)-m,   m        ),  tipo="orejas")
        oreja_der = crear_cubo("Oreja_Derecha_007",          (m*3,    ((m*10)/3)*2, m*2    ),    ((-m*1.5)+10, (((m*10)/3)*2)-m,   m        ),  tipo="orejas")
        cabeza = crear_cubo("Cabeza_Primitiva_001",          (m*10,   m*10,         m*10   ),    ((-m*5),       0,                 (m*5)    ),  tipo="cabeza")  
        ojo_izq = crear_cubo("OjoIzquierdo_Primitiva_002",   (m*1.5,  m*1.5,        (m)  ),    ((-m*1.7)+(-m*1.5), (-(m*10)/3.7),      (m*5.5) ),  tipo="ojos")#CAMBIÓ
        ojo_der = crear_cubo("OjoDerecho_Primitiva_003",     (m*1.5,  m*1.5,        (m)  ),    ((m*1.7), (-(m*10)/3.7),      (m*5.5) ),  tipo="ojos")#CAMBIÓ
        nariz = crear_cubo("Nariz_Primitiva_004",            (m,      m,            (m)  ),    ((-m/2),      (-(m*10)/2),        (m*5.5) ),  tipo="nariz")#CAMBIÓ
      
        tronco = crear_cubo("Tronco_Primitiva_010",          (m*13,   m*13,         (m*16)/2 ),    ((-m*6.5),  (-m*9),          (m*8)/2    ),  tipo="tronco")
        mano_izq = crear_cubo("ManoIzquierda_Primitiva_011", (m*6,    m*4,          m*4      ),    ((-m*7)+(-m*4.5), (-m*11.5),         (m*2)      ),  tipo="manos")
        mano_der = crear_cubo("ManoDerecha_Primitiva_012",   (m*6,    m*4,          m*4      ),    ((m*5.5), (-m*11.5),         (m*2)      ),  tipo="manos")
        pie_izq = crear_cubo("PieIzquierdo_Primitiva_008",   (m*4,    m*6,          m*4      ),    ((-m*2)-10, (-m*21),         (m*2)      ),  tipo="piernas")
        pie_der = crear_cubo("PieDerecho_Primitiva_009",     (m*4,    m*6,          m*4      ),    ((-m*2)+10, (-m*21),         (m*2)      ),  tipo="piernas")
        cola = crear_cubo("Cola_Primitiva_013",              (m*3,    m*3,          m*4      ),    ((-m*1.5),    (-m*9)+(-m*7.2), (-m*3.5 )),  tipo="cola") #CAMBIÓ
        

    elif morfologia == "horizontal":
        #                            nombre                            escala                            posicion 
        oreja_izq = crear_cubo("Oreja_Izquierda_006",        (m*5,    ((m*10)/3)*2, m*2    ),    ((-m*2)+(-m*5), (((m*10)/3)*2)-m, m        ),  tipo="orejas")
        oreja_der = crear_cubo("Oreja_Derecha_007",          (m*5,    ((m*10)/3)*2, m*2    ),    ((m*2), (((m*10)/3)*2)-m, m        ),  tipo="orejas")
        cabeza = crear_cubo("Cabeza_Primitiva_001",          (m*14,   m*10,         m*10   ),    ((-m*7),      0,                (m*5)    ),  tipo="cabeza")
        ojo_izq = crear_cubo("OjoIzquierdo_Primitiva_002",   (m*1.5,  m*1.5,        (m)  ),    ((-m*0.75)-7, (-(m*10)/3.7),    (m*5.5) ),  tipo="ojos")
        ojo_der = crear_cubo("OjoDerecho_Primitiva_003",     (m*1.5,  m*1.5,        (m)  ),    ((-m*0.75)+7, (-(m*10)/3.7),    (m*5.5) ),  tipo="ojos")
        nariz = crear_cubo("Nariz_Primitiva_004",            (m,      m,            (m)  ),    ((-m/2),      (-(m*10)/2),      (m*5.5) ),  tipo="nariz")

        tronco = crear_cubo("Tronco_Primitiva_010",          (m*19,   m*13,         (m*16)/2 ),    ((-m*9.5),    (-m*9),          (m*8)/2 ),  tipo="tronco")
        mano_izq = crear_cubo("ManoIzquierda_Primitiva_011", (m*7,    m*5,          m*5      ),    ((-m*9.5)+(-m*6), (-m*10.5),         (m*2.5) ),  tipo="manos")
        mano_der = crear_cubo("ManoDerecha_Primitiva_012",   (m*7,    m*5,          m*5      ),    ((m*8.5), (-m*10.5),         (m*2.5) ),  tipo="manos")
        pie_izq = crear_cubo("PieIzquierdo_Primitiva_008",   (m*5,    m*6,          m*5      ),    ((-m*2)+(-m*5), (-m*21),         (m*2.5) ),  tipo="piernas")
        pie_der = crear_cubo("PieDerecho_Primitiva_009",     (m*5,    m*6,          m*5      ),    ((m*2), (-m*21),         (m*2.5) ),  tipo="piernas")
        cola = crear_cubo("Cola_Primitiva_013",              (m*5,    m*5,          m*5      ),    ((-m*2.5),     (-m*9)+(-m*7.2), (-m*3.5) ),  tipo="cola")

    parte_superior = cmds.group(cabeza, ojo_izq, ojo_der, nariz, oreja_izq, oreja_der, name="ParteSuperior_Grupo")
    parte_inferior = cmds.group(tronco, mano_izq, mano_der, pie_izq, pie_der, cola, name="ParteInferior_Grupo")

   
    conejo = cmds.group(parte_superior, parte_inferior, name="Conej_Grupo_001") # grupo temporal por eso le falta una o a conejo 
    base = base_giratoria(nombre="Base_Conejo_014", morfologia=morfologia, emocion=emocion, conejo=conejo)
    conejocompleto =   cmds.group(conejo, base, name="Conejo_Grupo_001")


    piezas_deformables = [
        cabeza,
        tronco,
        mano_izq,
        mano_der,
        pie_izq,
        pie_der,
        oreja_izq,
        oreja_der
    ]

# endregion


# =====================================================
# CREAR BASE DEL CONEJO
# =====================================================
def base_giratoria(nombre, morfologia, emocion, conejo):

    bbox = cmds.exactWorldBoundingBox(conejo)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox
    ancho_conejo = (xmax - xmin)
    centro_x = (xmin + xmax) / 2
    centro_z = (zmin + zmax) / 2

    # ALTURA BASE SEGÚN MORFOLOGÍA

    if morfologia == "vertical":
        posicion_y = (-m*39.6)
        altura_base = m * 3
    else: # estándar y horizontal        
        posicion_y = (-m*27.6)
        altura_base = m * 3

    base = cmds.polyCylinder(   name="Base_Conejo",  r=(ancho_conejo / 2) + (m * 4),   h=altura_base,   sx=30 )[0]     # CREAR CILINDRO
    cmds.delete(base, ch=True)# eliminar history para que no se deforme con el escalado
    cmds.move(   centro_x, posicion_y, centro_z,   base) # POSICIONAR BASE

    return base
        
    # =====================================================
    # SUAVIZAR BASE
    # =====================================================

    #cmds.polySmooth(
        #base,
        #dv=1      
    #) 



