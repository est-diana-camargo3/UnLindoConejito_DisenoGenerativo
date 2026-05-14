#prueba de cambio 
#ESTE ES EL CODIGO HASTA EL MOMENTO 
#jenifer
import maya.cmds as cmds

import random

#Cambiar unidades a metros 
cmds.currentUnit(linear="meter") 

# =========================
# PRIMITIVAS
# =========================

PRIMITIVAS = ["Cubo","Esfera","Cilindro","Cono","Plano","Toro"]

def crear_primitiva_random(lista, nombre):
    tipo = random.choice(lista)

    if tipo == "Cubo":
        return cmds.polyCube(name=nombre)[0]
    elif tipo == "Esfera":
        return cmds.polySphere(name=nombre)[0]
    elif tipo == "Cilindro":
        return cmds.polyCylinder(name=nombre)[0]
    elif tipo == "Cono":
        return cmds.polyCone(name=nombre)[0]
    elif tipo == "Plano":
        return cmds.polyPlane(name=nombre)[0]
    elif tipo == "Toro":
        return cmds.polyTorus(name=nombre)[0]

# =========================
# PALETA DE COLOR
# =========================

def generar_paleta():
    base = [random.random(), random.random(), random.random()]

    paleta = []

    for i in range(5):
        variacion = [min(max(c + random.uniform(-0.2,0.2),0),1) for c in base]
        paleta.append(variacion)

    return paleta

def crear_material_color(color):
    mat = cmds.shadingNode('lambert', asShader=True)
    cmds.setAttr(mat + ".color", color[0], color[1], color[2], type="double3")

    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    cmds.connectAttr(mat + ".outColor", sg + ".surfaceShader", force=True)

    return sg

# =========================
# MORFOLOGIA
# =========================

def obtener_tipo():
    return random.choice(["alargado","robusto","alto","compacto","normal"])

# =========================
# PARTES
# =========================

def crear_cuerpo(prims, tipo):
    obj = crear_primitiva_random(prims, "cuerpo")

    if tipo == "alargado":
        cmds.scale(4,1,1,obj)
    elif tipo == "robusto":
        cmds.scale(2,2,2,obj)
    elif tipo == "alto":
        cmds.scale(1,3,1,obj)
    elif tipo == "compacto":
        cmds.scale(2.5,1,2.5,obj)
    else:
        cmds.scale(2,1.5,1.5,obj)

    return obj


def crear_cabeza(prims, cuerpo):
   
    obj = crear_primitiva_random(prims, "cabeza")

    # escala aleatoria
    escala = random.uniform(0.6, 1.2)
    cmds.scale(escala, escala, escala, obj)

    # bounding box del cuerpo
    bbox = cmds.exactWorldBoundingBox(cuerpo)

    minY = bbox[1]
    maxY = bbox[4]

    altura_cuerpo = maxY - minY

    # posición base: mitad del cuerpo hacia arriba
    y = minY + altura_cuerpo * random.uniform(0.5, 1.2)

    # ligera variación en Z (adelante)
    z = random.uniform(0.5, 1.5)

    # pequeña variación en X (lado a lado)
    x = random.uniform(-0.5, 0.5)

    cmds.move(x, y, z, obj)

    return obj
   

def crear_patas(prims, tipo):
    patas = []
    cantidad = 4 if tipo != "alargado" else random.randint(0,6)

    for i in range(cantidad):
        p = crear_primitiva_random(prims, f"pata_{i}")
        cmds.scale(0.3,1,0.3,p)
        cmds.move(random.uniform(-1,1),0.5,random.uniform(-1,1),p)
        patas.append(p)

    return patas

def crear_orejas(prims):
    orejas = []
    for i in range(2):
        o = crear_primitiva_random(prims, f"oreja_{i}")
        cmds.scale(0.3,1,0.3,o)
        x = -0.3 if i==0 else 0.3
        cmds.move(x,3,1,o)
        orejas.append(o)
    return orejas

def crear_cola(prims):
    c = crear_primitiva_random(prims,"cola")
    cmds.scale(0.2,1,0.2,c)
    cmds.move(0,1,-2,c)
    return c

# =========================
# CARA
# =========================

def crear_cara(cabeza):
    pos = cmds.xform(cabeza, q=True, ws=True, t=True)
    elementos = []    

    for i in range(2):
        ojo = cmds.polySphere()[0]
        cmds.scale(0.2,0.2,0.2,ojo)
        x = -0.3 if i==0 else 0.3
        cmds.move(pos[0]+x,pos[1]+0.2,pos[2]+0.8,ojo)

        # ojos negros
        mat = cmds.shadingNode('lambert', asShader=True)
        cmds.setAttr(mat+".color",0,0,0,type="double3")
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
        cmds.connectAttr(mat+".outColor", sg+".surfaceShader", force=True)
        cmds.sets(ojo, e=True, forceElement=sg)

        cmds.parent(ojo,cabeza)
        elementos.append(ojo)

    nariz = cmds.polySphere()[0]
    cmds.scale(0.15,0.15,0.15,nariz)
    cmds.move(pos[0],pos[1],pos[2]+1,nariz)
    cmds.parent(nariz,cabeza)

    boca = cmds.polyCube()[0]
    cmds.scale(0.4,0.05,0.05,boca)
    cmds.move(pos[0],pos[1]-0.3,pos[2]+0.9,boca)
    cmds.parent(boca,cabeza)

    elementos += [nariz,boca]
   
    return elementos

