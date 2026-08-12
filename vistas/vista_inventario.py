import customtkinter as ctk
from logica.logica_inventario import registrar_nuevo_producto, registrar_nuevo_lote
from config_tema import COLORS, FONTS, RADIUS, CARD_STYLE, INPUT_STYLE, BTN_PRIMARY, BTN_SUCCESS


class VistaInventario(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Farmacentric — Ingreso de Inventario")
        self.geometry("860x580")
        self.minsize(800, 520)
        self.configure(fg_color=COLORS["app_bg"])
        self.grab_set()  # Modal: bloquea la ventana principal

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.crear_panel_catalogo()
        self.crear_panel_lotes()

    # ── PANEL IZQUIERDO: Catálogo ─────────────────────────────────────────────
    def crear_panel_catalogo(self):
        """Formulario para registrar un nuevo tipo de medicamento."""
        self.frame_cat = ctk.CTkFrame(self, **CARD_STYLE)
        self.frame_cat.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.frame_cat.grid_rowconfigure(1, weight=1)
        self.frame_cat.grid_columnconfigure(0, weight=1)

        # ── Header ────────────────────────────────────────────────────────────
        header = ctk.CTkFrame(
            self.frame_cat, fg_color=COLORS["primary"],
            corner_radius=0, height=56
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        ctk.CTkLabel(
            header, text="➕   Nuevo Producto en Catálogo",
            font=FONTS["h2"], text_color="#FFFFFF"
        ).pack(side="left", padx=18)

        # ── Formulario ────────────────────────────────────────────────────────
        form = ctk.CTkFrame(self.frame_cat, fg_color="transparent")
        form.grid(row=1, column=0, padx=20, pady=16, sticky="nsew")
        form.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            form,
            text="Registra un nuevo tipo de medicamento\nen el catálogo de productos.",
            font=FONTS["body_small"],
            text_color=COLORS["text_secondary"],
            justify="left"
        ).pack(anchor="w", pady=(0, 16))

        # Campo: Nombre
        ctk.CTkLabel(form, text="Nombre del Producto",
                     font=FONTS["body"], text_color=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")
        self.ent_nombre = ctk.CTkEntry(
            form, placeholder_text="Ej. Ibuprofeno 400mg", **INPUT_STYLE
        )
        self.ent_nombre.pack(fill="x", pady=(4, 12))

        # Campo: Categoría
        ctk.CTkLabel(form, text="Categoría",
                     font=FONTS["body"], text_color=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")
        categorias = ["Venta Libre", "Antibiótico", "Controlado", "Material Médico"]
        self.combo_cat = ctk.CTkComboBox(
            form, values=categorias,
            corner_radius=RADIUS["input"],
            border_width=1,
            border_color=COLORS["border"],
            fg_color=COLORS["card_bg"],
            text_color=COLORS["text_primary"],
            button_color=COLORS["primary_light"],
            button_hover_color=COLORS["primary_hover"],
            dropdown_fg_color=COLORS["card_bg"],
            dropdown_text_color=COLORS["text_primary"],
            dropdown_hover_color=COLORS["panel_bg"],
            font=FONTS["body"],
            height=40
        )
        self.combo_cat.pack(fill="x", pady=(4, 12))

        # Campo: Precio de Venta
        ctk.CTkLabel(form, text="Precio de Venta (C$)",
                     font=FONTS["body"], text_color=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")
        self.ent_precio = ctk.CTkEntry(
            form, placeholder_text="Ej. 85.00", **INPUT_STYLE
        )
        self.ent_precio.pack(fill="x", pady=(4, 12))

        # Campo: Stock Mínimo
        ctk.CTkLabel(form, text="Stock Mínimo de Alerta",
                     font=FONTS["body"], text_color=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")
        self.ent_stock_min = ctk.CTkEntry(
            form, placeholder_text="Ej. 10", **INPUT_STYLE
        )
        self.ent_stock_min.pack(fill="x", pady=(4, 14))

        # Checkbox: Requiere Receta
        self.chk_receta = ctk.CTkCheckBox(
            form, text="  Requiere Receta Médica",
            font=FONTS["body"],
            text_color=COLORS["text_primary"],
            fg_color=COLORS["primary_light"],
            hover_color=COLORS["primary_hover"],
            border_color=COLORS["border"],
            checkmark_color="#FFFFFF",
            corner_radius=4
        )
        self.chk_receta.pack(anchor="w", pady=(0, 18))

        # Botón Crear Producto
        self.btn_guardar_cat = ctk.CTkButton(
            form, text="  ✚   Crear Producto",
            **BTN_PRIMARY,
            command=self.guardar_producto
        )
        self.btn_guardar_cat.pack(fill="x")

        # Mensaje de feedback
        self.lbl_msg_cat = ctk.CTkLabel(
            form, text="", font=FONTS["body_small"],
            text_color=COLORS["success_text"]
        )
        self.lbl_msg_cat.pack(pady=(10, 0))

    # ── PANEL DERECHO: Lotes ──────────────────────────────────────────────────
    def crear_panel_lotes(self):
        """Formulario para registrar las cajas físicas (lotes)."""
        self.frame_lote = ctk.CTkFrame(self, **CARD_STYLE)
        self.frame_lote.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.frame_lote.grid_rowconfigure(1, weight=1)
        self.frame_lote.grid_columnconfigure(0, weight=1)

        # ── Header ────────────────────────────────────────────────────────────
        header = ctk.CTkFrame(
            self.frame_lote, fg_color=COLORS["sidebar_bg"],
            corner_radius=0, height=56
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        ctk.CTkLabel(
            header, text="📥   Ingreso de Lote (Cajas)",
            font=FONTS["h2"], text_color="#FFFFFF"
        ).pack(side="left", padx=18)

        # ── Formulario ────────────────────────────────────────────────────────
        form = ctk.CTkFrame(self.frame_lote, fg_color="transparent")
        form.grid(row=1, column=0, padx=20, pady=16, sticky="nsew")
        form.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            form,
            text="Registra el ingreso físico de cajas\n(lote) de un producto ya en catálogo.",
            font=FONTS["body_small"],
            text_color=COLORS["text_secondary"],
            justify="left"
        ).pack(anchor="w", pady=(0, 16))

        # Campo: ID del Producto
        ctk.CTkLabel(form, text="ID del Producto",
                     font=FONTS["body"], text_color=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")
        self.ent_id_prod = ctk.CTkEntry(
            form, placeholder_text="Ej. 1001", **INPUT_STYLE
        )
        self.ent_id_prod.pack(fill="x", pady=(4, 12))

        # Campo: Código de Lote
        ctk.CTkLabel(form, text="Código de Lote",
                     font=FONTS["body"], text_color=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")
        self.ent_id_lote = ctk.CTkEntry(
            form, placeholder_text="Ej. L-001", **INPUT_STYLE
        )
        self.ent_id_lote.pack(fill="x", pady=(4, 12))

        # Campo: Cantidad
        ctk.CTkLabel(form, text="Cantidad (Cajas)",
                     font=FONTS["body"], text_color=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")
        self.ent_cantidad = ctk.CTkEntry(
            form, placeholder_text="Ej. 50", **INPUT_STYLE
        )
        self.ent_cantidad.pack(fill="x", pady=(4, 12))

        # Campo: Fecha de Vencimiento
        ctk.CTkLabel(form, text="⏰  Fecha de Vencimiento (YYYY-MM-DD)",
                     font=FONTS["body"], text_color=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")
        self.ent_fecha = ctk.CTkEntry(
            form, placeholder_text="Ej. 2026-12-31", **INPUT_STYLE
        )
        self.ent_fecha.pack(fill="x", pady=(4, 20))

        # Botón Registrar Lote
        self.btn_guardar_lote = ctk.CTkButton(
            form, text="  📥   Registrar Lote",
            **BTN_SUCCESS,
            command=self.guardar_lote
        )
        self.btn_guardar_lote.pack(fill="x")

        # Mensaje de feedback
        self.lbl_msg_lote = ctk.CTkLabel(
            form, text="", font=FONTS["body_small"],
            text_color=COLORS["success_text"]
        )
        self.lbl_msg_lote.pack(pady=(10, 0))

    # ── LÓGICA DE LA INTERFAZ ─────────────────────────────────────────────────
    def guardar_producto(self):
        nombre = self.ent_nombre.get().strip()
        categoria = self.combo_cat.get()
        precio_str = self.ent_precio.get().strip()
        stock_min_str = self.ent_stock_min.get().strip()
        requiere_receta = bool(self.chk_receta.get())

        if not nombre or not precio_str or not stock_min_str:
            self.lbl_msg_cat.configure(
                text="⚠  Complete todos los campos de texto.",
                text_color=COLORS["danger"]
            )
            return

        try:
            precio = float(precio_str)
            stock_min = int(stock_min_str)
            resultado = registrar_nuevo_producto(nombre, categoria, precio, stock_min, requiere_receta)

            if resultado["exito"]:
                self.lbl_msg_cat.configure(
                    text=f"✅  {resultado['mensaje']}",
                    text_color=COLORS["success_text"]
                )
                self.ent_nombre.delete(0, 'end')
                self.ent_precio.delete(0, 'end')
                self.ent_stock_min.delete(0, 'end')
                self.chk_receta.deselect()
            else:
                self.lbl_msg_cat.configure(
                    text=f"✗  {resultado['mensaje']}",
                    text_color=COLORS["danger"]
                )
        except ValueError:
            self.lbl_msg_cat.configure(
                text="✗  Precio y Stock deben ser números válidos.",
                text_color=COLORS["danger"]
            )

    def guardar_lote(self):
        id_prod_str = self.ent_id_prod.get().strip()
        id_lote = self.ent_id_lote.get().strip()
        cantidad_str = self.ent_cantidad.get().strip()
        fecha = self.ent_fecha.get().strip()

        if not id_prod_str or not id_lote or not cantidad_str or not fecha:
            self.lbl_msg_lote.configure(
                text="⚠  Complete todos los campos del lote.",
                text_color=COLORS["danger"]
            )
            return

        try:
            id_prod = int(id_prod_str)
            cantidad = int(cantidad_str)
            resultado = registrar_nuevo_lote(id_prod, id_lote, cantidad, fecha)

            if resultado["exito"]:
                self.lbl_msg_lote.configure(
                    text=f"✅  {resultado['mensaje']}",
                    text_color=COLORS["success_text"]
                )
                self.ent_id_prod.delete(0, 'end')
                self.ent_id_lote.delete(0, 'end')
                self.ent_cantidad.delete(0, 'end')
                self.ent_fecha.delete(0, 'end')

                # Actualizamos el dashboard que está de fondo
                self.master.cargar_datos_dashboard()
            else:
                self.lbl_msg_lote.configure(
                    text=f"✗  {resultado['mensaje']}",
                    text_color=COLORS["danger"]
                )
        except ValueError:
            self.lbl_msg_lote.configure(
                text="✗  ID Producto y Cantidad deben ser números enteros.",
                text_color=COLORS["danger"]
            )