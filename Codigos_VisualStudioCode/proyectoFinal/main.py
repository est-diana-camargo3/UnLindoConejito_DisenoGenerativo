
# region 1. Importaciones
import importlib
import os
import maya.cmds as cmds
import proyectoFinal.crearConejo as crearConejo
import proyectoFinal.funcionesFK as funcionesFK
import proyectoFinal.funcionesIniciales as funcionesIniciales
import proyectoFinal.paletas as paletas
import proyectoFinal.pintarConejo as pintarConejo
importlib.reload(crearConejo)
importlib.reload(funcionesFK)
importlib.reload(funcionesIniciales)
importlib.reload(paletas)
importlib.reload(pintarConejo)

# endregion

# region 2. Definir colores
#  
# =========================
# COLORES para interfaz (RGB normalizados 0–1)
# =========================

fondorosado = (236/255, 188/255, 251/255)   # #ecbcfb
morado = (182/255, 135/255, 232/255)   # 9C48CF
lila = (204/255, 153/255, 255/255)   # CC99FF
gris = (245/255, 240/255, 250/255)    #747474 
grisoscuro = (220/255, 220/255, 220/255)    #545353
blanco = (1,1,1)

# endregion

#region 3. Funciones UI

# =========================
# FUNCIÓN DEL BOTÓN GENERAR
# =========================
def generar_conejo_ui(*args):
    
    funcionesIniciales.crear_jerarquia_general()
    lista_fk = funcionesFK.crear_joints_coplanares(crearConejo.m)
    funcionesFK.orientar_joints_de_toda_la_cadena_FK(lista_fk)
    resultado_dup = funcionesFK.duplicar_y_renombrar_cadenas_IK_y_MAIN()
    funcionesFK.ocultar_cadenas_IK_y_MAIN()
    funcionesIniciales.organizar_cadenas_principales()
    funcionesFK.crear_fk_auto_root_control(lista_fk)
    
    funcionesIniciales.crear_sistema_fkik(
        lista_fk,
        resultado_dup,
        crearConejo.piezas_deformables
    )

    funcionesIniciales.crear_master_control()
    
    funcionesIniciales.crear_controles_anatomicos()

    funcionesIniciales.crear_jerarquia_anatomica()

    funcionesIniciales.conectar_columna_a_controles()

    funcionesIniciales.conectar_extremidades()

    funcionesIniciales.conectar_partes_secundarias()

    
    #suavizar_conejo_preview()

# =========================
# funcion_de_main_crear_conejo_cuadrado
# =========================
def funcion_de_main_crear_conejo_cuadrado(*args):

    seleccion = cmds.radioCollection("emociones",q=True, select=True )
    estilo = cmds.radioCollection("estilos",q=True,select=True)
    crearConejo.crear_conejo(seleccion)
    global ancho 
    ancho= crearConejo.m * 10
    cmds.text( "textoModulo", edit=True,  label=f"Ancho cabeza: {ancho:.1f} cm | Morfología: {crearConejo.morfologia}" )

# =========================
# funcion_de_main_pintar_conejo
# =========================
def funcion_de_main_pintar_conejo(*args):

    seleccion = cmds.radioCollection("emociones",q=True, select=True )
    estilo = cmds.radioCollection("estilos",q=True,select=True)
    pintarConejo.aplicar_estilo(seleccion,estilo)
    cmds.text( "textoModulo2", edit=True,  label=f"Dato Curioso: {pintarConejo.dato_curioso}" )

# =========================
# funcion mostrar_gizmos_pivotes
# =========================
def mostrar_gizmos_pivotes(*args):
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

# =========================
# funcion ocultar_gizmos_pivotes
# ========================= 
def ocultar_gizmos_pivotes(*args):
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

# =========================
# funcion_de_main_crear_jerarquia_general
# ========================= 
#def funcion_de_main_crear_jerarquia_general(*args):
    #funcionesIniciales.crear_jerarquia_general()


