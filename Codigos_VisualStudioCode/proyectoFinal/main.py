
# region 1. Importaciones
import importlib
import os
import random #aleatoriedad para el conejo sorpresa
import maya.cmds as cmds
from proyectoFinal import sistemaIKFKleg, sistemaIKFKspline
import proyectoFinal.crearConejo as crearConejo
import proyectoFinal.funcionesFK as funcionesFK
import proyectoFinal.funcionesIniciales as funcionesIniciales
import proyectoFinal.paletas as paletas
import proyectoFinal.pintarConejo as pintarConejo
import proyectoFinal.posesui as posesui
import proyectoFinal.props as props
import proyectoFinal.tomarfoto as tomarfoto
importlib.reload(crearConejo)
importlib.reload(funcionesFK)
importlib.reload(funcionesIniciales)
importlib.reload(paletas)
importlib.reload(pintarConejo)
importlib.reload(posesui)
importlib.reload(props)
importlib.reload(tomarfoto)


import os
import proyectoFinal

ruta_base = os.path.dirname(proyectoFinal.__file__)
AUTO_TOOL_SCRIPTJOB = None


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
# CAMBIAR TOOL SEGUN CONTROL
# =========================
def _atributo_control_activo(objeto, atributos):
    if not objeto or not cmds.objExists(objeto):
        return False

    for attr in atributos:
        plug = f"{objeto}.{attr}"

        if not cmds.objExists(plug):
            continue

        try:
            if not cmds.getAttr(plug, lock=True):
                return True
        except Exception:
            pass

    return False


def cambiar_tool_por_control_seleccionado(*args):
    seleccion = cmds.ls(selection=True, transforms=True) or []

    if not seleccion:
        return

    control = seleccion[0]
    puede_mover = _atributo_control_activo(control, ["tx", "ty", "tz"])
    puede_rotar = _atributo_control_activo(control, ["rx", "ry", "rz"])

    if puede_mover and not puede_rotar:
        cmds.setToolTo("moveSuperContext")
    elif puede_rotar and not puede_mover:
        cmds.setToolTo("RotateSuperContext")


def activar_auto_tool_controles():
    global AUTO_TOOL_SCRIPTJOB

    if AUTO_TOOL_SCRIPTJOB and cmds.scriptJob(exists=AUTO_TOOL_SCRIPTJOB):
        cmds.scriptJob(kill=AUTO_TOOL_SCRIPTJOB, force=True)

    AUTO_TOOL_SCRIPTJOB = cmds.scriptJob(
        event=["SelectionChanged", cambiar_tool_por_control_seleccionado],
        protected=True
    )

    cambiar_tool_por_control_seleccionado()


def seleccionar_fk_por_defecto():
    if cmds.control("radio_fk", exists=True):
        cmds.radioButton("radio_fk", edit=True, select=True)

