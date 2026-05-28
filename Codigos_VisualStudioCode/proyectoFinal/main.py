
# region 1. Importaciones
import importlib
import os
import maya.cmds as cmds
from proyectoFinal import sistemaIKFKleg, sistemaIKFKspline
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

# region 2. Colores
#  
# =========================
# COLORES para interfaz (RGB normalizados 0–1)
# =========================

# =========================
# HEX → RGB NORMALIZADO MAYA, porque los botones solo reciben rgb pero en hex puedo ver el cuadrito de color aqui en codigo 
# =========================
def hex_a_rgb(hex_color):

    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0

    return (r, g, b)

fondorosado = hex_a_rgb("#ECBCFB")
morado = hex_a_rgb("#FDC8FE")
lila = hex_a_rgb("#CC99FF")
gris = hex_a_rgb("#FBE8FC")
grisoscuro = hex_a_rgb("#E9E6E6")
blanco = hex_a_rgb("#FFFFFF")


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
    global IK_CTRL_COLUMNA
   

    resultado_ikfk = funcionesIniciales.crear_sistema_fkik(
        lista_fk,
        resultado_dup,
        crearConejo.piezas_deformables
    )

    IK_CTRL_COLUMNA = resultado_ikfk["Columna"]["ikControl"]

    print(IK_CTRL_COLUMNA)
    
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

    borrar_escena()
    seleccion = cmds.radioCollection("emociones",q=True, select=True )
    crearConejo.crear_conejo(seleccion)
    global ancho 
    ancho= crearConejo.m * 10

    # =====================================================
    # ACTIVAR SIEMPRE VISTA PERSPECTIVA  3/4
    # =====================================================

    cmds.setAttr("persp.rotateX", -15)
    cmds.setAttr("persp.rotateY", 45)
    cmds.setAttr("persp.rotateZ", 0)

    cmds.setAttr("persp.translateX", 80)
    cmds.setAttr("persp.translateY", 60)
    cmds.setAttr("persp.translateZ", 80)

    # centrar cámara al conejo
    cmds.viewFit("persp")

# =========================
# funcion_de_main_pintar_conejo
# =========================
def funcion_de_main_pintar_conejo(*args):

    seleccion = cmds.radioCollection(
        "emociones",
        q=True,
        select=True
    )

    material = pintarConejo.crear_material_degradado(
        "Conejo",
        seleccion
    )

    cmds.select(crearConejo.piezas_deformables)

    cmds.hyperShade(assign=material)

    # activar texturas en viewport
    paneles = cmds.getPanel(type='modelPanel')

    for panel in paneles:

        cmds.modelEditor(
            panel,
            edit=True,
            displayTextures=True,
            displayAppearance='smoothShaded'
        )

    cmds.refresh(force=True)

    print("✅ Conejo pintado correctamente")


def suavizar_geometria_de_conejo(*args):

    crearConejo.suavizar_conejo()
    crearConejo.deformar_cara_con_plano()



def cambiar_fk_ik(*args):

    global IK_CTRL_COLUMNA

    if not IK_CTRL_COLUMNA:
        cmds.warning("Primero crea el esqueleto IK/FK")
        return

    seleccion = cmds.radioCollection(
        "fkik_collection",
        q=True,
        select=True
    )

    if seleccion == "radio_fk":

        sistemaIKFKspline.cambiar_fkik(
            IK_CTRL_COLUMNA,
            0
        )
        sistemaIKFKleg.cambiar_fkik_leg(0)

        print("Modo FK")

    elif seleccion == "radio_ik":

        sistemaIKFKspline.cambiar_fkik(
            IK_CTRL_COLUMNA,
            1
        )
        sistemaIKFKleg.cambiar_fkik_leg(1)

        print("Modo IK")

# =========================
# POPUP FINAL CONEJITO
# =========================
def mostrar_popup_final(*args):

    ancho_cabeza = crearConejo.ancho_cabeza

    if 20 <= ancho_cabeza <= 27:
        morfologia = "Vertical"

    elif 28 <= ancho_cabeza <= 35:
        morfologia = "Estandar"

    elif 36 <= ancho_cabeza <= 43:
        morfologia = "Horizontal"

    emocion = cmds.radioCollection("emociones", q=True, select=True)
    dato_curioso = pintarConejo.generar_dato_curioso(emocion)

    mensaje = (
        "\n¡Haz creado una Dulce Fortuna! 🐇 \n\n"        
        f" 🐰 Morfología: {morfologia} "
        f" ({ancho_cabeza} cm)\n\n"
        f" 🐰 Emoción: {emocion}\n\n"
        f"{dato_curioso}\n"
    )

    cmds.confirmDialog(
        title="Mi Dulce Fortuna",
        message=mensaje,
        button=["¡ Quiero girarlo ! "],
        defaultButton="¡ Quiero girarlo ! ",
        bgc=fondorosado
    )

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
def crear_ui(*args):
   
    if cmds.window("miVentanaConejo", exists=True):
        cmds.deleteUI("miVentanaConejo")

    # =========================
    # MEDIDAS
    # =========================
    anchomenu=300
    anchoimagen=300
    altoimagen=300
    anchoventana=anchomenu
    altoventana=900
    ventana = cmds.window("miVentanaConejo", title="MI DULCE FORTUNA", widthHeight=(anchoventana,altoventana),sizeable=False)
    cmds.window(
    ventana,
    edit=True,
    widthHeight=(anchoventana, altoventana)
)
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
    cmds.separator(h=4, style="none") #espacio vacio    
    # Raya division
    cmds.text(label="", bgc=lila,height=4) 


    #---titulo
    cmds.separator(h=4, style="none") #espacio vacio
    cmds.text(label="   🐇   MI DULCE FORTUNA   🐇  ",height=27, width=anchomenu,bgc=lila, font="boldLabelFont", align="center")
        
    #---Raya division lila
    cmds.separator(h=4, style="none") #espacio vacio
    # Raya division
    cmds.text(label="", bgc=lila,height=4) 


    #---Texto instruccion
    cmds.separator(h=10, style="none") #espacio vacio
    cmds.text(label="Selecciona una emoción y luego los botones en orden", bgc=fondorosado)

