
import importlib
import os
import maya.cmds as cmds
import proyectofinal02.crearConejo as crearConejo
import proyectofinal02.funcionesFK as funcionesFK
import proyectofinal02.funcionesIniciales as funcionesIniciales
import proyectofinal02.paletas as paletas
import proyectofinal02.pintarConejo as pintarConejo

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
    
    seleccion = cmds.radioCollection("emociones", q=True, select=True)
    estilo = cmds.radioCollection("estilos",q=True,select=True)
    crearConejo.crear_conejo(seleccion)
    pintarConejo.aplicar_estilo(seleccion,estilo)
    ancho = crearConejo.m * 10
    cmds.text(
        "textoModulo",
        edit=True,
        label=f"Ancho cabeza: {ancho:.1f} cm | Morfología: {crearConejo.morfologia}"
    )
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
morado = (204/255, 79/255, 252/255)   # #cc4ffc
lila = (204/255, 153/255, 255/255)   # CC99FF
gris = (116/255, 116/255, 116/255)    # #747474
blanco = (1,1,1)
# =========================
# FUNCIÓN BOTÓN BORRAR
# =========================
def borrar_escena(*args):
    cmds.select(all=True)
    cmds.delete()

# =========================
# CREACIÓN UI
# =========================
def crear_ui():
    
    if cmds.window("miVentanaConejo", exists=True):
        cmds.deleteUI("miVentanaConejo")
    ventana = cmds.window("miVentanaConejo", title="MI DULCE FORTUNA", widthHeight=(600, 400))

    # =========================
    # LAYOUT PRINCIPAL (2 COLUMNAS)
    # =========================
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)

    # =========================
    # COLUMNA IZQUIERDA (IMAGEN)
    # =========================

    ruta_actual = os.getcwd()

    ruta_imagen = os.path.join(
        ruta_actual,
        "ImagenMenu.png"
    )

    ruta_imagen = ruta_imagen.replace("\\", "/")



    cmds.columnLayout(width=300)

    cmds.image(image=ruta_imagen)

    cmds.setParent('..')

    # =========================
    # COLUMNA DERECHA (MENÚ)
    # =========================
    cmds.columnLayout(adjustableColumn=True, bgc=fondorosado)

    cmds.separator(h=20, style="none")

    cmds.text(label="MI DULCE FORTUNA", height=35,  bgc=fondorosado,font="boldLabelFont",align="center")
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

    cmds.radioButton(
        "descanso",
        label="Descanso 🌿",
        select=True
    )

    cmds.radioButton(
        "fantasia",
        label="Fantasía ✨"
    )

    cmds.radioButton(
        "odio",
        label="Odio 😠"
    )

    cmds.radioButton(
        "barato",
        label="Barato 🛒"
    )

    cmds.radioButton(
        "envidia",
        label="Envidia 🟩"
    )

    cmds.radioButton(
        "infidelidad",
        label="Infidelidad 🖤"
    )

    cmds.radioButton(
        "cortesia",
        label="Cortesía 🌸"
    )

    cmds.radioButton(
        "feo",
        label="Feo 🪨"
    )

    cmds.setParent('..')  # cerrar columnLayout
    cmds.setParent('..')  # cerrar rowLayout

    cmds.separator(h=15, style="none")

    cmds.separator(h=15, style="none")

    cmds.text(
        label="Selecciona un estilo gráfico",
        bgc=fondorosado
    )

    cmds.separator(h=10, style="none")

    cmds.radioCollection("estilos")

    cmds.radioButton(
        "pixelart",
        label="Pixel Art 🟪",
        select=True
    )

    cmds.radioButton(
        "bento",
        label="Bento Art 🟦"
    )

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

    #texto para mostrar el ancho de cabeza generado y como varia 
    cmds.text(
        "textoModulo",
        label="Ancho de cabeza: --- cm",
        bgc=fondorosado,
        align="center"
    )

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