# =========================
# MOSTRAR MENSAJE CUANDO ARTICULA
# =========================
def mostrar_mensaje_conejito(morfologia, ancho_cabeza, emocion, dato_curioso):
    imagenes = {
        "descanso": ("descanso.png", 300, 260),
        "feo": ("feo.png", 300, 260),
        "pequeno": ("pequeño.png", 300, 260),
        "fantasia": ("fantasia.png", 300, 260),
        "odio": ("odio.png", 300, 260),
        "infiel": ("infiel.png", 300, 260),
        "artificial": ("artificial.png", 300, 260),
        "verdad": ("verdad.png", 300, 260),
    }

    nombre_imagen, ancho_imagen, alto_imagen = imagenes.get(
        emocion,
        ("descanso.png", 300, 260)
    )

    ruta_imagen = os.path.join(ruta_base, "iconosConejo", nombre_imagen)
    nombre_ventana = "mensajeDulceFortuna"

    if cmds.window(nombre_ventana, exists=True):
        cmds.deleteUI(nombre_ventana)

    ventana = cmds.window(
        nombre_ventana,
        title="Mi Dulce Fortuna",
        widthHeight=(520, 520),
        sizeable=False,
        bgc=fondorosado
    )

    cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=8,
        columnOffset=("both", 18),
        bgc=fondorosado
    )

    cmds.separator(h=10, style="none")

    cmds.text(
        label="¡Haz creado una Dulce Fortuna!",
        height=28,
        font="boldLabelFont",
        align="center",
        bgc=fondorosado
    )

    contenedor_imagen = cmds.formLayout(
        width=480,
        height=alto_imagen,
        bgc=fondorosado
    )

    imagen_ui = cmds.image(
        image=ruta_imagen,
        width=ancho_imagen,
        height=alto_imagen
    )

    cmds.formLayout(
        contenedor_imagen,
        edit=True,
        attachForm=[
            (imagen_ui, "top", 0),
        ],
        attachPosition=[
            (imagen_ui, "left", 0, 0),
        ],
        attachNone=[
            (imagen_ui, "right"),
            (imagen_ui, "bottom"),
        ]
    )

    cmds.setParent("..")

    cmds.text(
        label=f"Morfología: {morfologia} ({ancho_cabeza} cm)",
        align="center",
        bgc=fondorosado
    )

    cmds.text(
        label=f"Emoción: {emocion}",
        align="center",
        bgc=fondorosado
    )

    cmds.separator(h=6, style="none")


    cmds.button(
        label="¡ Mover Conejito !",
        height=30,
        bgc=lila,
        command=lambda *args: cerrar_mensaje_y_abrir_poses(nombre_ventana)
    )

    cmds.separator(h=10, style="none")

    cmds.showWindow(ventana)


def cerrar_mensaje_y_abrir_poses(nombre_ventana):
    if cmds.window(nombre_ventana, exists=True):
        cmds.deleteUI(nombre_ventana)

    posesui.abrir_ui()


#region 3.1 F.Generar conejo 




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

    posesui.cambiar_fkik(0)
    seleccionar_fk_por_defecto()

    funcionesIniciales.crear_jerarquia_controles_fk_anatomica()
    funcionesIniciales.crear_jerarquia_controles_ik_anatomica()

    funcionesIniciales.controles_en_ctrl_grp()

    activar_auto_tool_controles()

    

    crearConejo.ajustar_base_a_pies()

    ubicar_camara()
    # =========================
    # Mensaje Popup
    # =========================

    ancho_cabeza = crearConejo.ancho_cabeza

    if 20 <= ancho_cabeza <= 27:
        morfologia = "Vertical"

    elif 28 <= ancho_cabeza <= 35:
        morfologia = "Estandar"

    elif 36 <= ancho_cabeza <= 43:
        morfologia = "Horizontal"

    emocion = cmds.radioCollection("emociones", q=True, select=True)
    dato_curioso = pintarConejo.generar_dato_curioso(emocion)

    mostrar_mensaje_conejito(morfologia, ancho_cabeza, emocion, dato_curioso)

# endregion




#region 3.2 F.Ubicar camara
# =========================
# FUNCIÓN UBICAR CÁMARA
# =========================
def ubicar_camara():
    objetos = [
        obj for obj in crearConejo.piezas_deformables
        if cmds.objExists(obj)
    ]

    if not objetos:
        objetos = [
            obj for obj in [
                "Cabeza_Primitiva_001",
                "Tronco_Primitiva_010",
                "ManoIzquierda_Primitiva_011",
                "ManoDerecha_Primitiva_012",
                "PieIzquierdo_Primitiva_008",
                "PieDerecho_Primitiva_009",
                "Oreja_Izquierda_006",
                "Oreja_Derecha_007",
                "Cola_Primitiva_013",
            ]
            if cmds.objExists(obj)
        ]

    if not objetos:
        cmds.warning("No hay conejo para encuadrar la camara")
        return

    bbox = cmds.exactWorldBoundingBox(objetos)

    centro_x = (bbox[0] + bbox[3]) / 2
    centro_y = (bbox[1] + bbox[4]) / 2
    centro_z = (bbox[2] + bbox[5]) / 2

    ancho = bbox[3] - bbox[0]
    alto = bbox[4] - bbox[1]
    profundidad = bbox[5] - bbox[2]

    tamano = max(ancho, alto, profundidad)

    # Ligeramente rotada: no frontal, no 3/4 marcado.
    cmds.setAttr("persp.rotateX", -8)
    cmds.setAttr("persp.rotateY", 18)
    cmds.setAttr("persp.rotateZ", 0)

    # Distancia suave: encuadra todo y se aleja unas pocas unidades.
    morfologia = getattr(crearConejo, "morfologia", "estandar")

    if morfologia == "vertical":
        distancia = tamano * 2.5 + 6
        altura_offset = alto * 0.32
    elif morfologia == "horizontal":
        distancia = tamano * 2.0 + 3
        altura_offset = alto * 0.24
    else:
        distancia = tamano * 2.3 + 5
        altura_offset = alto * 0.28

    cmds.setAttr("persp.translateX", centro_x + distancia * 0.32)
    cmds.setAttr("persp.translateY", centro_y + altura_offset)
    cmds.setAttr("persp.translateZ", centro_z + distancia)
    # Ajustes de lente para evitar cortes.
    try:
        cmds.setAttr("perspShape.focalLength", 35)
        cmds.setAttr("perspShape.nearClipPlane", 0.1)
        cmds.setAttr("perspShape.farClipPlane", 10000)
    except:
        pass