# =========================
# FUNCIÓN BOTÓN BORRAR
# =========================
def borrar_escena(*args):
    cmds.select(all=True)
    cmds.delete()

#endregion de la seccion borrar escena 

#region 4. Interfaz UI

#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Interfaz UI                                                    ║
#                         ╚═════════════════════════════════════════════════════════════════╝

#region 4.1 Ventana Medidas   
# =========================
# CREACIÓN UI
# =========================
def crear_ui():
   
    if cmds.window("miVentanaConejo", exists=True):
        cmds.deleteUI("miVentanaConejo")

    # =========================
    # MEDIDAS
    # =========================
    anchomenu=300
    anchoimagen=300
    altoimagen=330
    anchoventana=anchomenu
    altoventana=850
    ventana = cmds.window("miVentanaConejo", title="MI DULCE FORTUNA", widthHeight=(anchoventana,altoventana),sizeable=False)

#endregion de la seccion ventana medidas 

#region 4.1.1.Imagen

    # =========================
    # LAYOUT PRINCIPAL (1 COLUMNA)
    # =========================
    cmds.columnLayout(adjustableColumn=True, width=anchoventana, bgc=fondorosado) #[ elemento ] # apartir de aqui voy a crear una columna 

    # =========================
     # 🖼️ (Imagen Centrada)
    # =========================

    #asi lo tenias tu
    #ruta_actual = os.getcwd()
    #ruta_imagen = os.path.join(
        #ruta_actual,
        #"ImagenMenu.png"
    #)
    #ruta_imagen = ruta_imagen.replace("\\", "/")
    #cmds.columnLayout(width=300)
    #cmds.image(image=ruta_imagen)
    #cmds.setParent('..')

    # Asi lo tengo yo, prueba haber si te funciona
    # =========================
    # 🖼️ (Imagen Centrada)
    # =========================
    
    #cmds.separator(h=20, style="none") #espacio vacio
    cmds.rowLayout(numberOfColumns=3,columnWidth3=(20, anchoimagen, 20),bgc=fondorosado)
    ruta_imagen = "C:/Users/USUARIO/Documents/GitHub/UnLindoConejito_DisenoGenerativo/Imagenes/ImagenMenu.png"
    cmds.image(image=ruta_imagen,width=anchoimagen,height=altoimagen)
    cmds.setParent('..') # cerrar rowLayout de la imagen para que el siguiente elemento no quede dentro de este

#endregion de la seccion imagen 
   
#region 4.1.2.Menú

    # =========================
    # 🎛️ (MENÚ)
    # =========================
    #---Raya division lila
    cmds.separator(h=10, style="none") #espacio vacio    
    cmds.text(label="", height=5, width=anchomenu,bgc=morado)

    #---titulo
    cmds.separator(h=4, style="none") #espacio vacio
    cmds.text(label="   🐰   MI DULCE FORTUNA   🐰  ",height=30, width=anchomenu,bgc=morado, font="boldLabelFont", align="center")
        
    #---Raya division lila
    cmds.separator(h=4, style="none") #espacio vacio
    cmds.text(label="", height=5, width=anchomenu,bgc=morado)

    #---Texto instruccion
    cmds.separator(h=13, style="none") #espacio vacio
    cmds.text(label="Selecciona una emoción", bgc=fondorosado)