#region 4.1.2.1. Emociones 
  
        # =========================
        # EMOCIONES A 3 COLUMNAS
        # =========================
       
    cmds.separator(h=10, style="none")

    # CONTENEDOR GENERAL PARA CENTRAR
    cmds.rowLayout( numberOfColumns=3,columnWidth3=(40, 220, 40))
    cmds.text(label="")  # espacio izquierdo

        # =========================
        # TABLA DE 4 COLUMNAS
        # [ radio ] [ corazon ] [ radio ] [ corazon ]
        # =========================

    cmds.rowColumnLayout( numberOfColumns=4,columnWidth=[(1,65), (2,20), (3,65),(4,20)], columnSpacing=[(1,10),(2,5),(3,30)], rowSpacing=(1,3) )
    cmds.radioCollection("emociones")

    cmds.radioButton( "descanso",  label="Descanso", align="center",  select=True  )
    cmds.text(label="💚", align="center")
    cmds.radioButton(  "feo", label="Feo", align="center"  )
    cmds.text(label="🤎", align="center")

    cmds.radioButton( "pequeno", label="Pequeño", align="center" )
    cmds.text(label="🩷", align="center")
    cmds.radioButton( "fantasia", label="Fantasía", align="center")
    cmds.text(label="🧡", align="center")

    cmds.radioButton( "odio",label="Odio",align="center" )
    cmds.text(label="🖤", align="center")
    cmds.radioButton("infiel",label="Infiel",align="center" )
    cmds.text(label="💛", align="center")

    cmds.radioButton("artificial",label="Artificial",align="center" )
    cmds.text(label="💜", align="center")
    cmds.radioButton("verdad",label="Verdad",align="center"  )
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
    cmds.separator(h=10, style="none") #espacio vacio
    # Raya division
    cmds.text(label="", bgc=lila,height=5) 


        # =========================
        # 🔘 BOTÓN GENERAR CONEJO CUADRADO
        # =========================

    cmds.separator(h=10, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,85), (2,120),(3,60)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label="🧊 Crear conejo",command=funcion_de_main_crear_conejo_cuadrado, bgc=gris,height=28 )
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este

        # =========================
        # 🔘 BOTÓN PINTAR CONEJO
        # =========================

    cmds.separator(h=8, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,85), (2,120),(3,60)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label="🎨 Pintar ",command=funcion_de_main_pintar_conejo, bgc=gris,height=28 )
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este

    
        # =========================
        # 🔘 BOTÓN Redondear (suavizar forma)
        # =========================
        
    cmds.separator(h=8, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,85), (2,120),(3,60)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label="🛞 Redondear ",command=suavizar_geometria_de_conejo,bgc=gris,height=28)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui


        # =========================
        # 🔘 BOTÓN crear_sistema fk to ik 
        # =========================
        
    cmds.separator(h=8, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,85), (2,120),(3,60)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label="🦴 Crear esqueleto ",command=generar_conejo_ui,bgc=gris,height=28)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui

    # =========================
    # CHECKS FK / IK
    # =========================

    cmds.separator(h=5, style="none")
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1,50),(2,190),(3,50) ] )
    cmds.text(label="")

    # FK
        # =========================
    # FK / IK RADIO BUTTONS
    # =========================

    cmds.radioCollection("fkik_collection")

    cmds.radioButton(
        "radio_fk",
        label="Quiero rotar hueso por hueso (FK)",
        select=True,
        onc=cambiar_fk_ik
    )

    cmds.radioButton(
        "radio_ik",
        label="Quiero rotar hueso con vecinos (IK)",
        onc=cambiar_fk_ik
)


        # =========================
        # 🔘 BOTÓN crear_sistema fk to ik 
        # =========================
        
    cmds.separator(h=8, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,75), (2,140),(3,60)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label="🐇 Terminar mi conejito ",command=mostrar_popup_final,bgc=lila,height=28)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui


        # =========================
        # 🔘 BOTÓN Borrar escena 
        # =========================
    cmds.separator(h=8, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,205), (2,80),(3,20)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    cmds.button(label="🧹Borrar todo ",command=borrar_escena,bgc=grisoscuro,height=28)
    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este
    cmds.separator(h=8, style="none") #espacio vacio

#endregion de la seccion botones


#region 4.2. creditos 

        # =========================
        # CRÉDITOS FINALES 
        # =========================
    # Raya division
    cmds.text(label="", bgc=lila,height=5) # Raya division
    cmds.separator(h=8, style="none") #espacio vacio 
    cmds.text(label="Mayerly Camargo Pedraza - Código 1202327", bgc=fondorosado,font="smallPlainLabelFont")
    cmds.text(label="Jennifer Leiva Martín - Código 1202617", bgc=fondorosado,font="smallPlainLabelFont")
    cmds.text(label="Docente: Diego Beltrán Cardona- UMNG 2026", bgc=fondorosado,font="smallPlainLabelFont")   
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
borrar_escena() #limpio
crear_ui()


# region Notas

#                         ╔═════════════════════════════════════════════════════════════════╗
#                         ║  Notas                                                          ║
#                         ╚═════════════════════════════════════════════════════════════════╝