# endregion


#region 3.3 F.Ocultar o mostrar malla

# =========================
# FUNCIÓN MOSTRAR / OCULTAR MALLA
# =========================
def ocultar_o_mostrar_malla(estado):

    paneles = cmds.getPanel(type="modelPanel")

    for panel in paneles:

        cmds.modelEditor(
            panel,
            edit=True,
            displayTextures=True,
            displayAppearance="smoothShaded",
            selectionHiliteDisplay=False,
            wireframeOnShaded=False,
            grid=False,
            joints=False,
            ikHandles=False,
            locators=True,
            deformers=False,
            handles=False
        )

    cmds.refresh(force=True)
# endregion


#region 3.4 F.Conejo Cuadrado

# =========================
# funcion_de_main_crear_conejo_cuadrado
# =========================
def funcion_de_main_crear_conejo_cuadrado(*args):

   
    borrar_escena()
    seleccion = cmds.radioCollection("emociones",q=True, select=True )
    crearConejo.crear_conejo(seleccion)
    ubicar_camara()

    global ancho 
    ancho= crearConejo.m * 10
    ocultar_o_mostrar_malla("mostrar")
# endregion

#region 3.5 F.Pintar conejo

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

    pintarConejo.pintar_cara_por_emocion(seleccion)
    pintarConejo.aplicar_outline_conejo()

    props.importar_corazones_decorativos(
        crearConejo.piezas_deformables,
        seleccion
    )

    props.importar_prop_aleatorio_personaje()

    cmds.refresh(force=True)

    print("✅ Conejo pintado correctamente")
    ocultar_o_mostrar_malla("mostrar")

# endregion

#region 3.6 F.Suavizar geometria

# =========================
# funcion Suavizar geometria
# =========================

def suavizar_geometria_de_conejo(*args):

    crearConejo.suavizar_conejo()
    crearConejo.deformar_cara_con_plano(crearConejo.cara)
    pintarConejo.aplicar_outline_conejo()

    # =========================
    # OCULTAR LÍNEAS DEL SMOOTH
    # =========================

    for obj in crearConejo.piezas_deformables:

        if cmds.objExists(obj):

            # mantener smooth preview
            cmds.setAttr(obj + ".displaySmoothMesh", 2)

            # ocultar líneas blancas
            cmds.setAttr(obj + ".smoothDrawType", 0)

    ocultar_o_mostrar_malla("ocultar")

    cmds.refresh(force=True)

# endregion


#region 3.7 F.def cambiar_fk_ik:
# =========================
# funcion cambiar_fk_ik
# =========================
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

# endregion


