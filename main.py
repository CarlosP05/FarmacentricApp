import customtkinter as ctk
from logica.logica_auth import iniciar_sesion
from vistas.vista_admin import DashboardAdmin
from vistas.vista_cajero import VistaCajero
from vistas.vista_rrhh import VistaRRHH
from config_tema import COLORS, FONTS, RADIUS, INPUT_STYLE

# Configuración global de la apariencia
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class AplicacionFarmacentric(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Farmacentric — Acceso al Sistema")
        self.geometry("820x520")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["card_bg"])
        self.eval('tk::PlaceWindow . center')

        self.crear_pantalla_login()

    def crear_pantalla_login(self):
        # ── Panel Izquierdo: Branding ─────────────────────────────────────────
        self.panel_marca = ctk.CTkFrame(
            self, width=340, corner_radius=0,
            fg_color=COLORS["sidebar_bg"]
        )
        self.panel_marca.pack(side="left", fill="y")
        self.panel_marca.pack_propagate(False)

        # Espaciador superior
        ctk.CTkFrame(self.panel_marca, fg_color="transparent", height=80).pack()

        # Cruz médica — ícono central de salud
        ctk.CTkLabel(
            self.panel_marca, text="✚",
            font=("Segoe UI", 60),
            text_color=COLORS["success"]
        ).pack()

        ctk.CTkLabel(
            self.panel_marca, text="Farmacentric",
            font=FONTS["logo"],
            text_color=COLORS["sidebar_text"]
        ).pack(pady=(12, 4))

        ctk.CTkLabel(
            self.panel_marca, text="Sistema de Gestión Integral",
            font=FONTS["logo_sub"],
            text_color=COLORS["sidebar_subtext"]
        ).pack()

        # Separador decorativo
        ctk.CTkFrame(
            self.panel_marca, height=2, width=110,
            fg_color=COLORS["primary_light"]
        ).pack(pady=28)

        # Características del sistema
        for texto in ["🏥  Gestión de Inventario", "💳  Punto de Venta (POS)", "👥  Recursos Humanos"]:
            ctk.CTkLabel(
                self.panel_marca, text=texto,
                font=FONTS["body_small"],
                text_color=COLORS["sidebar_subtext"],
                anchor="w"
            ).pack(padx=40, pady=3, anchor="w")

        # Slogan al fondo
        ctk.CTkFrame(self.panel_marca, fg_color="transparent").pack(expand=True)
        ctk.CTkLabel(
            self.panel_marca, text="Salud · Confianza · Precisión",
            font=FONTS["body_small"],
            text_color="#4A6B8A"
        ).pack(pady=24)

        # ── Panel Derecho: Formulario ─────────────────────────────────────────
        self.panel_form = ctk.CTkFrame(
            self, corner_radius=0,
            fg_color=COLORS["card_bg"]
        )
        self.panel_form.pack(side="right", fill="both", expand=True)

        # Contenedor centrado dentro del panel derecho
        form_container = ctk.CTkFrame(self.panel_form, fg_color="transparent")
        form_container.place(relx=0.5, rely=0.5, anchor="center")

        # Encabezado del formulario
        ctk.CTkLabel(
            form_container, text="Bienvenido de Vuelta",
            font=FONTS["h1"],
            text_color=COLORS["text_primary"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            form_container, text="Ingresa tus credenciales para continuar",
            font=FONTS["body_small"],
            text_color=COLORS["text_secondary"]
        ).pack(anchor="w", pady=(4, 28))

        # Campo: Usuario
        ctk.CTkLabel(
            form_container, text="Usuario",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(fill="x")

        self.entrada_usuario = ctk.CTkEntry(
            form_container, width=290,
            placeholder_text="ej. admin",
            **INPUT_STYLE
        )
        self.entrada_usuario.pack(pady=(4, 16))
        self.entrada_usuario.bind("<Return>", lambda e: self.entrada_password.focus())

        # Campo: Contraseña
        ctk.CTkLabel(
            form_container, text="Contraseña",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(fill="x")

        self.entrada_password = ctk.CTkEntry(
            form_container, width=290,
            placeholder_text="••••••••",
            show="•",
            **INPUT_STYLE
        )
        self.entrada_password.pack(pady=(4, 6))
        self.entrada_password.bind("<Return>", lambda e: self.validar_login())

        # Mensaje de error / éxito
        self.lbl_error = ctk.CTkLabel(
            form_container, text="",
            font=FONTS["body_small"],
            text_color=COLORS["danger"]
        )
        self.lbl_error.pack(pady=(4, 16))

        # Botón de inicio de sesión
        self.btn_login = ctk.CTkButton(
            form_container,
            text="Iniciar Sesión  →",
            width=290, height=46,
            corner_radius=RADIUS["btn_lg"],
            fg_color=COLORS["primary_light"],
            hover_color=COLORS["primary_hover"],
            text_color="#FFFFFF",
            font=FONTS["btn_large"],
            command=self.validar_login
        )
        self.btn_login.pack()

        # Versión del sistema
        ctk.CTkLabel(
            self.panel_form, text="v1.0  |  © 2026 Farmacentric",
            font=("Segoe UI", 10),
            text_color=COLORS["border"]
        ).place(relx=0.5, rely=0.95, anchor="center")

    def validar_login(self):
        """Conecta la interfaz gráfica con la lógica de autenticación."""
        user = self.entrada_usuario.get()
        password = self.entrada_password.get()

        # Limpiar mensaje previo
        self.lbl_error.configure(text="", text_color=COLORS["danger"])

        if not user or not password:
            self.lbl_error.configure(text="⚠  Por favor, complete todos los campos.")
            return

        # Deshabilitar botón durante validación
        self.btn_login.configure(state="disabled", text="Verificando...")

        respuesta = iniciar_sesion(user, password)

        if respuesta["exito"]:
            self.lbl_error.configure(
                text=f"✓  {respuesta['mensaje']}",
                text_color=COLORS["success_text"]
            )
            rol_usuario = respuesta["datos_usuario"]["rol"]

            if rol_usuario == "Administrador":
                self.withdraw()
                ventana_admin = DashboardAdmin(self)
                ventana_admin.protocol("WM_DELETE_WINDOW", self.destroy)

            elif rol_usuario == "Cajero/Farmacéutico":
                self.withdraw()
                ventana_cajero = VistaCajero(self)
                ventana_cajero.protocol("WM_DELETE_WINDOW", self.destroy)

            elif rol_usuario == "Contador/RRHH":
                self.withdraw()
                ventana_rrhh = VistaRRHH(self)
                ventana_rrhh.protocol("WM_DELETE_WINDOW", self.destroy)
            else:
                print(f"La vista para el rol '{rol_usuario}' aún no está construida.")
                self.btn_login.configure(state="normal", text="Iniciar Sesión  →")
        else:
            self.lbl_error.configure(
                text=f"✗  {respuesta['mensaje']}",
                text_color=COLORS["danger"]
            )
            self.btn_login.configure(state="normal", text="Iniciar Sesión  →")

    def cerrar_sesion(self, ventana_top):
        """Cierra el dashboard y vuelve a mostrar el login limpio."""
        ventana_top.destroy()
        self.entrada_usuario.delete(0, 'end')
        self.entrada_password.delete(0, 'end')
        self.lbl_error.configure(text="")
        self.btn_login.configure(state="normal", text="Iniciar Sesión  →")
        self.deiconify()


# Ejecutamos la aplicación
if __name__ == "__main__":
    app = AplicacionFarmacentric()
    app.mainloop()