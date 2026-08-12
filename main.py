import customtkinter as ctk
# Importamos la lógica que moviste a la nueva carpeta
from logica.logica_auth import iniciar_sesion
from vistas.vista_admin import DashboardAdmin
from vistas.vista_cajero import VistaCajero
from vistas.vista_rrhh import VistaRRHH

# 1. Configuración global de la estética (UI/UX)
ctk.set_appearance_mode("Light")  # "Light" ideal para sistemas de salud. "Dark" también disponible.
ctk.set_default_color_theme("blue")  # Colores de acento en azul marino

class AplicacionFarmacentric(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Farmacentric - Acceso al Sistema")
        self.geometry("400x500")
        self.resizable(False, False) # Evitamos que el usuario deforme la pantalla de login
        
        # Centrar la ventana en la pantalla
        self.eval('tk::PlaceWindow . center')

        self.crear_pantalla_login()

    def crear_pantalla_login(self):
        # Frame principal que contendrá los elementos (crea un efecto de tarjeta)
        self.frame_login = ctk.CTkFrame(self, width=320, height=400, corner_radius=15)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        self.lbl_titulo = ctk.CTkLabel(self.frame_login, text="Farmacentric", font=("Roboto", 28, "bold"))
        self.lbl_titulo.place(relx=0.5, rely=0.15, anchor="center")
        
        self.lbl_subtitulo = ctk.CTkLabel(self.frame_login, text="Sistema de Gestión Integral", font=("Roboto", 12), text_color="gray")
        self.lbl_subtitulo.place(relx=0.5, rely=0.22, anchor="center")

        # Campo de Usuario
        self.entrada_usuario = ctk.CTkEntry(self.frame_login, width=220, placeholder_text="Nombre de usuario")
        self.entrada_usuario.place(relx=0.5, rely=0.4, anchor="center")

        # Campo de Contraseña (con el atributo show="*" para ocultar el texto)
        self.entrada_password = ctk.CTkEntry(self.frame_login, width=220, placeholder_text="Contraseña", show="*")
        self.entrada_password.place(relx=0.5, rely=0.55, anchor="center")

        # Etiqueta para mostrar errores (invisible por defecto)
        self.lbl_error = ctk.CTkLabel(self.frame_login, text="", text_color="red", font=("Roboto", 10))
        self.lbl_error.place(relx=0.5, rely=0.68, anchor="center")

        # Botón de Inicio de Sesión
        self.btn_login = ctk.CTkButton(self.frame_login, text="Ingresar", width=220, font=("Roboto", 14, "bold"), command=self.validar_login)
        self.btn_login.place(relx=0.5, rely=0.8, anchor="center")

    def validar_login(self):
        """Esta función conecta la interfaz gráfica con tu carpeta de lógica"""
        # Obtenemos lo que el usuario escribió
        user = self.entrada_usuario.get()
        password = self.entrada_password.get()

        # Limpiamos mensajes de error previos
        self.lbl_error.configure(text="")

        # Validamos que no estén vacíos
        if not user or not password:
            self.lbl_error.configure(text="Por favor, complete todos los campos.")
            return

        # ¡AQUÍ ESTÁ LA MAGIA! Llamamos a tu archivo logica_auth.py
        respuesta = iniciar_sesion(user, password)

        if respuesta["exito"]:
            self.lbl_error.configure(text=respuesta["mensaje"], text_color="green")
            rol_usuario = respuesta["datos_usuario"]["rol"]
            
            # Si es administrador, abrimos su Dashboard
            if rol_usuario == "Administrador":
                self.withdraw() # Ocultamos la ventana de Login
                ventana_admin = DashboardAdmin(self) # Creamos la ventana de Admin
                
               # ¡CORRECCIÓN!: Si el usuario le da a la 'X' de la ventana, cerramos toda la aplicación
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
                print(f"La vista para el rol {rol_usuario} aún no está construida.")
                
        else:
            self.lbl_error.configure(text=respuesta["mensaje"], text_color="red")

    def cerrar_sesion(self, ventana_top):
        """Cierra el dashboard y vuelve a mostrar el login limpio"""
        ventana_top.destroy()
        self.entrada_usuario.delete(0, 'end')
        self.entrada_password.delete(0, 'end')
        self.lbl_error.configure(text="")
        self.deiconify() # Vuelve a mostrar el login

# Ejecutamos la aplicación
if __name__ == "__main__":
    app = AplicacionFarmacentric()
    app.mainloop()