
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



# region ui
#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Interfaz UI                                                    ║
#                         ╚═════════════════════════════════════════════════════════════════╝


# =========================
# FUNCIÓN DEL BOTÓN GENERAR
# =========================
def generar_conejo_ui(*args):
    
    #esto ya esta abajo en funcion_de_main_crear_conejo_cuadrado y funcion_de_main_pintarconejo  
      
    #seleccion = cmds.radioCollection("emociones", q=True, select=True)
    #estilo = cmds.radioCollection("estilos",q=True,select=True)
    #crearConejo.crear_conejo(seleccion)    
    #pintarConejo.aplicar_estilo(seleccion,estilo)
    #ancho = crearConejo.m * 10

    cmds.text(    "textoModulo",  edit=True,  label=f"Ancho cabeza: {ancho:.1f} cm | Morfología: {crearConejo.morfologia}"   )
    cmds.text(    "textoModulo2",  edit=True,  label=f"Dato Curioso: {pintarConejo.dato_curioso}"   )

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
# COLORES para interfaz (RGB normalizados 0–1)
# =========================

fondorosado = (236/255, 188/255, 251/255)   # #ecbcfb
morado = (182/255, 135/255, 232/255)   # 9C48CF
lila = (204/255, 153/255, 255/255)   # CC99FF
gris = (245/255, 240/255, 250/255)    # #747474
blanco = (1,1,1)


# =========================
# FUNCIÓN BOTÓN BORRAR
# =========================
def borrar_escena(*args):
    cmds.select(all=True)
    cmds.delete()

# =========================
# FUNCIÓN 
# =========================
def funcion_de_main_crear_conejo_cuadrado(*args):

    seleccion = cmds.radioCollection("emociones",q=True, select=True )
    estilo = cmds.radioCollection("estilos",q=True,select=True)
    crearConejo.crear_conejo(seleccion)
    ancho = crearConejo.m * 10
    cmds.text( "textoModulo", edit=True,  label=f"Ancho cabeza: {ancho:.1f} cm | Morfología: {crearConejo.morfologia}" )

# =========================
# FUNCIÓN 
# =========================
def funcion_de_main_pintar_conejo(*args):

    seleccion = cmds.radioCollection("emociones",q=True, select=True )
    estilo = cmds.radioCollection("estilos",q=True,select=True)
    pintarConejo.aplicar_estilo(seleccion,estilo)
    cmds.text( "textoModulo2", edit=True,  label=f"Dato Curioso: {pintarConejo.dato_curioso}" )


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

