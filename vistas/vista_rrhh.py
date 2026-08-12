import customtkinter as ctk
from logica.logica_rrhh import procesar_nomina_general
from logica.logica_finanzas import registrar_gasto_caja_chica, ejecutar_pago_nomina_mensual
from config_tema import COLORS, FONTS, RADIUS, CARD_STYLE, INPUT_STYLE, BTN_PRIMARY, BTN_SUCCESS, BTN_LOGOUT


class VistaRRHH(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Farmacentric — Recursos Humanos y Finanzas")
        self.geometry("980x640")
        self.minsize(840, 540)
        self.configure(fg_color=COLORS["app_bg"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.crear_panel_nomina()
        self.crear_panel_gastos()

    # ── PANEL IZQUIERDO: Nómina ───────────────────────────────────────────────
    def crear_panel_nomina(self):
        """Módulo para el pago de salarios a los trabajadores."""
        self.panel_izq = ctk.CTkFrame(self, **CARD_STYLE)
        self.panel_izq.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.panel_izq.grid_rowconfigure(2, weight=1)
        self.panel_izq.grid_columnconfigure(0, weight=1)

        # ── Header ────────────────────────────────────────────────────────────
        header = ctk.CTkFrame(
            self.panel_izq, fg_color=COLORS["primary"],
            corner_radius=0, height=56
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        ctk.CTkLabel(
            header, text="📑   Procesamiento de Nómina",
            font=FONTS["h2"], text_color="#FFFFFF"
        ).pack(side="left", padx=18)

        # ── Controles ─────────────────────────────────────────────────────────
        controles = ctk.CTkFrame(self.panel_izq, fg_color="transparent")
        controles.grid(row=1, column=0, padx=16, pady=14, sticky="ew")

        ctk.CTkLabel(
            controles,
            text="Calcula y ejecuta el pago mensual de salarios para todos\nlos empleados registrados en el sistema.",
            font=FONTS["body_small"],
            text_color=COLORS["text_secondary"],
            justify="left"
        ).pack(anchor="w", pady=(0, 12))

        self.btn_calcular = ctk.CTkButton(
            controles,
            text="  💰   Calcular y Pagar Nómina del Mes",
            **BTN_PRIMARY,
            command=self.procesar_pago
        )
        self.btn_calcular.pack(fill="x")

        # ── Área de Resultado (Colillas) ───────────────────────────────────────
        self.caja_nomina = ctk.CTkTextbox(
            self.panel_izq,
            font=FONTS["mono"],
            text_color=COLORS["text_primary"],
            fg_color=COLORS["app_bg"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=RADIUS["card"],
            wrap="none"
        )
        self.caja_nomina.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 12))
        self.caja_nomina.insert(
            "0.0",
            "Presione el botón de arriba para procesar la nómina actual.\n\n"
            "Los detalles de pago por empleado aparecerán aquí."
        )
        self.caja_nomina.configure(state="disabled")

        # ── Botón de Cerrar Sesión ────────────────────────────────────────────
        ctk.CTkFrame(self.panel_izq, height=1, fg_color=COLORS["border"]).grid(
            row=3, column=0, sticky="ew", padx=16
        )

        self.btn_salir = ctk.CTkButton(
            self.panel_izq,
            text="  ⏻   Cerrar Sesión",
            width=200, **BTN_LOGOUT,
            command=lambda: self.master.cerrar_sesion(self)
        )
        self.btn_salir.grid(row=4, column=0, padx=20, pady=14, sticky="w")

    # ── PANEL DERECHO: Caja Chica ─────────────────────────────────────────────
    def crear_panel_gastos(self):
        """Módulo para registrar gastos operativos de caja chica."""
        self.panel_der = ctk.CTkFrame(self, **CARD_STYLE)
        self.panel_der.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.panel_der.grid_rowconfigure(2, weight=1)
        self.panel_der.grid_columnconfigure(0, weight=1)

        # ── Header ────────────────────────────────────────────────────────────
        header = ctk.CTkFrame(
            self.panel_der, fg_color=COLORS["sidebar_bg"],
            corner_radius=0, height=56
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        ctk.CTkLabel(
            header, text="🧾   Registro de Caja Chica",
            font=FONTS["h2"], text_color="#FFFFFF"
        ).pack(side="left", padx=18)

        # ── Formulario ────────────────────────────────────────────────────────
        form = ctk.CTkFrame(self.panel_der, fg_color="transparent")
        form.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        form.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            form,
            text="Registra gastos operativos menores como\npapelería, servicios o insumos de limpieza.",
            font=FONTS["body_small"],
            text_color=COLORS["text_secondary"],
            justify="left"
        ).pack(anchor="w", pady=(0, 20))

        # Campo: Concepto
        ctk.CTkLabel(
            form, text="Concepto del Gasto",
            font=FONTS["body"], text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(fill="x")

        self.entrada_concepto = ctk.CTkEntry(
            form, placeholder_text="Ej. Papelería, Limpieza, Servicio...",
            **INPUT_STYLE
        )
        self.entrada_concepto.pack(fill="x", pady=(4, 14))

        # Campo: Monto
        ctk.CTkLabel(
            form, text="Monto en Córdobas (C$)",
            font=FONTS["body"], text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(fill="x")

        self.entrada_monto = ctk.CTkEntry(
            form, placeholder_text="Ej. 250.00",
            **INPUT_STYLE
        )
        self.entrada_monto.pack(fill="x", pady=(4, 20))

        # Botón Registrar Gasto
        self.btn_gasto = ctk.CTkButton(
            form,
            text="  ✔   Registrar Gasto",
            **BTN_SUCCESS,
            command=self.registrar_gasto
        )
        self.btn_gasto.pack(fill="x")

        # Mensaje de feedback
        self.lbl_mensaje_gasto = ctk.CTkLabel(
            form, text="",
            font=FONTS["body_small"],
            text_color=COLORS["success_text"]
        )
        self.lbl_mensaje_gasto.pack(pady=(12, 0))

        # ── Historial de gastos (scroll) ───────────────────────────────────────
        ctk.CTkFrame(form, height=1, fg_color=COLORS["border"]).pack(fill="x", pady=16)

        ctk.CTkLabel(
            form, text="Gastos Registrados en esta Sesión",
            font=FONTS["h3"], text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(anchor="w", pady=(0, 8))

        self.scroll_gastos = ctk.CTkScrollableFrame(
            form,
            fg_color=COLORS["app_bg"],
            corner_radius=RADIUS["card"],
            border_width=1,
            border_color=COLORS["border"],
            height=160
        )
        self.scroll_gastos.pack(fill="both", expand=True)

        # Mensaje inicial
        ctk.CTkLabel(
            self.scroll_gastos,
            text="Aún no se han registrado gastos.",
            font=FONTS["body_small"],
            text_color=COLORS["text_secondary"]
        ).pack(pady=20)

    # ── LÓGICA DE LA INTERFAZ ─────────────────────────────────────────────────
    def procesar_pago(self):
        """Ejecuta el pago de nómina y muestra las colillas."""
        ejecutar_pago_nomina_mensual()
        reporte = procesar_nomina_general()

        texto = "╔══════════════════════════════════╗\n"
        texto += "║       COLILLAS DE PAGO           ║\n"
        texto += "╚══════════════════════════════════╝\n\n"

        for pago in reporte["detalle"]:
            texto += f"  Empleado : {pago['nombre']}\n"
            texto += f"  Cargo    : {pago['cargo']}\n"
            texto += f"  Bruto    : C$ {pago['desglose']['salario_bruto']:,.2f}\n"
            texto += f"  -INSS    : C$ {pago['desglose']['deduccion_inss']:,.2f}\n"
            texto += f"  NETO     : C$ {pago['desglose']['salario_neto']:,.2f}\n"
            texto += "  " + "─" * 32 + "\n\n"

        texto += f"  TOTAL DESEMBOLSADO: C$ {reporte['totales_empresa']['costo_total_nomina']:,.2f}\n"

        self.caja_nomina.configure(state="normal")
        self.caja_nomina.delete("0.0", "end")
        self.caja_nomina.insert("0.0", texto)
        self.caja_nomina.configure(state="disabled")

        # Desactivar el botón para evitar pago doble
        self.btn_calcular.configure(
            state="disabled",
            text="  ✅   Nómina Pagada",
            fg_color=COLORS["success"],
            hover_color=COLORS["success"]
        )

    def registrar_gasto(self):
        """Registra un gasto de caja chica y lo muestra en el historial."""
        concepto = self.entrada_concepto.get().strip()
        monto_str = self.entrada_monto.get().strip()

        if not concepto or not monto_str:
            self.lbl_mensaje_gasto.configure(
                text="⚠  Complete todos los campos.",
                text_color=COLORS["danger"]
            )
            return

        try:
            monto = float(monto_str)
            resultado = registrar_gasto_caja_chica(concepto, monto)

            if resultado["exito"]:
                self.lbl_mensaje_gasto.configure(
                    text=f"✅  {resultado['mensaje']}",
                    text_color=COLORS["success_text"]
                )
                # Agregar al historial visual
                self._agregar_gasto_historial(concepto, monto)
                self.entrada_concepto.delete(0, 'end')
                self.entrada_monto.delete(0, 'end')
            else:
                self.lbl_mensaje_gasto.configure(
                    text=resultado["mensaje"],
                    text_color=COLORS["danger"]
                )
        except ValueError:
            self.lbl_mensaje_gasto.configure(
                text="✗  El monto debe ser un número válido.",
                text_color=COLORS["danger"]
            )

    def _agregar_gasto_historial(self, concepto, monto):
        """Agrega una fila al historial de gastos de la sesión."""
        # Limpiar mensaje "Aún no se han registrado gastos" si existe
        for widget in self.scroll_gastos.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        fila = ctk.CTkFrame(
            self.scroll_gastos,
            corner_radius=6,
            fg_color=COLORS["card_bg"],
            border_width=1,
            border_color=COLORS["border"]
        )
        fila.pack(fill="x", pady=3, padx=4)

        ctk.CTkFrame(fila, width=4, corner_radius=2,
                     fg_color=COLORS["warning"]).pack(
            side="left", fill="y", padx=(4, 0), pady=6
        )

        ctk.CTkLabel(
            fila, text=concepto,
            font=FONTS["body"], text_color=COLORS["text_primary"],
            anchor="w"
        ).pack(side="left", padx=10, pady=8)

        ctk.CTkLabel(
            fila, text=f"C$ {monto:,.2f}",
            font=FONTS["btn"], text_color=COLORS["danger"],
            anchor="e"
        ).pack(side="right", padx=12, pady=8)