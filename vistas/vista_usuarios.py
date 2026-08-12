import customtkinter as ctk
from logica.logica_usuarios import registrar_nuevo_usuario, obtener_lista_usuarios
from Datos.datos_usuarios import ROLES

class VistaUsuarios(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Farmacentric - Gestión de Usuarios")
        self.geometry("700x500")
        self.minsize(600, 450)
        
        # Hacemos que esta ventana bloquee la principal hasta que se cierre (Modal)
        self.grab_set() 

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1) # Formulario
        self.grid_columnconfigure(1, weight=1) # Lista

        self.crear_formulario()
        self.crear_lista_usuarios()
        self.actualizar_lista()

    def crear_formulario(self):
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        ctk.CTkLabel(self.frame_form, text="Nuevo Usuario", font=("Roboto", 18, "bold")).pack(pady=(20, 15))

        self.entrada_user = ctk.CTkEntry(self.frame_form, placeholder_text="Nombre de usuario", width=220)
        self.entrada_user.pack(pady=10)

        self.entrada_pass = ctk.CTkEntry(self.frame_form, placeholder_text="Contraseña", width=220, show="*")
        self.entrada_pass.pack(pady=10)

        # Menú desplegable para seleccionar el rol
        roles_disponibles = [ROLES["ADMIN"], ROLES["RRHH"], ROLES["CAJERO"]]
        self.combo_rol = ctk.CTkComboBox(self.frame_form, values=roles_disponibles, width=220)
        self.combo_rol.pack(pady=10)

        self.btn_guardar = ctk.CTkButton(self.frame_form, text="Registrar Acceso", command=self.guardar_usuario)
        self.btn_guardar.pack(pady=20)

        self.lbl_mensaje = ctk.CTkLabel(self.frame_form, text="", font=("Roboto", 12))
        self.lbl_mensaje.pack(pady=5)

    def crear_lista_usuarios(self):
        self.frame_lista = ctk.CTkFrame(self, fg_color="#f0f0f0")
        self.frame_lista.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

        ctk.CTkLabel(self.frame_lista, text="Usuarios Activos", font=("Roboto", 18, "bold"), text_color="black").pack(pady=(20, 10))

        self.caja_lista = ctk.CTkTextbox(self.frame_lista, width=300, font=("Courier", 13))
        self.caja_lista.pack(pady=10, padx=15, fill="both", expand=True)
        self.caja_lista.configure(state="disabled")

    def guardar_usuario(self):
        user = self.entrada_user.get()
        password = self.entrada_pass.get()
        rol = self.combo_rol.get()

        if not user or not password:
            self.lbl_mensaje.configure(text="Complete todos los campos.", text_color="red")
            return

        resultado = registrar_nuevo_usuario(user, password, rol)

        if resultado["exito"]:
            self.lbl_mensaje.configure(text=resultado["mensaje"], text_color="green")
            self.entrada_user.delete(0, 'end')
            self.entrada_pass.delete(0, 'end')
            self.actualizar_lista()
        else:
            self.lbl_mensaje.configure(text=resultado["mensaje"], text_color="red")

    def actualizar_lista(self):
        """Lee los datos quemados y actualiza la caja de texto"""
        usuarios_actuales = obtener_lista_usuarios()
        
        texto = ""
        for u in usuarios_actuales:
            estado = "Activo" if u["activo"] else "Inactivo"
            texto += f"ID: {u['id_usuario']} | {u['username']}\n"
            texto += f"Rol: {u['rol']}\n"
            texto += f"Estado: {estado}\n"
            texto += "-" * 30 + "\n"

        self.caja_lista.configure(state="normal")
        self.caja_lista.delete("0.0", "end")
        self.caja_lista.insert("0.0", texto)
        self.caja_lista.configure(state="disabled")