#Por si en un futuro queremos ocultar los gizmos de los pivotes 
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
# CREACIÓN UI
# =========================
def crear_ui():

    # rowLayout UNA sola fila horizontal.  
    #                                       [ elemento ][ elemento ][ elemento ]
    # rowColumnLayout sirve para organizar tablas 
    #                                       [ elemento ][ elemento ][ elemento ]
    #                                       [ elemento ][ elemento ][ elemento ]
    #                                       [ elemento ][ elemento ][ elemento ]
    # En Maya no creamos las filas de manera manual estas se crean con rowColumnLayout dependiendo de cuantos 
    # elementos agreguemos, por ejemplo si hacemos un rowColumnLayout de 3 columnas y agregamos 6 elementos se van a organizar asi:
    #  1 | 2 | 3
    #  4 | 5 | 6...y asi sucesivamente dependiendo cuandos elementos agreguemos.
    # cmds.columnLayout crea columna vertical
    # cmds.columnLayout(  columnAttach=("left", 30)) #Padding interno
    
    #---Raya division lila
    #cmds.separator(h=5, style="none") #espacio vacio
    #cmds.text(label="", height=6, width=anchomenu,bgc=lila)
    
    if cmds.window("miVentanaConejo", exists=True):
        cmds.deleteUI("miVentanaConejo")

    # =========================
    # MEDIDAS
    # =========================
    anchomenu=318
    anchoimagen=300
    anchoventana=anchomenu
    altoventana=800
    ventana = cmds.window("miVentanaConejo", title="MI DULCE FORTUNA", widthHeight=(anchoventana,altoventana),sizeable=False)

    # =========================
    # SCROLL GENERAL
    # =========================
    cmds.scrollLayout(
        verticalScrollBarThickness=16,
        horizontalScrollBarThickness=0
    )

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
    cmds.image(image=ruta_imagen,width=anchomenu)
    cmds.setParent('..') # cerrar rowLayout de la imagen para que el siguiente elemento no quede dentro de este


    # =========================
    # 🎛️ (MENÚ)
    # =========================
    #---Raya division lila
    cmds.separator(h=10, style="none") #espacio vacio    
    cmds.text(label="", height=5, width=anchomenu,bgc=morado)

    #---titulo
    cmds.separator(h=4, style="none") #espacio vacio
    cmds.text(label="MI DULCE FORTUNA",height=30, width=anchomenu,bgc=morado, font="boldLabelFont", align="center")
        
    #---Raya division lila
    cmds.separator(h=4, style="none") #espacio vacio
    cmds.text(label="", height=5, width=anchomenu,bgc=morado)

    #---Texto instruccion
    cmds.separator(h=13, style="none") #espacio vacio
    cmds.text(label="Selecciona una emoción", bgc=fondorosado)

    
    # =========================
    # EMOCIONES A 3 COLUMNAS
    # =========================
       
    cmds.separator(h=15, style="none") #espacio vacio
    # layout de 2 columnas
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,100), (2,100),(3,100)],columnSpacing=[(1,15)], rowSpacing=(1,5))
    #mcolumnSpacing=[(1,15)]desde la columna 1 coloca → 15 px de separación entre columnas

    cmds.radioCollection("emociones")

    cmds.radioButton("descanso",label="Descanso 🌿", select=True )
    cmds.radioButton("fantasia",label="Fantasía ✨")
    cmds.radioButton("odio",label="Odio 😠")
    cmds.radioButton("barato",label="Barato 🛒")
    cmds.radioButton("envidia",label="Envidia 🟩" )
    cmds.radioButton("infidelidad", label="Infidelidad 💛" )
    cmds.radioButton("cortesia", label="Cortesía 🌸" )
    cmds.radioButton("feo", label="Feo 🪨" )
    cmds.setParent('..')# cerrar rowColumnLayout de las columnas de las emociones 

    # =========================
    # 🎨 ESTILOS GRÁFICOS 
    # =========================
    cmds.separator(h=15, style="none")
    cmds.text( label="Selecciona un estilo gráfico",  bgc=fondorosado )
    cmds.separator(h=10, style="none") #espacio vacio
    cmds.radioCollection("estilos")
    cmds.radioButton( "pixelart", label=" Pixel Art ▀▄ ", select=True )
    cmds.radioButton( "bento", label=" Bento Art 📦 " )

    # =========================
    # 🔘 BOTONES 
    # =========================
     #---Raya division lila
    cmds.separator(h=20, style="none") #espacio vacio
    cmds.text(label="", height=3, width=anchomenu,bgc=lila)

    #---titulo
    cmds.separator(h=3, style="none") #espacio vacio
    cmds.text(label="GEOMETRÍA BÁSICA",height=20, width=anchomenu,bgc=lila, font="boldLabelFont", align="left")
   
    #---Raya division lila
    cmds.separator(h=3, style="none") #espacio vacio
    cmds.text(label="", height=3, width=anchomenu,bgc=lila)


        # =========================
        # 🔘 BOTÓN GENERAR CONEJO CUADRADO
        # =========================

    cmds.separator(h=15, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label="🧊 Crear conejo cuadrado ",command=funcion_de_main_crear_conejo_cuadrado, bgc=gris,height=30 )
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este

    #texto para mostrar el ancho de cabeza generado y como varia 
    cmds.separator(h=5, style="none")
    cmds.text( "textoModulo", label="Ancho de cabeza: --- cm | Morfología: ---", bgc=fondorosado, align="center" )

        # =========================
        # 🔘 BOTÓN mostrar gizmos pivotes
        # =========================
    cmds.separator(h=5, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label="🕹️ Mostrar gizmos pivotes de cubos ",command=mostrar_gizmos_pivotes,bgc=gris,height=30)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este
    
        # =========================
        # 🔘 BOTÓN ocultar gizmos pivotes
        # =========================
    cmds.separator(h=5, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label=" 🫣 Ocultar gizmos pivotes de cubos ",command=ocultar_gizmos_pivotes,bgc=gris,height=30)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este

    #texto 
    cmds.separator(h=5, style="none")
    cmds.text(label=" 💡 Recuerda: Lo que ves es el gizmo del CUBO ", height=15, width=anchomenu, bgc=fondorosado, align="center")
    cmds.separator(h=5, style="none")
    cmds.text(label="Los gizmos de los JOINTS lo veremos mas adelante", height=15, width=anchomenu, bgc=fondorosado, align="center")
    cmds.separator(h=5, style="none")

            # =========================
        # 🔘 BOTÓN PINTAR CONEJO
        # =========================

    cmds.separator(h=5, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label="🎨 Pintar conejo ",command=funcion_de_main_pintar_conejo, bgc=gris,height=30 )
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este

    #texto para mostrar el ancho de cabeza generado y como varia 
    cmds.separator(h=5, style="none")
    cmds.text( "textoModulo2", label="Dato Curioso: ---", bgc=fondorosado, align="center" )

        # =========================
        # 🔘 BOTÓNES FK IK 
        # =========================

     #---Raya division lila
    cmds.separator(h=20, style="none") #espacio vacio
    cmds.text(label="", height=3, width=anchomenu,bgc=lila)

    #---titulo
    cmds.separator(h=3, style="none") #espacio vacio
    cmds.text(label="SISTEMA FK TO IK ",height=20, width=anchomenu,bgc=lila, font="boldLabelFont", align="left")

    #---Raya division lila
    cmds.separator(h=3, style="none") #espacio vacio
    cmds.text(label="", height=3, width=anchomenu,bgc=lila)


        # =========================
        # 🔘 BOTÓN crear y renombrar joints 
        # =========================

    cmds.separator(h=15, style="none")
    cmds.rowLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label=" 👑 Crear Jerarquia general ",command=generar_conejo_ui,bgc=gris,height=30)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui

   
        # =========================
        # 🔘 BOTÓN crear y renombrar joints 
        # =========================

    cmds.separator(h=15, style="none")
    cmds.rowLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label=" 🦴 Crear y Renombrar joints coplanares ",command=generar_conejo_ui,bgc=gris,height=30)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui

        # =========================
        # 🔘 BOTÓN orientar joints
        # =========================
        
    cmds.separator(h=15, style="none")
    cmds.rowLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label=" ➕ Orientar joints ",command=generar_conejo_ui,bgc=gris,height=30)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui


    
        # =========================
        # 🔘 BOTÓN duplicar y renombrar cadenas
        # =========================
        
    cmds.separator(h=15, style="none")
    cmds.rowLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label=" Duplicar y renombrar cadenas IK Y MAIN ",command=generar_conejo_ui,bgc=gris,height=30)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui


        # =========================
        # 🔘 BOTÓN mostrar cadenas ik y main
        # =========================
        
    cmds.separator(h=15, style="none")
    cmds.rowLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label=" mostrar cadenas ik y main ",command=generar_conejo_ui,bgc=gris,height=30)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui


        # =========================
        # 🔘 BOTÓN ocultar cadenas ik y main
        # =========================
        
    cmds.separator(h=15, style="none")
    cmds.rowLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label=" ocultar cadenas ik y main ",command=generar_conejo_ui,bgc=gris,height=30)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui




        # =========================
        # 🔘 BOTÓN crear_fk_auto_root_control
        # =========================
        
    cmds.separator(h=15, style="none")
    cmds.rowLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label=" crear_fk_auto_root_control ",command=generar_conejo_ui,bgc=gris,height=30)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui



        # =========================
        # 🔘 BOTÓN crear_sistema fk to ik 
        # =========================
        
    cmds.separator(h=15, style="none")
    cmds.rowLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label=" Crear_sistema fk to ik  ",command=generar_conejo_ui,bgc=gris,height=30)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui

        # =========================
        # 🔘 BOTÓNES COLUMNA
        # =========================

     #---Raya division lila
    cmds.separator(h=20, style="none") #espacio vacio
    cmds.text(label="", height=3, width=anchomenu,bgc=lila)

    #---titulo
    cmds.separator(h=3, style="none") #espacio vacio
    cmds.text(label="SISTEMA COLUMNA ",height=20, width=anchomenu,bgc=lila, font="boldLabelFont", align="left")

    #---Raya division lila
    cmds.separator(h=3, style="none") #espacio vacio
    cmds.text(label="", height=3, width=anchomenu,bgc=lila)


        # =========================
        # 🔘 BOTÓN sistema columna
        # =========================

    cmds.separator(h=15, style="none")
    cmds.rowLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label=" 👑 Crear sistema columna ",command=generar_conejo_ui,bgc=gris,height=30)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui


        # =========================
        # 🔘 BOTÓNES LIMPIEZA
        # =========================

     #---Raya division lila
    cmds.separator(h=20, style="none") #espacio vacio
    cmds.text(label="", height=3, width=anchomenu,bgc=lila)

    #---titulo
    cmds.separator(h=3, style="none") #espacio vacio
    cmds.text(label="LIMPIEZA ",height=20, width=anchomenu,bgc=lila, font="boldLabelFont", align="left")

    #---Raya division lila
    cmds.separator(h=3, style="none") #espacio vacio
    cmds.text(label="", height=3, width=anchomenu,bgc=lila)


        # =========================
        # 🔘 BOTÓN Borrar escena 
        # =========================
    cmds.separator(h=15, style="none")
    cmds.rowLayout(numberOfColumns=3,columnWidth= [(1,50), (2,200),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label=" Borrar Escena 🧹 ",command=borrar_escena,bgc=gris,height=30)
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
