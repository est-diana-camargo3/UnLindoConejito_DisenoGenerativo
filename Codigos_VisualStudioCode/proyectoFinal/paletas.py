# ╔═══════════════════════════════════════════════════════════════╗
# ║                     PALETAS EMOCIONALES                      ║
# ║          Inspiradas en "La Psicología del Color"             ║
# ║                         Eva Heller                            ║
# ╚═══════════════════════════════════════════════════════════════╝


# =========================
# HEX → RGB NORMALIZADO
# =========================

def hex_a_rgb(hex_color):

    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0

    return (r, g, b)


# =========================
# PALETAS
# =========================

PALETAS = {

    # =========================================================
    # DESCANSO
    # =========================================================
    "descanso": [

        (hex_a_rgb("#00334d"), 35),   # azul
        (hex_a_rgb("#beff7e"), 35),   # verde
        (hex_a_rgb("#FFFFFF"), 15),   # blanco
        (hex_a_rgb("#f3ff88"), 15)    # amarillo claro
    ],

    # =========================================================
    # FEO
    # =========================================================
    "feo": [

        (hex_a_rgb("#463a28"), 32),   # café
        (hex_a_rgb("#ccb3b3"), 32),   # gris
        (hex_a_rgb("#1a1a1a"), 26),   # negro
        (hex_a_rgb("#8080ff"), 10)    # azul oscuro
    ],

    # =========================================================
    # PEQUEÑO
    # =========================================================
    "pequeno": [

        (hex_a_rgb("#ff80cc"), 40),   # rosado
        (hex_a_rgb("#ffcc4d"), 35),   # amarillo
        (hex_a_rgb("#FFFFFF"), 15),   # blanco
        (hex_a_rgb("#8080ff"), 10)    # gris
    ],

    # =========================================================
    # FANTASIA
    # =========================================================
    "fantasia": [

        (hex_a_rgb("#001aff"), 29),   # azul brillante
        (hex_a_rgb("#00001a"), 29),   # azul oscuro
        (hex_a_rgb("#e6cc80"), 29),   # naranja
        (hex_a_rgb("#00ffff"), 13)    # verde
    ],

    # =========================================================
    # ODIO
    # =========================================================
    "odio": [

        (hex_a_rgb("#ff3333"), 30),   # rosa
        (hex_a_rgb("#660000"), 30),   # rojo
        (hex_a_rgb("#000000"), 30),   # negro
        (hex_a_rgb("#ffb380"), 10)    # amarillo
    ],

    # =========================================================
    # INFIEL
    # =========================================================
    "infiel": [

        (hex_a_rgb("#ffbe3d"), 55),   # amarillo
        (hex_a_rgb("#6eff4a"), 25),   # verde
        (hex_a_rgb("#e6cc99"), 10),   # gris verdoso
        (hex_a_rgb("#FF5C5C"), 10)    # negro
    ],

    # =========================================================
    # ARTIFICIAL
    # =========================================================
    "artificial": [

        (hex_a_rgb("#331a80"), 22),   # morado
        (hex_a_rgb("#666666"), 22),   # gris
        (hex_a_rgb("#ff80ff"), 20),   # rosado
        (hex_a_rgb("#e6ff33"), 18),   # dorado
        (hex_a_rgb("#ff4d1a"), 18)    # naranja
    ],

    # =========================================================
    # VERDAD
    # =========================================================
    "verdad": [

        (hex_a_rgb("#FFFFFF"), 40),   # blanco
        (hex_a_rgb("#000033"),20),   # azul
        (hex_a_rgb("#334dff"), 20),   # gris azulado
        (hex_a_rgb("#ff9933"), 20)    # dorado frío
    ],

}