#region 3.8 F.Borrar
# =========================
# FUNCIÓN BOTÓN BORRAR
# =========================
def borrar_escena(*args):
    global AUTO_TOOL_SCRIPTJOB

    if AUTO_TOOL_SCRIPTJOB and cmds.scriptJob(exists=AUTO_TOOL_SCRIPTJOB):
        cmds.scriptJob(kill=AUTO_TOOL_SCRIPTJOB, force=True)
        AUTO_TOOL_SCRIPTJOB = None

    objetos = cmds.ls(assemblies=True)

    protegidos = ["persp", "top", "front", "side"]

    for obj in objetos:

        if obj not in protegidos and cmds.objExists(obj):
            cmds.delete(obj)

    # limpiar variables globales
    crearConejo.piezas_deformables = []
    crearConejo.cara = []

    global IK_CTRL_COLUMNA
    IK_CTRL_COLUMNA = None


    nodos_render = [
        "file",
        "place2dTexture",
        "ramp",
        "noise",
        "bump2d",
        "bump3d",
        "aiImage",
        "aiSkyDomeLight",
        "aiStandardSurface",
    ]

    if cmds.window("posesConejitoUI", exists=True):
        cmds.deleteUI("posesConejitoUI")


    print("🧹 Escena limpiada")
# endregion


#region 3.9 F.Conejo sorpresa

# =========================
# FUNCIÓN Boton CONEJO SORPRESA
# =========================
def conejo_sorpresa(*args):

    
    borrar_escena()

    emociones = [
        "descanso",
        "feo",
        "pequeno",
        "fantasia",
        "odio",
        "infiel",
        "artificial",
        "verdad"
    ]

    emocion_random = random.choice(emociones)

    cmds.radioButton(
        emocion_random,
        edit=True,
        select=True
    )

    crearConejo.crear_conejo(emocion_random)

    funcion_de_main_pintar_conejo()

    suavizar_geometria_de_conejo()

    generar_conejo_ui()
    ubicar_camara()

    #cmds.viewFit("persp")

  

