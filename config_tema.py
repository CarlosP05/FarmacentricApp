# =============================================================
#   FARMACENTRIC — SISTEMA DE DISEÑO CENTRAL
#   Importa este archivo en TODAS las vistas para consistencia.
#   Uso: from config_tema import COLORS, FONTS, RADIUS, BTN_PRIMARY, ...
# =============================================================

# ── PALETA DE COLORES ─────────────────────────────────────────────────────────
COLORS = {
    # Primarios (Azul Médico Profundo)
    "primary":          "#1A3C5E",
    "primary_light":    "#2D6A9F",
    "primary_hover":    "#245A8A",

    # Sidebar
    "sidebar_bg":       "#0F2844",
    "sidebar_active":   "#1A3C5E",
    "sidebar_text":     "#FFFFFF",
    "sidebar_subtext":  "#94A3B8",

    # Fondos
    "app_bg":           "#F0F4F8",   # Fondo general de la ventana
    "card_bg":          "#FFFFFF",   # Fondo de tarjetas y paneles
    "panel_bg":         "#E8F0FE",   # Fondo de paneles secundarios (ticket, etc.)

    # Texto
    "text_primary":     "#1E293B",   # Texto principal
    "text_secondary":   "#64748B",   # Subtítulos, labels, placeholders

    # Semáforo de estados
    "success":          "#10B981",   # Verde esmeralda — Procesar Pago, éxito
    "success_hover":    "#059669",   # Verde más oscuro — hover de botones verdes
    "success_text":     "#16A34A",   # Verde texto — mensajes de confirmación
    "warning":          "#F59E0B",   # Ámbar — advertencias (próximos a vencer)
    "danger":           "#DC2626",   # Rojo médico — alertas críticas, cerrar sesión
    "danger_hover":     "#B91C1C",   # Rojo oscuro — hover en botones de peligro
    "danger_text":      "#B91C1C",   # Rojo texto — mensajes de error

    # Bordes y separadores
    "border":           "#CBD5E1",
}

# ── SISTEMA TIPOGRÁFICO ───────────────────────────────────────────────────────
# Segoe UI está preinstalada en Windows — no requiere instalación adicional.
# Para Inter (alternativa premium): https://fonts.google.com/specimen/Inter
FONTS = {
    "logo":         ("Segoe UI", 22, "bold"),    # Nombre del sistema en sidebar
    "logo_sub":     ("Segoe UI", 11),            # Subtítulo bajo el logo
    "h1":           ("Segoe UI", 22, "bold"),    # Título principal de ventana
    "h2":           ("Segoe UI", 16, "bold"),    # Título de sección/panel
    "h3":           ("Segoe UI", 14, "bold"),    # Subtítulo de componente
    "body":         ("Segoe UI", 13),            # Texto de cuerpo estándar
    "body_small":   ("Segoe UI", 11),            # Texto auxiliar/meta
    "btn":          ("Segoe UI", 13, "bold"),    # Botones estándar
    "btn_large":    ("Segoe UI", 15, "bold"),    # Botones CTA grandes
    "mono":         ("Consolas", 13),            # Texto monoespaciado (tickets, colillas)
    "kpi":          ("Segoe UI", 28, "bold"),    # Valores grandes de KPI
    "sidebar_item": ("Segoe UI", 13),            # Texto de botones del sidebar
}

# ── RADIOS DE BORDE ───────────────────────────────────────────────────────────
RADIUS = {
    "card":    12,    # Tarjetas de contenido
    "btn":      8,    # Botones estándar
    "btn_lg":  10,    # Botones CTA grandes
    "input":    8,    # Campos de entrada
    "sidebar":  0,    # Sidebar — siempre sin borde
    "chip":    20,    # Badges/etiquetas redondeadas
}

# ── DIMENSIONES ───────────────────────────────────────────────────────────────
SIZES = {
    "sidebar_width":   220,
    "btn_height":       38,
    "btn_lg_height":    50,
    "input_height":     40,
    "card_padding":     16,
}

# =============================================================
#   ESTILOS PREFABRICADOS PARA WIDGETS
#   Desempaqueta con **: ctk.CTkFrame(parent, **CARD_STYLE)
# =============================================================

CARD_STYLE = {
    "corner_radius": RADIUS["card"],
    "fg_color":      COLORS["card_bg"],
    "border_width":  1,
    "border_color":  COLORS["border"],
}

SIDEBAR_STYLE = {
    "corner_radius": RADIUS["sidebar"],
    "fg_color":      COLORS["sidebar_bg"],
    "width":         SIZES["sidebar_width"],
}

INPUT_STYLE = {
    "corner_radius":              RADIUS["input"],
    "border_width":               1,
    "border_color":               COLORS["border"],
    "fg_color":                   COLORS["card_bg"],
    "text_color":                 COLORS["text_primary"],
    "placeholder_text_color":     COLORS["text_secondary"],
    "font":                       FONTS["body"],
    "height":                     SIZES["input_height"],
}

BTN_PRIMARY = {
    "corner_radius":  RADIUS["btn"],
    "fg_color":       COLORS["primary_light"],
    "hover_color":    COLORS["primary_hover"],
    "text_color":     "#FFFFFF",
    "font":           FONTS["btn"],
    "height":         SIZES["btn_height"],
}

BTN_SUCCESS = {
    "corner_radius":  RADIUS["btn_lg"],
    "fg_color":       COLORS["success"],
    "hover_color":    COLORS["success_hover"],
    "text_color":     "#FFFFFF",
    "font":           FONTS["btn_large"],
    "height":         SIZES["btn_lg_height"],
}

BTN_DANGER = {
    "corner_radius":  RADIUS["btn"],
    "fg_color":       COLORS["danger"],
    "hover_color":    COLORS["danger_hover"],
    "text_color":     "#FFFFFF",
    "font":           FONTS["btn"],
    "height":         SIZES["btn_height"],
}

# Botón transparente con hover — ideal para sidebar
BTN_GHOST = {
    "corner_radius":  RADIUS["btn"],
    "fg_color":       "transparent",
    "hover_color":    COLORS["sidebar_active"],
    "text_color":     COLORS["sidebar_text"],
    "font":           FONTS["sidebar_item"],
    "height":         40,
    "anchor":         "w",
}

# Botón de cerrar sesión — transparente en reposo, rojo en hover
BTN_LOGOUT = {
    "corner_radius":  RADIUS["btn"],
    "fg_color":       "transparent",
    "hover_color":    COLORS["danger"],
    "text_color":     COLORS["sidebar_subtext"],
    "font":           FONTS["sidebar_item"],
    "height":         40,
    "anchor":         "w",
}
