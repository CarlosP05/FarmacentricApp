import customtkinter as ctk
from logica.logica_alertas import obtener_dashboard_alertas
from logica.logica_finanzas import generar_reporte_financiero
from vistas.vista_usuarios import VistaUsuarios
from vistas.vista_inventario import VistaInventario
from config_tema import COLORS, FONTS, RADIUS, CARD_STYLE, BTN_GHOST, BTN_LOGOUT


class DashboardAdmin(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Farmacentric — Panel de Administrador")
        self.geometry("1000x640")
        self.minsize(860, 560)
        self.configure(fg_color=COLORS["app_bg"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)  # Área principal se expande

        self.crear_sidebar()
        self.crear_area_principal()
        self.cargar_datos_dashboard()

    # ── SIDEBAR ───────────────────────────────────────────────────────────────
    def crear_sidebar(self):
        """Menú lateral izquierdo con identidad de marca."""
        self.sidebar = ctk.CTkFrame(
            self, width=230, corner_radius=0,
            fg_color=COLORS["sidebar_bg"]
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(8, weight=1)  # Empuja logout al fondo

        # ── Logo ──────────────────────────────────────────────────────────────
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(24, 8), sticky="ew")

        ctk.CTkLabel(
            logo_frame, text="✚  Farmacentric",
            font=FONTS["logo"], text_color=COLORS["sidebar_text"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo_frame, text="Panel de Administrador",
            font=FONTS["logo_sub"], text_color=COLORS["sidebar_subtext"]
        ).pack(anchor="w")

        # ── Separador ─────────────────────────────────────────────────────────
        ctk.CTkFrame(
            self.sidebar, height=1, fg_color=COLORS["primary"]
        ).grid(row=1, column=0, sticky="ew", padx=16, pady=4)

        # ── Label de sección ──────────────────────────────────────────────────
        ctk.CTkLabel(
            self.sidebar, text="   MENÚ PRINCIPAL",
            font=("Segoe UI", 10),
            text_color=COLORS["sidebar_subtext"],
            anchor="w"
        ).grid(row=2, column=0, sticky="ew", padx=16, pady=(12, 4))

        # ── Botón Activo: Dashboard ────────────────────────────────────────────
        self.btn_inicio = ctk.CTkButton(
            self.sidebar, text="  ⊞   Dashboard",
            width=198, height=40, anchor="w",
            corner_radius=RADIUS["btn"],
            fg_color=COLORS["primary_light"],
            hover_color=COLORS["primary_hover"],
            text_color="#FFFFFF",
            font=FONTS["sidebar_item"],
        )
        self.btn_inicio.grid(row=3, column=0, padx=16, pady=3)

        # ── Botones Ghost: Navegación ──────────────────────────────────────────
        self.btn_usuarios = ctk.CTkButton(
            self.sidebar, text="  👥   Usuarios",
            width=198, **BTN_GHOST,
            command=self.abrir_gestion_usuarios
        )
        self.btn_usuarios.grid(row=4, column=0, padx=16, pady=3)

        self.btn_inventario = ctk.CTkButton(
            self.sidebar, text="  📦   Inventario",
            width=198, **BTN_GHOST,
            command=self.abrir_gestion_inventario
        )
        self.btn_inventario.grid(row=5, column=0, padx=16, pady=3)

        # ── Separador inferior ────────────────────────────────────────────────
        ctk.CTkFrame(
            self.sidebar, height=1, fg_color=COLORS["primary"]
        ).grid(row=7, column=0, sticky="ew", padx=16, pady=8)

        # ── Cerrar Sesión ─────────────────────────────────────────────────────
        self.btn_salir = ctk.CTkButton(
            self.sidebar, text="  ⏻   Cerrar Sesión",
            width=198, **BTN_LOGOUT,
            command=lambda: self.master.cerrar_sesion(self)
        )
        self.btn_salir.grid(row=9, column=0, padx=16, pady=(0, 24), sticky="s")

    def abrir_gestion_usuarios(self):
        VistaUsuarios(self)

    def abrir_gestion_inventario(self):
        VistaInventario(self)

    # ── ÁREA PRINCIPAL ────────────────────────────────────────────────────────
    def crear_area_principal(self):
        """Área central con KPIs y alertas de inventario."""
        self.main_frame = ctk.CTkFrame(self, fg_color=COLORS["app_bg"])
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=24, pady=24)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)

        # ── Encabezado ────────────────────────────────────────────────────────
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))

        ctk.CTkLabel(
            header, text="Resumen General",
            font=FONTS["h1"], text_color=COLORS["text_primary"]
        ).pack(side="left")

        ctk.CTkLabel(
            header, text="Vista del Administrador",
            font=FONTS["body_small"], text_color=COLORS["text_secondary"]
        ).pack(side="left", padx=12, pady=6)

        # ── Tarjeta KPI 1: Balance Neto ───────────────────────────────────────
        self.tarjeta_balance = self._crear_tarjeta_kpi(
            self.main_frame,
            titulo="Balance Neto del Período",
            valor="Calculando...",
            icono="💵",
            color_acento=COLORS["success"]
        )
        self.tarjeta_balance.grid(row=1, column=0, padx=(0, 10), sticky="new")

        # ── Tarjeta KPI 2: Estado Financiero ──────────────────────────────────
        self.tarjeta_estado = self._crear_tarjeta_kpi(
            self.main_frame,
            titulo="Estado Financiero",
            valor="...",
            icono="📊",
            color_acento=COLORS["primary_light"]
        )
        self.tarjeta_estado.grid(row=1, column=1, padx=(10, 0), sticky="new")

        # ── Panel de Alertas de Inventario ────────────────────────────────────
        self.frame_alertas = ctk.CTkFrame(
            self.main_frame, **CARD_STYLE
        )
        self.frame_alertas.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(18, 0))
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Header del panel de alertas
        alertas_header = ctk.CTkFrame(
            self.frame_alertas, fg_color=COLORS["primary"],
            corner_radius=0, height=50
        )
        alertas_header.pack(fill="x")
        alertas_header.pack_propagate(False)

        ctk.CTkLabel(
            alertas_header, text="⚠️   Alertas Críticas de Inventario",
            font=FONTS["h2"], text_color="#FFFFFF"
        ).pack(side="left", padx=16)

        # Área scrollable para alertas
        self.scroll_alertas = ctk.CTkScrollableFrame(
            self.frame_alertas,
            fg_color=COLORS["app_bg"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary_light"],
            corner_radius=0
        )
        self.scroll_alertas.pack(fill="both", expand=True, padx=12, pady=12)

    def _crear_tarjeta_kpi(self, parent, titulo, valor, icono, color_acento):
        """Componente reutilizable de tarjeta KPI con franja lateral de color."""
        tarjeta = ctk.CTkFrame(parent, **CARD_STYLE)

        # Franja de color lateral
        ctk.CTkFrame(
            tarjeta, width=5, corner_radius=3,
            fg_color=color_acento
        ).pack(side="left", fill="y", padx=(8, 0), pady=12)

        contenido = ctk.CTkFrame(tarjeta, fg_color="transparent")
        contenido.pack(side="left", fill="both", expand=True, padx=14, pady=14)

        # Ícono + Título
        fila_top = ctk.CTkFrame(contenido, fg_color="transparent")
        fila_top.pack(fill="x")

        ctk.CTkLabel(
            fila_top, text=icono,
            font=("Segoe UI", 20), text_color=color_acento
        ).pack(side="left")

        ctk.CTkLabel(
            fila_top, text=titulo,
            font=FONTS["h3"], text_color=COLORS["text_secondary"]
        ).pack(side="left", padx=8)

        # Valor grande
        lbl_valor = ctk.CTkLabel(
            contenido, text=valor,
            font=FONTS["kpi"], text_color=COLORS["text_primary"]
        )
        lbl_valor.pack(anchor="w", pady=(6, 0))

        # Guardamos referencia al label para actualizarlo luego
        tarjeta._lbl_valor = lbl_valor

        return tarjeta

    def _agregar_alerta_item(self, texto, color, icono):
        """Agrega un ítem de alerta individual al scroll de alertas."""
        item = ctk.CTkFrame(
            self.scroll_alertas,
            corner_radius=8,
            fg_color=COLORS["card_bg"],
            border_width=1,
            border_color=COLORS["border"]
        )
        item.pack(fill="x", pady=4, padx=4)

        # Barra de color izquierda
        ctk.CTkFrame(item, width=4, corner_radius=2, fg_color=color).pack(
            side="left", fill="y", padx=(6, 0), pady=8
        )

        ctk.CTkLabel(
            item, text=f"{icono}  {texto}",
            font=FONTS["body"], text_color=COLORS["text_primary"],
            anchor="w"
        ).pack(side="left", padx=12, pady=10)

    # ── DATOS ──────────────────────────────────────────────────────────────────
    def cargar_datos_dashboard(self):
        """Conecta la interfaz con la lógica del sistema."""
        # 1. Finanzas
        finanzas = generar_reporte_financiero()

        self.tarjeta_balance._lbl_valor.configure(
            text=f"C$ {finanzas['balance_neto']:,.2f}"
        )
        self.tarjeta_estado._lbl_valor.configure(
            text=finanzas["estado_financiero"]
        )

        # 2. Alertas — limpiar y recargar
        for widget in self.scroll_alertas.winfo_children():
            widget.destroy()

        alertas = obtener_dashboard_alertas()
        tiene_alertas = False

        if alertas["alertas_stock"]:
            tiene_alertas = True
            for a in alertas["alertas_stock"]:
                self._agregar_alerta_item(
                    texto=f"{a['producto']}  —  Quedan {a['stock_actual']} uds. (Mínimo: {a['stock_minimo']})",
                    color=COLORS["danger"],
                    icono="📉"
                )

        if alertas["alertas_vencimiento"]:
            tiene_alertas = True
            for a in alertas["alertas_vencimiento"]:
                self._agregar_alerta_item(
                    texto=f"{a['producto']}  (Lote: {a['lote']})  —  {a['estado']}",
                    color=COLORS["warning"],
                    icono="📅"
                )

        if not tiene_alertas:
            self._agregar_alerta_item(
                texto="Todo en orden. No hay alertas críticas en el inventario.",
                color=COLORS["success"],
                icono="✅"
            )