# =========================
# GENERADOR
# =========================

def generar_criatura(prims):

    if not prims:
        cmds.warning("Selecciona al menos una primitiva")
        return

    tipo = obtener_tipo()
    paleta = generar_paleta()

    grupo = cmds.group(empty=True)

    cuerpo = crear_cuerpo(prims, tipo)
    cabeza = crear_cabeza(prims, cuerpo)
    patas = crear_patas(prims, tipo)
    orejas = crear_orejas(prims)
    cola = crear_cola(prims)
    cara = crear_cara(cabeza)

    # materiales por parte
    mat_cuerpo = crear_material_color(paleta[0])
    mat_cabeza = crear_material_color(paleta[1])
    mat_patas = crear_material_color(paleta[2])
    mat_orejas = crear_material_color(paleta[3])
    mat_cola = crear_material_color(paleta[4])

    cmds.sets(cuerpo, e=True, forceElement=mat_cuerpo)
    cmds.sets(cabeza, e=True, forceElement=mat_cabeza)
    cmds.sets(cola, e=True, forceElement=mat_cola)

    for p in patas:
        cmds.sets(p, e=True, forceElement=mat_patas)

    for o in orejas:
        cmds.sets(o, e=True, forceElement=mat_orejas)

    for obj in [cuerpo,cabeza,cola]+patas+orejas+cara:
        cmds.parent(obj, grupo)

    return grupo

def generar_multiple(prims):

    crear_escena_render()

    for i in range(3):
        g = generar_criatura(prims)
        cmds.move(i*6, 0, random.uniform(-3,3), g)
       
# =========================
# ESCENA DE RENDER
# =========================

def crear_escena_render():
   
    # borrar luces viejas
    for l in cmds.ls(type="light"):
        try:
            cmds.delete(cmds.listRelatives(l, parent=True))
        except:
            pass

    grupo = cmds.group(empty=True, name="Escena_Render")

    # =========================
    # LUZ PRINCIPAL
    # =========================
    key = cmds.directionalLight(name="KeyLight")
    key_t = cmds.listRelatives(key, parent=True)[0]
    cmds.rotate(-45, 45, 0, key_t)
    cmds.setAttr(key + ".intensity", 1.5)

    # =========================
    # LUZ RELLENO
    # =========================
    fill = cmds.directionalLight(name="FillLight")
    fill_t = cmds.listRelatives(fill, parent=True)[0]
    cmds.rotate(-20, -45, 0, fill_t)
    cmds.setAttr(fill + ".intensity", 0.5)

    # =========================
    # LUZ CONTRA
    # =========================
    rim = cmds.directionalLight(name="RimLight")
    rim_t = cmds.listRelatives(rim, parent=True)[0]
    cmds.rotate(45, 180, 0, rim_t)
    cmds.setAttr(rim + ".intensity", 0.8)

    cmds.parent(key_t, fill_t, rim_t, grupo)

    # =========================
    # FONDO CICLORAMA (MEJOR)
    # =========================
    fondo = cmds.polyPlane(w=40, h=40, name="Fondo")[0]
    cmds.rotate(-90, 0, 0, fondo)
    cmds.move(0, -0.01, 0, fondo)

    # pared atrás
    pared = cmds.polyPlane(w=40, h=20, name="FondoBack")[0]
    cmds.move(0, 10, -20, pared)

    # material fondo
    mat = cmds.shadingNode('lambert', asShader=True, name="fondo_mat")
    cmds.setAttr(mat+".color", 0.6, 0.6, 0.6, type="double3")

    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    cmds.connectAttr(mat+".outColor", sg+".surfaceShader", force=True)

    cmds.sets(fondo, e=True, forceElement=sg)
    cmds.sets(pared, e=True, forceElement=sg)

    cmds.parent(fondo, pared, grupo)

    # =========================
    # SOMBRAS
    # =========================
    for luz in [key, fill, rim]:
        try:
            cmds.setAttr(luz + ".useRayTraceShadows", 1)
        except:
            pass

    # =========================
    # CÁMARA
    # =========================
    cam = cmds.camera(name="RenderCam")[0]
    cmds.move(0, 6, 18, cam)
    cmds.rotate(-15, 0, 0, cam)

    print("Escena render lista  ")
   
# =========================
# UI
# =========================

def obtener_seleccion():
    seleccion = []
    for p in PRIMITIVAS:
        if cmds.checkBox(p, q=True, v=True):
            seleccion.append(p)
    return seleccion

def crear_ui():
    if cmds.window("win", exists=True):
        cmds.deleteUI("win")

    cmds.window("win", title="Generador Criaturas FINAL")
    cmds.columnLayout()

    cmds.text(label="Selecciona primitivas:")

    for p in PRIMITIVAS:
        cmds.checkBox(p, label=p, v=True)

    cmds.button(label="Generar 1",
        command=lambda x: generar_criatura(obtener_seleccion()))

    cmds.button(label="Generar 3",
        command=lambda x: generar_multiple(obtener_seleccion()))

    cmds.showWindow()

crear_ui()
