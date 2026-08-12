import customtkinter as ctk
from logica.logica_pos import calcular_venta, procesar_venta
from logica.logica_finanzas import registrar_ingreso_venta
from config_tema import COLORS, FONTS, RADIUS, CARD_STYLE, INPUT_STYLE, BTN_PRIMARY, BTN_SUCCESS, BTN_LOGOUT


class VistaCajero(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Farmacentric — Punto de Venta (POS)")
        self.geometry("980x640")
        self.minsize(840, 540)
        self.configure(fg_color=COLORS["app_bg"])

        # Estado interno
        self.carrito = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.crear_panel_izquierdo()
        self.crear_panel_derecho()

    # ── PANEL IZQUIERDO: Búsqueda y acciones ──────────────────────────────────
    def crear_panel_izquierdo(self):
        """Panel de búsqueda de productos y controles del carrito."""
        self.panel_izq = ctk.CTkFrame(self, **CARD_STYLE)
        self.panel_izq.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.panel_izq.grid_rowconfigure(8, weight=1)  # Expande espacio libre

        # ── Header del panel ──────────────────────────────────────────────────
        header = ctk.CTkFrame(
            self.panel_izq, fg_color=COLORS["primary"],
            corner_radius=0, height=56
        )
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.grid_propagate(False)

        ctk.CTkLabel(
            header, text="🛒   Agregar Producto",
            font=FONTS["h2"], text_color="#FFFFFF"
        ).pack(side="left", padx=18, pady=10)

        # ── Formulario ────────────────────────────────────────────────────────
        form = ctk.CTkFrame(self.panel_izq, fg_color="transparent")
        form.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.panel_izq.grid_columnconfigure(0, weight=1)

        # Campo: ID del Producto
        ctk.CTkLabel(
            form, text="ID del Producto",
            font=FONTS["body"], text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(fill="x")

        self.entrada_id = ctk.CTkEntry(
            form, placeholder_text="Ej. 1001",
            **INPUT_STYLE
        )
        self.entrada_id.pack(fill="x", pady=(4, 14))
        self.entrada_id.bind("<Return>", lambda e: self.entrada_cantidad.focus())

        # Campo: Cantidad
        ctk.CTkLabel(
            form, text="Cantidad",
            font=FONTS["body"], text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(fill="x")

        self.entrada_cantidad = ctk.CTkEntry(
            form, placeholder_text="Ej. 2",
            **INPUT_STYLE
        )
        self.entrada_cantidad.pack(fill="x", pady=(4, 20))
        self.entrada_cantidad.bind("<Return>", lambda e: self.agregar_al_carrito())

        # Botón Añadir al Carrito
        self.btn_agregar = ctk.CTkButton(
            form, text="  ➕   Añadir al Carrito",
            **BTN_PRIMARY,
            command=self.agregar_al_carrito
        )
        self.btn_agregar.pack(fill="x")

        # Separador
        ctk.CTkFrame(form, height=1, fg_color=COLORS["border"]).pack(fill="x", pady=16)

        # Botón Limpiar Carrito (ghost)
        self.btn_limpiar = ctk.CTkButton(
            form,
            text="  🗑   Limpiar Carrito",
            height=38,
            corner_radius=RADIUS["btn"],
            fg_color="transparent",
            hover_color=COLORS["panel_bg"],
            text_color=COLORS["text_secondary"],
            border_width=1,
            border_color=COLORS["border"],
            font=FONTS["btn"],
            command=self.limpiar_carrito
        )
        self.btn_limpiar.pack(fill="x")

        # Mensaje de feedback
        self.lbl_mensaje = ctk.CTkLabel(
            form, text="",
            font=FONTS["body_small"],
            text_color=COLORS["danger"]
        )
        self.lbl_mensaje.pack(pady=(12, 0))

        # ── Botón de Cerrar Sesión (al fondo) ────────────────────────────────
        separador_inf = ctk.CTkFrame(
            self.panel_izq, height=1, fg_color=COLORS["border"]
        )
        separador_inf.grid(row=7, column=0, sticky="ew", padx=16)

        self.btn_salir = ctk.CTkButton(
            self.panel_izq,
            text="  ⏻   Cerrar Sesión",
            width=200, **BTN_LOGOUT,
            command=lambda: self.master.cerrar_sesion(self)
        )
        self.btn_salir.grid(row=9, column=0, padx=20, pady=16, sticky="s")

    # ── PANEL DERECHO: Ticket de venta ────────────────────────────────────────
    def crear_panel_derecho(self):
        """Panel del ticket de venta y botón de cobro."""
        self.panel_der = ctk.CTkFrame(self, **CARD_STYLE)
        self.panel_der.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.panel_der.grid_rowconfigure(1, weight=1)
        self.panel_der.grid_columnconfigure(0, weight=1)

        # ── Header del ticket ─────────────────────────────────────────────────
        header = ctk.CTkFrame(
            self.panel_der, fg_color=COLORS["sidebar_bg"],
            corner_radius=0, height=56
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        ctk.CTkLabel(
            header, text="🧾   Ticket de Venta",
            font=FONTS["h2"], text_color="#FFFFFF"
        ).pack(side="left", padx=18, pady=10)

        # ── Área Scrollable de Ítems ──────────────────────────────────────────
        self.scroll_ticket = ctk.CTkScrollableFrame(
            self.panel_der,
            fg_color=COLORS["app_bg"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary_light"],
            corner_radius=0
        )
        self.scroll_ticket.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        # Mensaje inicial del ticket vacío
        self.lbl_ticket_vacio = ctk.CTkLabel(
            self.scroll_ticket,
            text="El carrito está vacío.\nAgrega productos desde el panel izquierdo.",
            font=FONTS["body_small"],
            text_color=COLORS["text_secondary"],
            justify="center"
        )
        self.lbl_ticket_vacio.pack(pady=40)

        # ── Franja de Total ───────────────────────────────────────────────────
        total_frame = ctk.CTkFrame(
            self.panel_der, fg_color=COLORS["panel_bg"],
            corner_radius=0, height=72
        )
        total_frame.grid(row=2, column=0, sticky="ew")
        total_frame.grid_propagate(False)

        ctk.CTkLabel(
            total_frame, text="TOTAL A PAGAR",
            font=FONTS["body_small"],
            text_color=COLORS["text_secondary"]
        ).pack(anchor="w", padx=18, pady=(10, 0))

        self.lbl_total = ctk.CTkLabel(
            total_frame, text="C$ 0.00",
            font=FONTS["kpi"],
            text_color=COLORS["success"]
        )
        self.lbl_total.pack(anchor="w", padx=18)

        # ── Botón de Pago ─────────────────────────────────────────────────────
        self.btn_cobrar = ctk.CTkButton(
            self.panel_der,
            text="  💳   PROCESAR PAGO",
            **BTN_SUCCESS,
            command=self.cobrar
        )
        self.btn_cobrar.grid(row=3, column=0, sticky="ew", padx=16, pady=14)

    # ── LÓGICA DE LA INTERFAZ ─────────────────────────────────────────────────
    def agregar_al_carrito(self):
        self.lbl_mensaje.configure(text="", text_color=COLORS["danger"])
        id_prod = self.entrada_id.get().strip()
        cant = self.entrada_cantidad.get().strip()

        if not id_prod.isdigit() or not cant.isdigit():
            self.lbl_mensaje.configure(text="⚠  Ingrese solo números en ambos campos.")
            return

        self.carrito.append({"id_producto": int(id_prod), "cantidad": int(cant)})
        self.actualizar_ticket()

        self.entrada_id.delete(0, 'end')
        self.entrada_cantidad.delete(0, 'end')
        self.entrada_id.focus()

    def actualizar_ticket(self):
        """Reconstruye el área del ticket con los ítems actuales del carrito."""
        # Limpiar contenido anterior del scroll
        for widget in self.scroll_ticket.winfo_children():
            widget.destroy()

        if not self.carrito:
            self.lbl_ticket_vacio = ctk.CTkLabel(
                self.scroll_ticket,
                text="El carrito está vacío.\nAgrega productos desde el panel izquierdo.",
                font=FONTS["body_small"],
                text_color=COLORS["text_secondary"],
                justify="center"
            )
            self.lbl_ticket_vacio.pack(pady=40)
            self.lbl_total.configure(text="C$ 0.00")
            return

        resultado = calcular_venta(self.carrito)

        # Renderizar cada ítem como una tarjeta
        for item in resultado["detalle"]:
            item_frame = ctk.CTkFrame(
                self.scroll_ticket,
                corner_radius=8,
                fg_color=COLORS["card_bg"],
                border_width=1,
                border_color=COLORS["border"]
            )
            item_frame.pack(fill="x", pady=4, padx=8)

            # Barra lateral verde
            ctk.CTkFrame(item_frame, width=4, corner_radius=2,
                         fg_color=COLORS["success"]).pack(
                side="left", fill="y", padx=(6, 0), pady=8
            )

            info = ctk.CTkFrame(item_frame, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, padx=12, pady=8)

            ctk.CTkLabel(
                info,
                text=f"{item['cantidad']}x  {item['producto']}",
                font=FONTS["body"], text_color=COLORS["text_primary"],
                anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                info,
                text=f"Subtotal: C$ {item['subtotal']:.2f}",
                font=FONTS["body_small"], text_color=COLORS["text_secondary"],
                anchor="w"
            ).pack(anchor="w")

        # Advertencia de recetas requeridas
        if resultado.get("pedir_recetas_para"):
            receta_frame = ctk.CTkFrame(
                self.scroll_ticket,
                corner_radius=8,
                fg_color="#FEF3C7",
                border_width=1,
                border_color=COLORS["warning"]
            )
            receta_frame.pack(fill="x", pady=(8, 4), padx=8)

            ctk.CTkLabel(
                receta_frame,
                text="📋  Solicitar receta médica para:",
                font=FONTS["body"], text_color="#92400E",
                anchor="w"
            ).pack(anchor="w", padx=12, pady=(8, 4))

            for med in resultado["pedir_recetas_para"]:
                ctk.CTkLabel(
                    receta_frame,
                    text=f"    •  {med}",
                    font=FONTS["body_small"], text_color="#92400E",
                    anchor="w"
                ).pack(anchor="w", padx=12)

            ctk.CTkFrame(receta_frame, fg_color="transparent", height=8).pack()

        # Actualizar total
        self.lbl_total.configure(text=f"C$ {resultado['total_pagar']:,.2f}")

    def limpiar_carrito(self):
        self.carrito = []
        self.actualizar_ticket()
        self.lbl_mensaje.configure(
            text="🗑  Carrito limpiado.",
            text_color=COLORS["text_secondary"]
        )

    def cobrar(self):
        if not self.carrito:
            self.lbl_mensaje.configure(
                text="⚠  No hay productos en el carrito.",
                text_color=COLORS["danger"]
            )
            return

        resultado = procesar_venta(self.carrito)

        if resultado["exito"]:
            registrar_ingreso_venta(resultado["total_cobrado"])
            self.limpiar_carrito()
            self.lbl_mensaje.configure(
                text="✅  Venta procesada exitosamente.",
                text_color=COLORS["success_text"]
            )
        else:
            self.lbl_mensaje.configure(
                text=f"✗  {resultado['mensaje']}",
                text_color=COLORS["danger"]
            )