import maya.cmds as cmds
import random # Generar números aleatorios.

# Variable global para modulo
m = 1
morfologia= "estandar"

#  region Funcion crear_cubo
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Entender como Maya saca las formas, Funcion crear_cubo         ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝

def crear_cubo(nombre, escala, posicion): 
    ancho, alto, profundidad = escala # Definimos nombre de los valores de la escala, en lugar de w.h.d  por defecto.

    """
    Creamos una función reutilizable para dibujar n cubos.
    parametros: nombre STRING que llevara el cubo en el ouliner de maya (string), 
                 escala VECTOR (3 valores para x= ancho, y= alto, z= profundidad),
                posicion VECTOR (3 valores para coordenadas x,y,z)
    """

    subdivisiones=(2,2,2)
    sx , sy , sz = subdivisiones
  
    cubo = cmds.polyCube( name=nombre, w=ancho, h=alto, d=profundidad, sx=3,sy=3,sz=3)[0]  

    """
    Creamos un cubo con el comando polyCube y le asignamos un nombre y una escala
        la razon por la que usamos una lista, es porque polycube devuelve una lista, 
        En la que el primer elemento es el objeto (la geometria)
        y el segundo elemento es las transformaciones que se le han hecho
        nosotros cogemos la primera que es el objeto y le asigamos nombre y escala. 
    """
    
    """
    Calculamos el offset de la posicion,  por defecto el cubo se crea con su centro en el origen (0,0,0),
    y nosotros queremos que el punto de referencia sea la esquina superior izquierda de la cara frontal del cubo,
              y que se dibuje de ahi para abajo y hacia la derecha y la sobre el plano xy osea z=0
    Al finalizar el conejo debemos reubicar los pivotes para que los joints se creen en el centro de las formas.
    """
    offset_x = ancho / 2
    offset_y = -(alto / 2)
    offset_z = -(profundidad / 2)
    cmds.move(posicion[0] + offset_x, posicion[1] + offset_y, posicion[2] + offset_z, cubo)
    
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
    global morfologia

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

    morfologia = "estandar"

    if 20 <= ancho_cabeza <= 27:
        morfologia = "vertical"

    elif 28 <= ancho_cabeza <= 35:
        morfologia = "estandar"

    elif 36 <= ancho_cabeza <= 43:
        morfologia = "horizontal"

    print(" 📐🐰 Morfología:", morfologia)

    if morfologia == "vertical":
        #                            nombre                            escala                            posicion 
        cabeza = crear_cubo("Cabeza_Primitiva_001",          (m*10,   m*10,         (m*10)/2 ),    (0,     0,                  0          )  ) 
        ojo_izq = crear_cubo("OjoIzquierdo_Primitiva_002",   (m,      m,            (m*1.7)  ),    (m*7,   (-(m*10)/3.7),      (m*1.7)-m  )  )
        ojo_der = crear_cubo("OjoDerecho_Primitiva_003",     (m,      m,            (m*1.7)  ),    (m*2,   (-(m*10)/3.7),      (m*1.7)-m  )  )
        nariz = crear_cubo("Nariz_Primitiva_004",            (m,      m,            (m*1.7)  ),    (m*4.5, (-(m*10)/2),        (m*1.7)-m  )  )
        boca = crear_cubo("Boca_Primitiva_005",              (m*3,    m/2,          (m*1.7)  ),    (m*3.5, (-(m*10)/1.33),     (m*1.7)-m  )  )
        oreja_izq = crear_cubo("Oreja_Izquierda_006",        (m*3,    ((m*10)/3)*2, m*2      ),    (m*6,   (((m*10)/3)*2)-m,   (-m*1.5)   )  )
        oreja_der = crear_cubo("Oreja_Derecha_007",          (m*3,    ((m*10)/3)*2, m*2      ),    (m,     (((m*10)/3)*2)-m,   (-m*1.5)   )  )
        

        pie_izq = crear_cubo("PieIzquierdo_Primitiva_008",   (m*3,    m*5,          m*2      ),    (m*6,    (-m*28.3),              (-m*1.5))) #CAMBIÓ
        pie_der = crear_cubo("PieDerecho_Primitiva_009",     (m*3,    m*5,          m*2      ),    (m,      (-m*28.3),              (-m*1.5))) #CAMBIÓ
        tronco = crear_cubo("Tronco_Primitiva_010",          (m*13,   m*20,         (m*16)/2 ),    (-m*1.5, (-m*9),            (m*1.5) ) ) #CAMBIÓ
        mano_izq = crear_cubo("ManoIzquierda_Primitiva_011", (m*4,    m*3,          m*2      ),    (m*10.5, (-m*12),           (-m*1.5)   )  )
        mano_der = crear_cubo("ManoDerecha_Primitiva_012",   (m*4,    m*3,          m*2      ),    (-m*4.5, (-m*12),           (-m*1.5)   )  )
        cola = crear_cubo("Cola_Primitiva_013",              (m,      m,            m*2      ),    (m*4.5,  (-m*9)+(-m*12),   (-m*5.5)   )  ) #CAMBIÓ

    
    elif morfologia == "estandar":
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
    
    elif morfologia == "horizontal":
        #                            nombre                            escala                            posicion 
        cabeza = crear_cubo("Cabeza_Primitiva_001",          (m*10,   m*10,         (m*10)/2 ),    (0,     0,                  0          )  ) 
        ojo_izq = crear_cubo("OjoIzquierdo_Primitiva_002",   (m,      m,            (m*1.7)  ),    (m*7,   (-(m*10)/3.7),      (m*1.7)-m  )  )
        ojo_der = crear_cubo("OjoDerecho_Primitiva_003",     (m,      m,            (m*1.7)  ),    (m*2,   (-(m*10)/3.7),      (m*1.7)-m  )  )
        nariz = crear_cubo("Nariz_Primitiva_004",            (m,      m,            (m*1.7)  ),    (m*4.5, (-(m*10)/2),        (m*1.7)-m  )  )
        boca = crear_cubo("Boca_Primitiva_005",              (m*3,    m/2,          (m*1.7)  ),    (m*3.5, (-(m*10)/1.33),     (m*1.7)-m  )  )
        oreja_izq = crear_cubo("Oreja_Izquierda_006",        (m*3,    ((m*10)/3)*2, m*2      ),    (m*6,   (((m*10)/3)*2)-m,   (-m*1.5)   )  )
        oreja_der = crear_cubo("Oreja_Derecha_007",          (m*3,    ((m*10)/3)*2, m*2      ),    (m,     (((m*10)/3)*2)-m,   (-m*1.5)   )  )
        

        pie_izq = crear_cubo("PieIzquierdo_Primitiva_008",   (m*4,    m*3,          m*2      ),    (m*6,    (-m*21),              (-m*1.5)))#CAMBIÓ
        pie_der = crear_cubo("PieDerecho_Primitiva_009",     (m*4,    m*3,          m*2      ),    (0,      (-m*21),              (-m*1.5)))#CAMBIÓ
        tronco = crear_cubo("Tronco_Primitiva_010",          (m*19,   m*13,         (m*16)/2 ),    (-m*4.5, (-m*9),            (m*1.5)   )  )#CAMBIÓ
        mano_izq = crear_cubo("ManoIzquierda_Primitiva_011", (m*4,    m*3,          m*2      ),    (m*13.5, (-m*12),           (-m*1.5)   )  )#CAMBIÓ
        mano_der = crear_cubo("ManoDerecha_Primitiva_012",   (m*4,    m*3,          m*2      ),    (-m*7.5, (-m*12),           (-m*1.5)   )  )
        cola = crear_cubo("Cola_Primitiva_013",              (m,      m,            m*2      ),    (m*4.5,  (-m*9)+(-m*7.2),   (-m*5.5)   )  ) 
    
    parte_superior = cmds.group(cabeza, ojo_izq, ojo_der, nariz, boca, oreja_izq, oreja_der, name="ParteSuperior_Grupo")
    parte_inferior = cmds.group(tronco, mano_izq, mano_der, pie_izq, pie_der, cola, name="ParteInferior_Grupo")
    conejo = cmds.group(parte_superior, parte_inferior, name="Conejo_Grupo_001")

# endregion

#region suavizado
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Suavizar las formas                                            ║                                                               ║
#                         ╚═════════════════════════════════════════════════════════════════╝

def suavizar_conejo_preview():

    objetos = [
        "Cabeza_Primitiva_001",
        "OjoIzquierdo_Primitiva_002",
        "OjoDerecho_Primitiva_003",
        "Nariz_Primitiva_004",
        "Boca_Primitiva_005",
        "Oreja_Izquierda_006",
        "Oreja_Derecha_007",
        "PieIzquierdo_Primitiva_008",
        "PieDerecho_Primitiva_009",
        "Tronco_Primitiva_010",
        "ManoIzquierda_Primitiva_011",
        "ManoDerecha_Primitiva_012",
        "Cola_Primitiva_013"
    ]

    for obj in objetos:
        if cmds.objExists(obj):

            # equivalente a tecla 3
            cmds.setAttr(obj + ".displaySmoothMesh", 2)
            # calidad del preview
            cmds.setAttr(obj + ".smoothLevel", 2)

    print("Conejo suavizado")
# endregion

