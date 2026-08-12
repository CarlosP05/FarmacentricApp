import customtkinter as ctk
from logica.logica_inventario import registrar_nuevo_producto, registrar_nuevo_lote

class VistaInventario(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Farmacentric - Ingreso de Inventario")
        self.geometry("800x550")
        self.minsize(750, 500)
        self.grab_set() # Bloquea la ventana principal hasta que se cierre esta

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1) # Panel de Catálogo
        self.grid_columnconfigure(1, weight=1) # Panel de Lotes

        self.crear_panel_catalogo()
        self.crear_panel_lotes()

    def crear_panel_catalogo(self):
        """Formulario para registrar un NUEVO TIPO de medicamento"""
        self.frame_cat = ctk.CTkFrame(self)
        self.frame_cat.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        ctk.CTkLabel(self.frame_cat, text="1. Nuevo en Catálogo", font=("Roboto", 18, "bold")).pack(pady=(20, 15))

        self.ent_nombre = ctk.CTkEntry(self.frame_cat, placeholder_text="Nombre (Ej. Ibuprofeno 400mg)", width=250)
        self.ent_nombre.pack(pady=10)

        categorias = ["Venta Libre", "Antibiótico", "Controlado", "Material Médico"]
        self.combo_cat = ctk.CTkComboBox(self.frame_cat, values=categorias, width=250)
        self.combo_cat.pack(pady=10)

        self.ent_precio = ctk.CTkEntry(self.frame_cat, placeholder_text="Precio de Venta (C$)", width=250)
        self.ent_precio.pack(pady=10)

        self.ent_stock_min = ctk.CTkEntry(self.frame_cat, placeholder_text="Stock Mínimo (Alerta)", width=250)
        self.ent_stock_min.pack(pady=10)

        self.chk_receta = ctk.CTkCheckBox(self.frame_cat, text="¿Requiere Receta Médica?")
        self.chk_receta.pack(pady=15)

        self.btn_guardar_cat = ctk.CTkButton(self.frame_cat, text="Crear Producto", command=self.guardar_producto)
        self.btn_guardar_cat.pack(pady=10)

        self.lbl_msg_cat = ctk.CTkLabel(self.frame_cat, text="", font=("Roboto", 12))
        self.lbl_msg_cat.pack(pady=5)

    def crear_panel_lotes(self):
        """Formulario para registrar las CAJAS FÍSICAS (Lotes)"""
        self.frame_lote = ctk.CTkFrame(self, fg_color="#f0f0f0")
        self.frame_lote.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

        ctk.CTkLabel(self.frame_lote, text="2. Ingreso de Lote (Cajas)", font=("Roboto", 18, "bold"), text_color="black").pack(pady=(20, 15))

        self.ent_id_prod = ctk.CTkEntry(self.frame_lote, placeholder_text="ID del Producto (Ej. 1001)", width=250)
        self.ent_id_prod.pack(pady=10)

        self.ent_id_lote = ctk.CTkEntry(self.frame_lote, placeholder_text="Código de Lote (Ej. L-001)", width=250)
        self.ent_id_lote.pack(pady=10)

        self.ent_cantidad = ctk.CTkEntry(self.frame_lote, placeholder_text="Cantidad (Cajas)", width=250)
        self.ent_cantidad.pack(pady=10)

        self.ent_fecha = ctk.CTkEntry(self.frame_lote, placeholder_text="Vencimiento (YYYY-MM-DD)", width=250)
        self.ent_fecha.pack(pady=10)

        self.btn_guardar_lote = ctk.CTkButton(self.frame_lote, text="Registrar Lote", fg_color="green", hover_color="darkgreen", command=self.guardar_lote)
        self.btn_guardar_lote.pack(pady=20)

        self.lbl_msg_lote = ctk.CTkLabel(self.frame_lote, text="", font=("Roboto", 12))
        self.lbl_msg_lote.pack(pady=5)

    def guardar_producto(self):
        nombre = self.ent_nombre.get()
        categoria = self.combo_cat.get()
        precio_str = self.ent_precio.get()
        stock_min_str = self.ent_stock_min.get()
        requiere_receta = bool(self.chk_receta.get())

        if not nombre or not precio_str or not stock_min_str:
            self.lbl_msg_cat.configure(text="Complete todos los campos de texto.", text_color="red")
            return

        try:
            precio = float(precio_str)
            stock_min = int(stock_min_str)
            
            resultado = registrar_nuevo_producto(nombre, categoria, precio, stock_min, requiere_receta)
            
            if resultado["exito"]:
                self.lbl_msg_cat.configure(text=resultado["mensaje"], text_color="green")
                # Limpiamos los campos
                self.ent_nombre.delete(0, 'end')
                self.ent_precio.delete(0, 'end')
                self.ent_stock_min.delete(0, 'end')
            else:
                self.lbl_msg_cat.configure(text=resultado["mensaje"], text_color="red")
                
        except ValueError:
            self.lbl_msg_cat.configure(text="Precio y Stock deben ser números válidos.", text_color="red")

    def guardar_lote(self):
        id_prod_str = self.ent_id_prod.get()
        id_lote = self.ent_id_lote.get()
        cantidad_str = self.ent_cantidad.get()
        fecha = self.ent_fecha.get()

        if not id_prod_str or not id_lote or not cantidad_str or not fecha:
            self.lbl_msg_lote.configure(text="Complete todos los campos del lote.", text_color="red")
            return

        try:
            id_prod = int(id_prod_str)
            cantidad = int(cantidad_str)
            
            # Nota: En un sistema en producción se validaría el formato de la fecha YYYY-MM-DD
            resultado = registrar_nuevo_lote(id_prod, id_lote, cantidad, fecha)
            
            if resultado["exito"]:
                self.lbl_msg_lote.configure(text=resultado["mensaje"], text_color="green")
                # Limpiamos
                self.ent_id_prod.delete(0, 'end')
                self.ent_id_lote.delete(0, 'end')
                self.ent_cantidad.delete(0, 'end')
                self.ent_fecha.delete(0, 'end')
                
                # Actualizamos el dashboard que está de fondo
                self.master.cargar_datos_dashboard()
            else:
                self.lbl_msg_lote.configure(text=resultado["mensaje"], text_color="red")
                
        except ValueError:
            self.lbl_msg_lote.configure(text="ID Producto y Cantidad deben ser números enteros.", text_color="red")