#region 4.1.2.1. Emociones 
  
    # =========================
    # EMOCIONES A 3 COLUMNAS
    # =========================
       
    cmds.separator(h=10, style="none")

    # CONTENEDOR GENERAL PARA CENTRAR
    cmds.rowLayout(
        numberOfColumns=3,
        columnWidth3=(40, 220, 40)
    )

    cmds.text(label="")  # espacio izquierdo

    # =========================
    # TABLA DE 4 COLUMNAS
    # [ radio ] [ corazon ] [ radio ] [ corazon ]
    # =========================

    cmds.rowColumnLayout(
        numberOfColumns=4,
        columnWidth=[
            (1,65),
            (2,20),
            (3,65),
            (4,20)
        ],
        columnSpacing=[
            (1,10),
            (2,5),
            (3,30)
        ],
        rowSpacing=(1,5)
    )

    cmds.radioCollection("emociones")

    # FILA 1
    cmds.radioButton(
        "descanso",
        label="Descanso",
        align="center",
        select=True
    )
    cmds.text(label="💚", align="center")

    cmds.radioButton(
        "infidelidad",
        label="Feo",
        align="center"
    )
    cmds.text(label="🤎", align="center")

    # FILA 2
    cmds.radioButton(
        "barato",
        label="Pequeño",
        align="center"
    )
    cmds.text(label="🩷", align="center")

    cmds.radioButton(
        "fantasia",
        label="Fantasía",
        align="center"
    )
    cmds.text(label="🧡", align="center")

    # FILA 3
    cmds.radioButton(
        "odio",
        label="Odio",
        align="center"
    )
    cmds.text(label="🖤", align="center")

    cmds.radioButton(
        "envidia2",
        label="Envidia",
        align="center"
    )
    cmds.text(label="💛", align="center")

    # FILA 4
    cmds.radioButton(
        "cortesia",
        label="Artificial",
        align="center"
    )
    cmds.text(label="💜", align="center")

    cmds.radioButton(
        "envidia",
        label="Verdad",
        align="center"
    )
    cmds.text(label="🤍", align="center")

    cmds.setParent('..')  # cerrar rowColumnLayout

    cmds.text(label="")  # espacio derecho

    cmds.setParent('..')  # cerrar rowLayout



#endregion de la seccion emociones


#region 4.1.2.2. Botones

    # =========================
    # 🔘 BOTONES 
    # =========================
     #---Raya division lila
    cmds.separator(h=15, style="none") #espacio vacio
    cmds.text(label="", height=3, width=anchomenu,bgc=morado)
    cmds.separator(h=3, style="none") #espacio vacio
    cmds.text(label="", height=3, width=anchomenu,bgc=morado)

    #---Texto instruccion
    cmds.separator(h=13, style="none") #espacio vacio
    cmds.text(label="Selecciona los botones en orden", bgc=fondorosado)


        # =========================
        # 🔘 BOTÓN GENERAR CONEJO CUADRADO
        # =========================

    cmds.separator(h=8, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,80), (2,140),(3,60)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label="🧊 Crear conejo ",command=funcion_de_main_crear_conejo_cuadrado, bgc=gris,height=30 )
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este

        # =========================
        # 🔘 BOTÓN PINTAR CONEJO
        # =========================

    cmds.separator(h=8, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,80), (2,140),(3,80)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label="🎨 Pintar conejo ",command=funcion_de_main_pintar_conejo, bgc=gris,height=30 )
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este

        # =========================
        # 🔘 BOTÓN crear_sistema fk to ik 
        # =========================
        
    cmds.separator(h=8, style="none")
    cmds.rowLayout(numberOfColumns=3,columnWidth= [(1,80), (2,140),(3,80)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label="🦴 Crear esqueleto ",command=generar_conejo_ui,bgc=gris,height=30)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui

        # =========================
        # 🔘 BOTÓN Borrar escena 
        # =========================
    cmds.separator(h=10, style="none")
    cmds.rowLayout(numberOfColumns=3,columnWidth= [(1,80), (2,140),(3,80)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label="🧹 Borrar Escena ",command=borrar_escena,bgc=grisoscuro,height=30)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este
    cmds.separator(h=10, style="none") #espacio vacio
#endregion de la seccion botones


#region 4.2. creditos 

        # =========================
        # CRÉDITOS FINALES 
        # =========================
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

#endregion de la seccion creditos
# endregion de la seccion menu
#endregion de la seccion interfaz UI

# =========================
# EJECUTAR UI
# =========================
crear_ui()


# region Notas

#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Notas                                                          ║
#                         ╚═════════════════════════════════════════════════════════════════╝
