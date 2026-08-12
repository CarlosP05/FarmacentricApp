import customtkinter as ctk
from logica.logica_pos import calcular_venta, procesar_venta
from logica.logica_finanzas import registrar_ingreso_venta

class VistaCajero(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.title("Farmacentric - Punto de Venta (POS)")
        self.geometry("900x600")
        self.minsize(800, 500)
        

        # Variables de estado
        self.carrito = [] # Aquí guardaremos los productos antes de cobrar
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1) # Panel Izquierdo
        self.grid_columnconfigure(1, weight=1) # Panel Derecho (Ticket)

        self.crear_panel_izquierdo()
        self.crear_panel_derecho()

    def crear_panel_izquierdo(self):
        """Controles para buscar y agregar medicamentos"""
        self.panel_izq = ctk.CTkFrame(self)
        self.panel_izq.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        ctk.CTkLabel(self.panel_izq, text="Agregar Producto", font=("Roboto", 20, "bold")).pack(pady=(20, 10))

        # Inputs
        self.entrada_id = ctk.CTkEntry(self.panel_izq, placeholder_text="ID del Producto (Ej. 1001)", width=250)
        self.entrada_id.pack(pady=10)

        self.entrada_cantidad = ctk.CTkEntry(self.panel_izq, placeholder_text="Cantidad", width=250)
        self.entrada_cantidad.pack(pady=10)

        # Botones de Acción
        self.btn_agregar = ctk.CTkButton(self.panel_izq, text="Añadir al Carrito", command=self.agregar_al_carrito)
        self.btn_agregar.pack(pady=15)
        
        self.btn_limpiar = ctk.CTkButton(self.panel_izq, text="Limpiar Carrito", fg_color="gray", command=self.limpiar_carrito)
        self.btn_limpiar.pack(pady=5)

        # Feedback de errores
        self.lbl_mensaje = ctk.CTkLabel(self.panel_izq, text="", text_color="red")
        self.lbl_mensaje.pack(pady=20)
        
        # Botón de Salir (Misma lógica que el admin)
        self.btn_salir = ctk.CTkButton(self.panel_izq, text="Cerrar Sesión", fg_color="#d32f2f", hover_color="#b71c1c", command=lambda: self.master.cerrar_sesion(self))
        self.btn_salir.pack(side="bottom", pady=20)

    def crear_panel_derecho(self):
        """Muestra el ticket de compra y el botón de cobrar"""
        self.panel_der = ctk.CTkFrame(self, fg_color="#f0f0f0")
        self.panel_der.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

        ctk.CTkLabel(self.panel_der, text="Ticket de Venta", font=("Roboto", 20, "bold"), text_color="black").pack(pady=(20, 10))

        # Pantalla del Ticket
        self.caja_ticket = ctk.CTkTextbox(self.panel_der, width=350, height=300, font=("Courier", 14))
        self.caja_ticket.pack(pady=10, padx=20, fill="both", expand=True)
        self.caja_ticket.insert("0.0", "El carrito está vacío.")
        self.caja_ticket.configure(state="disabled")

        # Total a pagar
        self.lbl_total = ctk.CTkLabel(self.panel_der, text="TOTAL: C$ 0.00", font=("Roboto", 24, "bold"), text_color="green")
        self.lbl_total.pack(pady=10)

        # Botón de Cobrar
        self.btn_cobrar = ctk.CTkButton(self.panel_der, text="PROCESAR PAGO", font=("Roboto", 16, "bold"), height=50, fg_color="green", hover_color="darkgreen", command=self.cobrar)
        self.btn_cobrar.pack(pady=(0, 20), padx=20, fill="x")

    def agregar_al_carrito(self):
        self.lbl_mensaje.configure(text="")
        id_prod = self.entrada_id.get()
        cant = self.entrada_cantidad.get()

        if not id_prod.isdigit() or not cant.isdigit():
            self.lbl_mensaje.configure(text="Por favor, ingrese solo números.")
            return

        # Agregamos al carrito temporal
        self.carrito.append({"id_producto": int(id_prod), "cantidad": int(cant)})
        self.actualizar_ticket()
        
        # Limpiar inputs
        self.entrada_id.delete(0, 'end')
        self.entrada_cantidad.delete(0, 'end')

    def actualizar_ticket(self):
        self.caja_ticket.configure(state="normal")
        self.caja_ticket.delete("0.0", "end")
        
        if not self.carrito:
            self.caja_ticket.insert("0.0", "El carrito está vacío.")
            self.lbl_total.configure(text="TOTAL: C$ 0.00")
            self.caja_ticket.configure(state="disabled")
            return

        # Usamos la lógica de POS para previsualizar la venta
        resultado = calcular_venta(self.carrito)
        
        texto_ticket = "--- DETALLE DE COMPRA ---\n\n"
        for item in resultado["detalle"]:
            texto_ticket += f"{item['cantidad']}x {item['producto'][:15]}... \n   Subtotal: C${item['subtotal']:.2f}\n"
            
        if resultado["pedir_recetas_para"]:
            texto_ticket += "\n⚠️ SOLICITAR RECETA PARA:\n"
            for med in resultado["pedir_recetas_para"]:
                texto_ticket += f"- {med}\n"

        self.caja_ticket.insert("0.0", texto_ticket)
        self.lbl_total.configure(text=f"TOTAL: C$ {resultado['total_pagar']:,.2f}")
        self.caja_ticket.configure(state="disabled")

    def limpiar_carrito(self):
        self.carrito = []
        self.actualizar_ticket()
        self.lbl_mensaje.configure(text="Carrito limpiado.", text_color="blue")

    def cobrar(self):
        if not self.carrito:
            self.lbl_mensaje.configure(text="No hay productos para cobrar.")
            return

        # Ejecutamos la venta real (Descuenta inventario)
        resultado = procesar_venta(self.carrito)
        
        if resultado["exito"]:
            # Registramos el dinero en las finanzas
            registrar_ingreso_venta(resultado["total_cobrado"])
            
            self.limpiar_carrito()
            self.lbl_mensaje.configure(text="✅ Venta procesada exitosamente.", text_color="green")
        else:
            self.lbl_mensaje.configure(text=resultado["mensaje"], text_color="red")