# endregion






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
    ruta_imagen = os.path.join(ruta_base, "ImagenMenu.png")
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
    cmds.text(label="Da clic en conejo sorpresa \nó Selecciona una emoción y sigue los botones en orden", bgc=fondorosado,font="boldLabelFont")


        # =========================
        # 🔘 BOTÓN CONEJO SORPRESA
        # =========================

    cmds.separator(h=10, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,85), (2,120),(3,60)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo

    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.iconTextButton(style='iconOnly', image1=ruta_base + "/iconosConejo/regalo.png", width=24, height=28)
    cmds.button(label="Conejo Sorpresa", command=conejo_sorpresa,bgc=lila,height=28)
    cmds.setParent('..')

    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este
    

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
    cmds.image(image=ruta_base + "/iconosConejo/c1.png",width=10,height=10)

    cmds.radioButton(  "feo", label="Feo", align="center"  )
    cmds.image(image=ruta_base + "/iconosConejo/c5.png",width=10,height=10)

    cmds.radioButton( "pequeno", label="Pequeño", align="center" )
    cmds.image(image=ruta_base + "/iconosConejo/c2.png",width=10,height=10)

    cmds.radioButton( "fantasia", label="Fantasía", align="center")
    cmds.image(image=ruta_base + "/iconosConejo/c6.png",width=10,height=10)

    cmds.radioButton( "odio",label="Odio",align="center" )
    cmds.image(image=ruta_base + "/iconosConejo/c3.png",width=10,height=10)

    cmds.radioButton("infiel",label="Infiel",align="center" )
    cmds.image(image=ruta_base + "/iconosConejo/c7.png",width=10,height=10)

    cmds.radioButton("artificial",label="Artificial",align="center" )
    cmds.image(image=ruta_base + "/iconosConejo/c4.png",width=10,height=10)

    cmds.radioButton("verdad",label="Verdad",align="center"  )
    cmds.image(image=ruta_base + "/iconosConejo/c8.png",width=10,height=10)

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

    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.iconTextButton(style='iconOnly', image1=ruta_base + "/iconosConejo/crear.png", width=24, height=24)
    cmds.button(label="Crear", command=funcion_de_main_crear_conejo_cuadrado,bgc=gris,height=28)
    cmds.setParent('..')

    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este

        # =========================
        # 🔘 BOTÓN PINTAR CONEJO
        # =========================

    cmds.separator(h=8, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,85), (2,120),(3,60)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo
    
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.iconTextButton(style='iconOnly', image1=ruta_base + "/iconosConejo/colorear.png", width=24, height=24)
    cmds.button(label="Pintar", command=funcion_de_main_pintar_conejo,bgc=gris,height=28)
    cmds.setParent('..')

    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout para que el siguiente elemento no quede dentro de este

    
        # =========================
        # 🔘 BOTÓN Redondear (suavizar forma)
        # =========================
        
    cmds.separator(h=8, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,85), (2,120),(3,60)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo

    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.iconTextButton(style='iconOnly', image1=ruta_base + "/iconosConejo/redondear.png", width=24, height=24)
    cmds.button(label="Redondear", command=suavizar_geometria_de_conejo,bgc=gris,height=28)
    cmds.setParent('..')

    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui


    
        # =========================
        # FK / IK RADIO BUTTONS
        # =========================

    cmds.separator(h=10, style="none")

    # CONTENEDOR CENTRADO
    cmds.rowColumnLayout(
        numberOfColumns=3,
        columnWidth=[(1,40), (2,220), (3,40)]
    )

    # espacio izquierdo
    cmds.text(label="")

    # columna central
    cmds.columnLayout(adjustableColumn=True)

    cmds.radioCollection("fkik_collection")

    cmds.radioButton(
        "radio_fk",
        label="Quiero rotar hueso por hueso (FK)",
        select=True,
        enable=True,
        onc=cambiar_fk_ik
    )

    cmds.separator(h=3, style="none")

    cmds.radioButton(
        "radio_ik",
        label="Quiero rotar hueso con vecinos (IK)",
        enable=True,
        onc=cambiar_fk_ik
    )

    cmds.setParent('..')  # cerrar columnLayout

    # espacio derecho
    cmds.text(label="")

    cmds.setParent('..')  # cerrar rowColumnLayout


        # =========================
        # 🔘 BOTÓN crear_sistema fk to ik 
        # =========================
        
    cmds.separator(h=8, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,65), (2,160),(3,50)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo

    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.iconTextButton(style='iconOnly', image1=ruta_base + "/iconosConejo/esqueleto.png", width=24, height=28)
    cmds.button(label="Articular mi conejito", command=generar_conejo_ui,bgc=lila,height=28)
    cmds.setParent('..')

    cmds.text(label="", bgc=fondorosado) # espacio derecho
    cmds.setParent('..') #cierro el rowlayout del boton generar_conejo_ui

    # =========================
    # BOTON TOMAR FOTO
    # =========================

    cmds.separator(h=8, style="none")
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,85), (2,120), (3,60)])
    cmds.text(label="", bgc=fondorosado)

    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.iconTextButton(style='iconOnly', image1=ruta_base + "/iconosConejo/crear.png", width=24, height=24)
    cmds.button(label="Tomar foto", command=tomarfoto.tomar_foto, bgc=gris, height=28)
    cmds.setParent('..')

    cmds.text(label="", bgc=fondorosado)
    cmds.setParent('..')

        # =========================
        # 🔘 BOTÓN Borrar escena 
        # =========================
    cmds.separator(h=5, style="none")
    cmds.rowColumnLayout(numberOfColumns=3,columnWidth= [(1,205), (2,80),(3,20)]) # izquierda, botón, derecha
    cmds.text(label="", bgc=fondorosado) # espacio izquierdo

    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.iconTextButton(style='iconOnly', image1=ruta_base + "/iconosConejo/borrar.png", width=28, height=28)
    cmds.button(label="Borrar", command=borrar_escena,bgc=gris,height=28)
    cmds.setParent('..')

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
    cmds.columnLayout(adjustableColumn=True)

    cmds.text(
        label="Mayerly Camargo Pedraza - Código 1202327",
        align="center",
        bgc=fondorosado,
        font="smallPlainLabelFont"
    )

    cmds.text(
        label="Jenifer Lizethe Leiva Martín - Código 1202617",
        align="center",
        bgc=fondorosado,
        font="smallPlainLabelFont"
    )

    cmds.text(
        label="Docente: Diego Beltrán Cardona - UMNG 2026",
        align="center",
        bgc=fondorosado,
        font="smallPlainLabelFont"
    )

    cmds.setParent('..')
    cmds.separator(h=20, style="none") #espacio vacio
    cmds.setParent('..')  # ← cerrar columnLayout derecha


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
