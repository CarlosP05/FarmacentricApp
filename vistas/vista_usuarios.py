import customtkinter as ctk
from logica.logica_usuarios import registrar_nuevo_usuario, obtener_lista_usuarios
from Datos.datos_usuarios import ROLES
from config_tema import COLORS, FONTS, RADIUS, CARD_STYLE, INPUT_STYLE, BTN_PRIMARY


class VistaUsuarios(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Farmacentric — Gestión de Usuarios")
        self.geometry("780x560")
        self.minsize(700, 480)
        self.configure(fg_color=COLORS["app_bg"])
        self.grab_set()  # Modal

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.crear_formulario()
        self.crear_lista_usuarios()
        self.actualizar_lista()

    # ── PANEL IZQUIERDO: Formulario Nuevo Usuario ──────────────────────────────
    def crear_formulario(self):
        """Panel para registrar nuevos accesos al sistema."""
        self.frame_form = ctk.CTkFrame(self, **CARD_STYLE)
        self.frame_form.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.frame_form.grid_rowconfigure(1, weight=1)
        self.frame_form.grid_columnconfigure(0, weight=1)

        # ── Header ────────────────────────────────────────────────────────────
        header = ctk.CTkFrame(
            self.frame_form, fg_color=COLORS["primary"],
            corner_radius=0, height=56
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        ctk.CTkLabel(
            header, text="👤   Nuevo Usuario",
            font=FONTS["h2"], text_color="#FFFFFF"
        ).pack(side="left", padx=18)

        # ── Formulario ────────────────────────────────────────────────────────
        form = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        form.grid(row=1, column=0, padx=20, pady=16, sticky="nsew")
        form.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            form,
            text="Crea credenciales de acceso para\nun nuevo miembro del equipo.",
            font=FONTS["body_small"],
            text_color=COLORS["text_secondary"],
            justify="left"
        ).pack(anchor="w", pady=(0, 20))

        # Campo: Nombre de usuario
        ctk.CTkLabel(form, text="Nombre de Usuario",
                     font=FONTS["body"], text_color=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")
        self.entrada_user = ctk.CTkEntry(
            form, placeholder_text="Ej. juan.perez", **INPUT_STYLE
        )
        self.entrada_user.pack(fill="x", pady=(4, 14))

        # Campo: Contraseña
        ctk.CTkLabel(form, text="Contraseña",
                     font=FONTS["body"], text_color=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")
        self.entrada_pass = ctk.CTkEntry(
            form, placeholder_text="••••••••",
            show="•", **INPUT_STYLE
        )
        self.entrada_pass.pack(fill="x", pady=(4, 14))

        # Campo: Rol
        ctk.CTkLabel(form, text="Rol en el Sistema",
                     font=FONTS["body"], text_color=COLORS["text_secondary"],
                     anchor="w").pack(fill="x")
        roles_disponibles = [ROLES["ADMIN"], ROLES["RRHH"], ROLES["CAJERO"]]
        self.combo_rol = ctk.CTkComboBox(
            form, values=roles_disponibles,
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
        self.combo_rol.pack(fill="x", pady=(4, 22))

        # Botón Registrar
        self.btn_guardar = ctk.CTkButton(
            form, text="  ✔   Registrar Acceso",
            **BTN_PRIMARY,
            command=self.guardar_usuario
        )
        self.btn_guardar.pack(fill="x")

        # Mensaje de feedback
        self.lbl_mensaje = ctk.CTkLabel(
            form, text="",
            font=FONTS["body_small"],
            text_color=COLORS["success_text"]
        )
        self.lbl_mensaje.pack(pady=(12, 0))

    # ── PANEL DERECHO: Lista de Usuarios ──────────────────────────────────────
    def crear_lista_usuarios(self):
        """Panel con la lista de usuarios registrados en el sistema."""
        self.frame_lista = ctk.CTkFrame(self, **CARD_STYLE)
        self.frame_lista.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.frame_lista.grid_rowconfigure(1, weight=1)
        self.frame_lista.grid_columnconfigure(0, weight=1)

        # ── Header ────────────────────────────────────────────────────────────
        header = ctk.CTkFrame(
            self.frame_lista, fg_color=COLORS["sidebar_bg"],
            corner_radius=0, height=56
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        ctk.CTkLabel(
            header, text="👥   Usuarios Activos",
            font=FONTS["h2"], text_color="#FFFFFF"
        ).pack(side="left", padx=18)

        # ── Scroll de tarjetas de usuario ─────────────────────────────────────
        self.scroll_usuarios = ctk.CTkScrollableFrame(
            self.frame_lista,
            fg_color=COLORS["app_bg"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary_light"],
            corner_radius=0
        )
        self.scroll_usuarios.grid(row=1, column=0, sticky="nsew", padx=12, pady=12)
        self.scroll_usuarios.grid_columnconfigure(0, weight=1)

    def _color_rol(self, rol):
        """Retorna el color de acento según el rol del usuario."""
        if "Admin" in rol:
            return COLORS["primary_light"]
        elif "RRHH" in rol or "Contador" in rol:
            return COLORS["warning"]
        else:
            return COLORS["success"]

    def _etiqueta_rol(self, rol):
        """Retorna el ícono del rol."""
        if "Admin" in rol:
            return "⊞"
        elif "RRHH" in rol or "Contador" in rol:
            return "💰"
        else:
            return "🛒"

    def actualizar_lista(self):
        """Lee los datos y construye tarjetas de usuario individuales."""
        # Limpiar contenido anterior
        for widget in self.scroll_usuarios.winfo_children():
            widget.destroy()

        usuarios_actuales = obtener_lista_usuarios()

        if not usuarios_actuales:
            ctk.CTkLabel(
                self.scroll_usuarios,
                text="No hay usuarios registrados.",
                font=FONTS["body_small"],
                text_color=COLORS["text_secondary"]
            ).pack(pady=30)
            return

        for u in usuarios_actuales:
            estado_activo = u.get("activo", True)
            color_rol = self._color_rol(u["rol"])
            icono_rol = self._etiqueta_rol(u["rol"])

            # Tarjeta de usuario
            tarjeta = ctk.CTkFrame(
                self.scroll_usuarios,
                corner_radius=10,
                fg_color=COLORS["card_bg"],
                border_width=1,
                border_color=COLORS["border"]
            )
            tarjeta.pack(fill="x", pady=5, padx=4)
            tarjeta.grid_columnconfigure(1, weight=1)

            # Franja lateral de color según rol
            ctk.CTkFrame(
                tarjeta, width=5, corner_radius=3,
                fg_color=color_rol
            ).grid(row=0, column=0, rowspan=3, sticky="ns", padx=(8, 0), pady=10)

            # Avatar / Ícono
            ctk.CTkLabel(
                tarjeta, text=icono_rol,
                font=("Segoe UI", 24),
                text_color=color_rol,
                width=40
            ).grid(row=0, column=1, rowspan=2, padx=(12, 4), pady=10)

            # Nombre de usuario
            ctk.CTkLabel(
                tarjeta, text=u["username"],
                font=FONTS["h3"],
                text_color=COLORS["text_primary"],
                anchor="w"
            ).grid(row=0, column=2, sticky="w", padx=(4, 8), pady=(10, 0))

            # Rol
            ctk.CTkLabel(
                tarjeta, text=u["rol"],
                font=FONTS["body_small"],
                text_color=COLORS["text_secondary"],
                anchor="w"
            ).grid(row=1, column=2, sticky="w", padx=(4, 8), pady=(0, 10))

            # Badge de estado (Activo / Inactivo)
            badge_color = COLORS["success"] if estado_activo else COLORS["danger"]
            badge_text = "● Activo" if estado_activo else "● Inactivo"
            ctk.CTkLabel(
                tarjeta, text=badge_text,
                font=("Segoe UI", 11, "bold"),
                text_color=badge_color,
                anchor="e"
            ).grid(row=0, column=3, padx=(0, 14), pady=(10, 0), sticky="e")

            # ID del usuario
            ctk.CTkLabel(
                tarjeta, text=f"ID: {u['id_usuario']}",
                font=FONTS["body_small"],
                text_color=COLORS["border"],
                anchor="e"
            ).grid(row=1, column=3, padx=(0, 14), pady=(0, 10), sticky="e")

    # ── LÓGICA DE LA INTERFAZ ─────────────────────────────────────────────────
    def guardar_usuario(self):
        user = self.entrada_user.get().strip()
        password = self.entrada_pass.get()
        rol = self.combo_rol.get()

        if not user or not password:
            self.lbl_mensaje.configure(
                text="⚠  Complete todos los campos.",
                text_color=COLORS["danger"]
            )
            return

        resultado = registrar_nuevo_usuario(user, password, rol)

        if resultado["exito"]:
            self.lbl_mensaje.configure(
                text=f"✅  {resultado['mensaje']}",
                text_color=COLORS["success_text"]
            )
            self.entrada_user.delete(0, 'end')
            self.entrada_pass.delete(0, 'end')
            self.actualizar_lista()
        else:
            self.lbl_mensaje.configure(
                text=f"✗  {resultado['mensaje']}",
                text_color=COLORS["danger"]
            )