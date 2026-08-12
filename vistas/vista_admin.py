import customtkinter as ctk
from logica.logica_alertas import obtener_dashboard_alertas
from logica.logica_finanzas import generar_reporte_financiero
from vistas.vista_usuarios import VistaUsuarios
from vistas.vista_inventario import VistaInventario

class DashboardAdmin(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        # Configuración de la ventana principal del Admin
        self.title("Farmacentric - Panel de Administrador")
        self.geometry("900x600")
        self.minsize(800, 500)
        
        # Centrar la ventana
        # self.eval('tk::PlaceWindow . center')

        # Configurar el grid (sistema de cuadrícula) para dividir la pantalla
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1) # La columna 1 (centro) se expandirá

        self.crear_sidebar()
        self.crear_area_principal()
        
        # Cargar los datos lógicos al iniciar
        self.cargar_datos_dashboard()

    def crear_sidebar(self):
        """Crea el menú lateral izquierdo"""
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Empuja el botón de salir hacia abajo

        self.lbl_logo = ctk.CTkLabel(self.sidebar_frame, text="Farmacentric\nAdmin", font=("Roboto", 20, "bold"))
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.btn_inicio = ctk.CTkButton(self.sidebar_frame, text="Inicio (Dashboard)")
        self.btn_inicio.grid(row=1, column=0, padx=20, pady=10)

        # Cambia esta línea:
        self.btn_usuarios = ctk.CTkButton(self.sidebar_frame, text="Gestión de Usuarios", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.abrir_gestion_usuarios)
        self.btn_usuarios.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_inventario = ctk.CTkButton(self.sidebar_frame, text="Gestión de Inventario", fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), command=self.abrir_gestion_inventario)
        self.btn_inventario.grid(row=3, column=0, padx=20, pady=10)
        
        self.btn_salir = ctk.CTkButton(self.sidebar_frame, text="Cerrar Sesión", fg_color="#d32f2f", hover_color="#b71c1c", command=lambda: self.master.cerrar_sesion(self))
        self.btn_salir.grid(row=5, column=0, padx=20, pady=20)
        
    def abrir_gestion_usuarios(self):
        # Abre la ventana de usuarios encima del Dashboard
        VistaUsuarios(self)
        
    def abrir_gestion_inventario(self):
        # Abre la ventana de inventario encima del Dashboard
        VistaInventario(self)

    def crear_area_principal(self):
        """Crea el área central donde se muestra la información"""
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.lbl_bienvenida = ctk.CTkLabel(self.main_frame, text="Resumen General", font=("Roboto", 24, "bold"))
        self.lbl_bienvenida.pack(anchor="w", pady=(0, 20))

        # --- Tarjetas de Finanzas ---
        self.frame_finanzas = ctk.CTkFrame(self.main_frame)
        self.frame_finanzas.pack(fill="x", pady=(0, 20))
        
        self.lbl_titulo_finanzas = ctk.CTkLabel(self.frame_finanzas, text="Salud Financiera", font=("Roboto", 16, "bold"))
        self.lbl_titulo_finanzas.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.lbl_balance = ctk.CTkLabel(self.frame_finanzas, text="Cargando balance...", font=("Roboto", 14))
        self.lbl_balance.pack(anchor="w", padx=15, pady=(0, 10))

        # --- Tarjetas de Alertas de Inventario ---
        self.frame_alertas = ctk.CTkFrame(self.main_frame)
        self.frame_alertas.pack(fill="both", expand=True)
        
        self.lbl_titulo_alertas = ctk.CTkLabel(self.frame_alertas, text="Alertas Críticas de Inventario", font=("Roboto", 16, "bold"), text_color="#d32f2f")
        self.lbl_titulo_alertas.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Caja de texto donde mostraremos las alertas
        self.caja_alertas = ctk.CTkTextbox(self.frame_alertas, font=("Roboto", 13))
        self.caja_alertas.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def cargar_datos_dashboard(self):
        """Conecta la interfaz con la lógica que construimos antes"""
        # 1. Cargar Finanzas
        finanzas = generar_reporte_financiero()
        texto_finanzas = f"Balance Neto: C$ {finanzas['balance_neto']:,.2f}  |  Estado: {finanzas['estado_financiero']}"
        self.lbl_balance.configure(text=texto_finanzas)
        
        # 2. Cargar Alertas
        alertas = obtener_dashboard_alertas()
        texto_alertas = ""
        
        if alertas["alertas_stock"]:
            texto_alertas += "--- PRODUCTOS CON STOCK BAJO ---\n"
            for a in alertas["alertas_stock"]:
                texto_alertas += f"⚠️ {a['producto']}: Quedan {a['stock_actual']} (Mínimo: {a['stock_minimo']})\n"
            texto_alertas += "\n"
            
        if alertas["alertas_vencimiento"]:
            texto_alertas += "--- PRÓXIMOS A VENCER ---\n"
            for a in alertas["alertas_vencimiento"]:
                texto_alertas += f"📅 {a['producto']} (Lote: {a['lote']}) - {a['estado']}\n"
                
        if not texto_alertas:
            texto_alertas = "✅ Todo en orden. No hay alertas críticas en el inventario."
            
        self.caja_alertas.insert("0.0", texto_alertas)
        self.caja_alertas.configure(state="disabled") # Bloqueamos el texto para que el usuario no pueda borrarlo