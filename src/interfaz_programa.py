import customtkinter as ctk, logging, tkinter as tk, webbrowser
from tkinter import filedialog, ttk
from PIL import Image

import tkinter.messagebox as msg

from core.PROTECCION import Proteccion
from core.LEER_DB import Leer_crear_db

from core.RUTAS import *

class PanelSistema(ctk.CTkFrame):
    def __init__(self, parent, nombre_user, ultima_fecha_acceso):
        super().__init__(parent)
        ancho = 900
        alto = 700
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.master.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.master.resizable(True, True)
        self.configure(fg_color="#1C1C1C")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        self.nombre_user = nombre_user
        self.ultima_fecha_acceso = ultima_fecha_acceso
        
        self.frames_iniciales()
        self.widget_interfaz_superior()
        self.widget_interfaz_medio()
        self.widget_interfaz_db()
        self.insertar_datos_db()
        self.interfaz_actividad_reciente()
        
    def frames_iniciales(self):

        self.frame_linea_superior = ctk.CTkFrame(self, fg_color="#1C1C1C")
        self.frame_linea_superior.grid(row = 0, column = 0, padx=0, pady=2, sticky="we")
        self.frame_linea_superior.grid_columnconfigure(0, weight=1)
        # self.frame_linea_superior.grid_rowconfigure(2, weight=1)

        #frame de titulo
        self.frame_titulo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_titulo.grid(row = 2, column = 0, pady=5)

        #frame seleccion ocultar - desocultar
        self.frame_protecciones = ctk.CTkFrame (self, fg_color="transparent")
        self.frame_protecciones.grid(row = 3, column = 0, padx=10, sticky="we")
        self.frame_protecciones.grid_columnconfigure(0, weight=1)
        self.frame_protecciones.grid_columnconfigure(1, weight=1)

        #frame tabla db
        self.frame_contenedor_db = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_contenedor_db.grid(row = 4, column = 0, padx=10, sticky="snwe")
        self.frame_contenedor_db.grid_columnconfigure(0, weight=1)
        self.frame_contenedor_db.grid_rowconfigure(1, weight=1)
        
        self.frame_actividad = ctk.CTkFrame(self, fg_color="transparent",border_width=1,border_color="#3C3C3C")
        self.frame_actividad.grid(row = 5, column = 0, padx=10, pady=(0,20), sticky="snwe")
        self.frame_actividad.grid_columnconfigure(1, weight=1)

        
    def widget_interfaz_superior(self):
        #barner superior
        
        label_user_login = ctk.CTkLabel(self.frame_linea_superior, text=f"Usuario: {self.nombre_user} Ultimo Acceso: {self.ultima_fecha_acceso}", font=("Bahnschrift", 13, "bold"), fg_color="transparent",text_color="#E7E7E7",anchor="e")
        label_user_login.grid(row = 0, column = 0, padx=10, pady=0, sticky="ew")
        linea_label = ctk.CTkFrame(self.frame_linea_superior, fg_color="#242424", height=2) 
        linea_label.grid(row = 1, column = 0, padx=0, pady=5, sticky="eswn")
        
        logo_acerca_de = ctk.CTkImage (light_image=Image.open(ruta_logo_acerca_de), size=(15,15))
        label_acerca_de = ctk.CTkLabel(self.frame_linea_superior, image=logo_acerca_de, text="", fg_color="transparent",text_color="#E7E7E7",anchor="w", cursor = "hand2")
        label_acerca_de.grid(row = 0, column = 1, padx =(0,10))
        label_acerca_de.bind("<Button-1>", self._interfaz_acerca_de)
        
        
        #barner logotipo
        logo = ctk.CTkImage (light_image=Image.open(ruta_logo_png), size=(130,90))
        label_logo = ctk.CTkLabel(self, image=logo, text="")
        label_logo.grid(row = 1, column = 0, padx=10, pady=0, sticky="ew")
        
        #widget que estan en el frame frame_titulo
        titulo1 = ctk.CTkLabel(self.frame_titulo, text="ORS", font=("Bahnschrift", 30, "bold"))
        titulo1.grid(row = 0, column = 0, pady=(5,3))
        
        titulo2 = ctk.CTkLabel(self.frame_titulo, text="4", font=("Bahnschrift", 30, "bold"), text_color="red")
        titulo2.grid(row = 0, column =1, pady=(5,3))
        
        titulo3 = ctk.CTkLabel(self.frame_titulo, text="GHOST", font=("Bahnschrift", 30, "bold"))
        titulo3.grid(row = 0, column = 2, pady=(5,3))

        
    def widget_interfaz_medio (self):
        #frame contenedor
        self.frame_ocultar = ctk.CTkFrame(self.frame_protecciones, fg_color="#171616",border_color="#3C3C3C", border_width=1)
        self.frame_ocultar.grid(row = 0, column = 0, padx=(10,5), pady=0, sticky="we")
        self.frame_ocultar.grid_columnconfigure(0, weight=1)

        #frame contenedor titulo
        frame_titulo_protec = ctk.CTkFrame(self.frame_ocultar, fg_color="transparent") #Frame que contiene el titulo para que se vea el borde del contenedor
        frame_titulo_protec.grid(row = 0, column = 0, padx=5, pady=5, sticky="ew")
        
        logo_carpeta_oculta = ctk.CTkImage (light_image=Image.open(ruta_logo_carpeta_oculta), size=(30, 28))

        label_titulo_protec = ctk.CTkLabel(frame_titulo_protec, image=logo_carpeta_oculta, text=" Proteger carpetas o archivos", font=("Arial", 15, "bold"), text_color="#D0CFCF", compound="left", anchor="w")
        label_titulo_protec.grid(row = 0, column = 0, padx=5, pady=10, sticky="ew")

        #frame contenedor seleccion
        frame_seleccion = ctk.CTkFrame(self.frame_ocultar, fg_color="transparent", border_width=1, border_color="#3C3C3C") #Frame que contiene el titulo para que se vea el borde del contenedor
        frame_seleccion.grid(row = 1, column = 0, padx=5, sticky="ew")
        frame_seleccion.grid_columnconfigure(0, weight=1)

        auto = ctk.StringVar(value="Tipo")
        self.select_option = ctk.CTkOptionMenu(frame_seleccion, values=["Carpeta", "Archivo"], variable=auto, font=("Arial", 15), text_color="#E7E7E7", fg_color="#1A1818",dropdown_fg_color="#1A1818", dropdown_text_color="#E7E7E7", dropdown_hover_color="#2A2929", button_color="#1A1818", button_hover_color="#501509",width=50, command=self.select_ruta)
        self.select_option.grid(row = 0, column = 1, padx=(0,5), pady=5)   

        self.entry_ruta_select = ctk.CTkEntry(frame_seleccion, placeholder_text="Esperando selección...", font=("Arial", 15), text_color="#E7E7E7", fg_color="#1A1818", border_width=1, border_color="#1F1E1E")
        self.entry_ruta_select.grid(row = 0, column = 0, padx=5, pady=5, sticky="ew")
        self.entry_ruta_select.configure(state="disabled")
        
        # self.boton_seleccionar_o = ctk.CTkButton(frame_seleccion, text="Seleccionar", font=("Arial", 15, "bold"), width= 60, fg_color="#661909",hover_color="#501509", text_color="#D0CFCF", command=self.select_ruta)
        # self.boton_seleccionar_o.grid(row = 0, column = 2, padx=(0,5), sticky="ew")

        self.boton_proteger = ctk.CTkButton(self.frame_ocultar, text="Aplicar proteccion", font=("Arial", 15, "bold"),  width= 60,  fg_color="#661909", hover_color="#501509", text_color="#D0CFCF",height=30, state="disabled", command=self.aplicar_proteccion)
        self.boton_proteger.grid(row = 2, column = 0, columnspan=2, pady=20)



        self.frame_desocultar = ctk.CTkFrame(self.frame_protecciones, fg_color="#171616",border_color="#3C3C3C", border_width=1)
        self.frame_desocultar.grid(row = 0, column = 1, padx=(10,5), pady=0, sticky="we")
        self.frame_desocultar.grid_columnconfigure(0, weight=1)

        frame_titulo_desprotec = ctk.CTkFrame(self.frame_desocultar, fg_color="transparent") #Frame que contiene el titulo para que se vea el borde del contenedor
        frame_titulo_desprotec.grid(row = 0, column = 0, padx=5, pady=5, sticky="ew")
        
        logo_carpeta_desoculta = ctk.CTkImage (light_image=Image.open(ruta_logo_desocultar), size=(30, 28))

        label_titulo_desprotec = ctk.CTkLabel(frame_titulo_desprotec, image=logo_carpeta_desoculta, text=" Recuperacion Manual", font=("Arial", 15, "bold"), text_color="#D0CFCF", compound="left", anchor="w")
        label_titulo_desprotec.grid(row = 0, column = 0, padx=5, pady=10, sticky="ew")


        #frame contenedor seleccion
        frame_seleccion_2 = ctk.CTkFrame(self.frame_desocultar, fg_color="transparent", border_width=1, border_color="#3C3C3C") #Frame que contiene el titulo para que se vea el borde del contenedor
        frame_seleccion_2.grid(row = 1, column = 0, padx=5, sticky="ew")
        frame_seleccion_2.grid_columnconfigure(0, weight=1)


        # auto_d = ctk.StringVar(value="Tipo")
        # self.select_option_d = ctk.CTkOptionMenu(frame_seleccion_2, values=["Carpeta origen"], variable=auto_d, font=("Arial", 15), text_color="#E7E7E7", fg_color="#1A1818",dropdown_fg_color="#1A1818", dropdown_text_color="#E7E7E7", dropdown_hover_color="#2A2929", button_color="#1A1818", button_hover_color="#501509",width=50, command=self.select_ruta_d)
        # self.select_option_d.grid(row = 0, column = 1, padx=(0,5), pady=5)   

        self.entry_ruta_manual = ctk.CTkEntry(frame_seleccion_2, placeholder_text="Esperando selección...", font=("Arial", 15), text_color="#E7E7E7", fg_color="#1A1818", border_width=1, border_color="#1F1E1E")
        self.entry_ruta_manual.grid(row = 0, column = 0, padx=5, pady=5, sticky="ew")
        self.entry_ruta_manual.configure(state="disabled")
        self.boton_desproteger = ctk.CTkButton(self.frame_desocultar, text="Seleccionar ubicación original", font=("Arial", 15, "bold"),  width= 60,  fg_color="#661909", hover_color="#501509", text_color="#D0CFCF",height=30, command=self._interfaz_recuperacion_manual)
        self.boton_desproteger.grid(row = 2, column = 0, columnspan=2, pady=20)

    def select_ruta (self, opcion):
        """
        Selecciona la ruta del archivo o carpeta a proteger
        """
        
        opcion = self.select_option.get()
        self.ruta_select = ""
        if "Archivo" == opcion:
            self.ruta_select = filedialog.askopenfilenames()
            self.entry_ruta_select.configure(state="normal")
            self.entry_ruta_select.delete(0,"end")
            if self.ruta_select:
                self.entry_ruta_select.insert(0,(self.ruta_select))
                self.boton_proteger.configure(state="normal")
            else:
                self.entry_ruta_select.insert(0,"Esperando selección...")
                self.boton_proteger.configure(state="disabled")
            self.entry_ruta_select.configure(state="readonly")


        elif "Carpeta" == opcion:
            self.ruta_select = filedialog.askdirectory()
            self.entry_ruta_select.configure(state="normal")
            self.entry_ruta_select.delete(0,"end")
            
            if self.ruta_select:
                self.entry_ruta_select.insert(0,(self.ruta_select))
                self.boton_proteger.configure(state="normal")
            else:
                self.entry_ruta_select.insert(0,"Esperando selección...")
                self.boton_proteger.configure(state="disabled")
            self.entry_ruta_select.configure(state="readonly")

    def aplicar_proteccion (self):
        """
        Aplica la proteccion a la ruta seleccionada y envia la informacion para actualizar la actividad
        """
        
        
        self.errores_protec = 0
        self.protec_no_permitidos = False
        proteccion = Proteccion()
        
        procesados = 0
        if isinstance(self.ruta_select, tuple):
            for ruta in self.ruta_select:
                proteccion_aplicada =proteccion.aplicar_proteccion(ruta)

                if proteccion_aplicada:
                    self.boton_proteger.configure(state="disabled")
                    self.insertar_datos_db()
                    procesados += 1

                elif proteccion_aplicada is False:
                    self.errores_protec += 1

                else:
                    self.protec_no_permitidos = True

        else:
            proteccion_aplicada =proteccion.aplicar_proteccion(self.ruta_select)
            
            if proteccion_aplicada:
                self.boton_proteger.configure(state="disabled")
                self.insertar_datos_db()
                procesados += 1

            elif proteccion_aplicada is False:
                self._interfaz_error()

            else:
                self._interfaz_bloqueo()

        if self.errores_protec > 0:
            self._interfaz_error()
        
        if self.protec_no_permitidos:
            self._interfaz_bloqueo()
            
        if procesados == 1:
            if isinstance(self.ruta_select, tuple):
                actividad = f" ✔ Proteccion aplicada a {self.ruta_select[0]} "
                self._actualizar_actividad(actividad)
            else:
                actividad = f" ✔ Proteccion aplicada a {self.ruta_select} "
                self._actualizar_actividad(actividad)

        elif procesados > 1:
            actividad = f" ✔ Proteccion aplicada a {procesados} archivos. Los más recientes aparecen al inicio de la lista."
            self._actualizar_actividad(actividad)

    def _interfaz_error (self):
        """
        Metodo que muestra cuando hay un error al ocultar o desocultar
        """
        ventana_error = ctk.CTkToplevel(self)
        ventana_error.title("Error")
        ventana_error.geometry("410x180")
        ventana_error.resizable(False, False)
        
        ventana_error.update_idletasks()  

        ancho = ventana_error.winfo_width()  
        alto = ventana_error.winfo_height()  
        
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
        ventana_error.geometry(f"+{x}+{y}")

        ventana_error.lift()
        ventana_error.grab_set()
        ventana_error.bind("<Escape>", lambda event: ventana_error.destroy())
        
        icono = tk.PhotoImage(file=ruta_logo_png)
        ventana_error.icono_ref = icono
        ventana_error.after(200, lambda: ventana_error.iconphoto(False, ventana_error.icono_ref))


        frame_error = ctk.CTkFrame(ventana_error, fg_color="transparent")
        frame_error.pack(padx = 2, pady = (5,10), fill = "both", expand=True)
        
        logo_error = ctk.CTkImage (light_image=Image.open(ruta_logo_error), size=(30, 30))
        label_logo_error = ctk.CTkLabel (frame_error, image=logo_error, text="",)
        label_logo_error.grid(row=0, column=0, padx=(18,10), sticky="ws")

        label_msj_error = ctk.CTkLabel (frame_error, text=f"No se pudo completar la operación en {self.errores_protec} archivos.", font=("Bahnschrift", 14,"bold" ), text_color="#CF4343",)
        label_msj_error.grid(row=0, column=1, pady=3, sticky="w")
        label_msj_error2 = ctk.CTkLabel (frame_error, text="Posibles causas:", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error2.grid(row=1, column=1, columnspan=2, sticky="ws")
        label_msj_error3 = ctk.CTkLabel (frame_error, text="     - El archivo está en uso", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error3.grid(row=2, column=1, columnspan=2, sticky="ws")
        label_msj_error4 = ctk.CTkLabel (frame_error, text="     - No tienes permisos suficientes", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error4.grid(row=3, column=1, columnspan=2, sticky="ws")
        label_msj_error5 = ctk.CTkLabel (frame_error, text="     - La ruta no es válida", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error5.grid(row=4, column=1, columnspan=2, sticky="ws")
        label_msj_error6 = ctk.CTkLabel (frame_error, text="Intentalo nuevamente", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error6.grid(row=5, column=1, columnspan=2, sticky="ws")
        
    def _interfaz_bloqueo (self):
        """
        Metodo que muestra un error al ocultar archivos no permitidos
        """
        ventana_error = ctk.CTkToplevel(self)
        ventana_error.title("Error")
        ventana_error.geometry("420x100")
        ventana_error.resizable(False, False)
        
        ventana_error.update_idletasks()  

        ancho = ventana_error.winfo_width()  
        alto = ventana_error.winfo_height()  
        
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
        ventana_error.geometry(f"+{x}+{y}")

        ventana_error.lift()
        ventana_error.grab_set()
        ventana_error.bind("<Escape>", lambda event: ventana_error.destroy())
        
        icono = tk.PhotoImage(file=ruta_logo_png)
        ventana_error.icono_ref = icono
        ventana_error.after(200, lambda: ventana_error.iconphoto(False, ventana_error.icono_ref))

        frame_error = ctk.CTkFrame(ventana_error, fg_color="transparent")
        frame_error.pack(padx = 2, pady = (5,10), fill = "both", expand=True)
        
        logo_error = ctk.CTkImage (light_image=Image.open(ruta_logo_alerta), size=(30, 30))
        label_logo_error = ctk.CTkLabel (frame_error, image=logo_error, text="",)
        label_logo_error.grid(row=0, column=0, padx=(18,10), sticky="ws")

        label_msj_error = ctk.CTkLabel (frame_error, text="Operación Bloqueada.", font=("Bahnschrift", 14,"bold" ), text_color="#CF4343",)
        label_msj_error.grid(row=0, column=1, pady=3, sticky="w")
        label_msj_error2 = ctk.CTkLabel (frame_error, text="No se permite ocultar archivos o carpetas del sistema.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error2.grid(row=1, column=1, columnspan=2, sticky="ws")
        label_msj_error3 = ctk.CTkLabel (frame_error, text="Esta acción podría afectar la estabilidad del sistema.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error3.grid(row=2, column=1, columnspan=2, sticky="ws")


    def _interfaz_recuperacion_manual (self):
        """
        Metodo que muestra un msj al realizar recuperacion manual
        """
        self.ventana_msj = ctk.CTkToplevel(self)
        self.ventana_msj.title("Error")
        self.ventana_msj.geometry("550x200")
        self.ventana_msj.resizable(False, False)
        
        self.ventana_msj.update_idletasks()  

        ancho = self.ventana_msj.winfo_width()  
        alto = self.ventana_msj.winfo_height()  
        
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
        self.ventana_msj.geometry(f"+{x}+{y}")

        self.ventana_msj.lift()
        self.ventana_msj.grab_set()
        self.ventana_msj.bind("<Escape>", lambda event: self.ventana_msj.destroy())
        
        icono = tk.PhotoImage(file=ruta_logo_png)
        self.ventana_msj.icono_ref = icono
        self.ventana_msj.after(200, lambda: self.ventana_msj.iconphoto(False, self.ventana_msj.icono_ref))

        frame_msj = ctk.CTkFrame(self.ventana_msj, fg_color="transparent")
        frame_msj.pack(padx = 2, pady = (5,10), fill = "both", expand=True)

        logo_advertencia = ctk.CTkImage (light_image=Image.open(ruta_logo_alerta), size=(25, 22))
        label_logo_advertencia = ctk.CTkLabel (frame_msj, image=logo_advertencia, text="",)
        label_logo_advertencia.grid(row=0, column=0, padx=(18,10), sticky="ws")

        label_msj_error = ctk.CTkLabel (frame_msj, text=f"Modo de recuperación manual archivos.", font=("Bahnschrift", 14,"bold" ), text_color="#DCAA21",)
        label_msj_error.grid(row=0, column=1, pady=3, sticky="w")
        label_msj_error2 = ctk.CTkLabel (frame_msj, text="Se iniciará la recuperación manual de elementos ocultos.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error2.grid(row=1, column=1, columnspan=2, sticky="ws")
        label_msj_error3 = ctk.CTkLabel (frame_msj, text=" - No se utilizará el registro de la aplicación", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error3.grid(row=2, column=1, columnspan=2, sticky="ws")
        label_msj_error4 = ctk.CTkLabel (frame_msj, text=" - Se restaurarán los elementos encontrados en la ubicación seleccionada", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error4.grid(row=3, column=1, columnspan=2, sticky="ws")
        label_msj_error5 = ctk.CTkLabel (frame_msj, text="  - Selecciona la ubicación original donde se ocultaron los archivos", font=("Bahnschrift", 14,"bold"), text_color="#E8E8E8", anchor="n")
        label_msj_error5.grid(row=4, column=1, columnspan=2, sticky="ws")
        
        boton_ok = ctk.CTkButton (frame_msj, text="Aceptar ", font=("Bahnschrift", 12, "bold"), fg_color="#661909", hover_color="#501509", command= self.select_recuperacion_manual)
        boton_ok.grid(row=5, column=1, columnspan=2, padx=5, pady=(5,0),)

    def select_recuperacion_manual (self):
        """
        EJECUTA LA RECUPERACION MANUAL Y CIERRA LA VENTANA DE INTERFAZ RECUPERACION MANUAL 
        """
        self.ventana_msj.destroy()
        self.ruta_manual = ""
        
        self.ruta_manual = filedialog.askdirectory()
        
        if self.ruta_manual:
            self.entry_ruta_manual.configure(state="normal")
            self.entry_ruta_manual.delete(0,"end")
            self.entry_ruta_manual.insert(0,(self.ruta_manual))
            self.entry_ruta_manual.configure(state="readonly")

        else:
            self.entry_ruta_manual.configure(state="normal")
            self.entry_ruta_manual.delete(0,"end")
            self.entry_ruta_manual.insert(0,"Esperando selección...")
            self.entry_ruta_manual.configure(state="readonly")

            return
        
        proteccion = Proteccion()
        existe_carpeta_baul = proteccion._buscar_carpetas_baul(self.ruta_manual)
        if not existe_carpeta_baul:
            self._interfaz_carpeta_baul_no_existe()
            return
        
        proteccion._desproteger_carpeta()
        proteccion.actualizar_db()
        self.insertar_datos_db()
        msj = " ✔ Restauración completada. Se desprotegieron todos los elementos encontrados en la ruta seleccionada."
        self._actualizar_actividad(msj)


    def _interfaz_carpeta_baul_no_existe (self):
        
        """
        Metodo que muestra cuando no se encuentra la carpeta baul
        """
        ventana_error = ctk.CTkToplevel(self)
        ventana_error.title("Error")
        ventana_error.geometry("575x175")
        ventana_error.resizable(False, False)
        
        ventana_error.update_idletasks()  

        ancho = ventana_error.winfo_width()  
        alto = ventana_error.winfo_height()  
        
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
        ventana_error.geometry(f"+{x}+{y}")

        ventana_error.lift()
        ventana_error.grab_set()
        ventana_error.bind("<Escape>", lambda event: ventana_error.destroy())
        
        icono = tk.PhotoImage(file=ruta_logo_png)
        ventana_error.icono_ref = icono
        ventana_error.after(200, lambda: ventana_error.iconphoto(False, ventana_error.icono_ref))

        frame_error = ctk.CTkFrame(ventana_error, fg_color="transparent")
        frame_error.pack(padx = 2, pady = (5,10), fill = "both", expand=True)
        
        logo_error = ctk.CTkImage (light_image=Image.open(ruta_logo_error), size=(30, 30))
        label_logo_error = ctk.CTkLabel (frame_error, image=logo_error, text="",)
        label_logo_error.grid(row=0, column=0, padx=(18,10), sticky="ws")

        label_msj_error = ctk.CTkLabel (frame_error, text=f"Error al restaurar.", font=("Bahnschrift", 20,"bold" ), text_color="#CF4343",)
        label_msj_error.grid(row=0, column=1, pady=3, sticky="w")
        label_msj_error2 = ctk.CTkLabel (frame_error, text="Posibles causas:", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error2.grid(row=1, column=1, columnspan=2, sticky="ws")
        label_msj_error3 = ctk.CTkLabel (frame_error, text="  - La ruta original no existe o fue modificada", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error3.grid(row=2, column=1, columnspan=2, sticky="ws")
        label_msj_error4 = ctk.CTkLabel (frame_error, text="  - Se seleccionó una ruta incorrecta.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error4.grid(row=3, column=1, columnspan=2, sticky="ws")
        
        label_msj_error5 = ctk.CTkLabel (frame_error, text="Verifica que estás seleccionando la carpeta correcta e inténtalo nuevamente.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error5.grid(row=4, column=1, columnspan=2, sticky="ws")


    def widget_interfaz_db(self):
        """
        METODO QUE DIBUJA UNICAMENTE LA TABLA EN LA INTERFAZ
        """
        
        label_titulo = ctk.CTkLabel(self.frame_contenedor_db, text="Elementos ocultos", font=("Bahnschrift", 18, "bold"), text_color="#E8E8E8")
        label_titulo.grid(row = 0, column = 0, padx=10,pady=(10,0), sticky="w")
        
        #FRAME DE LA TABLA DB
        self.frame_db = ctk.CTkFrame (self.frame_contenedor_db, fg_color="transparent")
        self.frame_db.grid(row = 1, column = 0, padx=5, pady=5, sticky="snwe")
        self.frame_db.grid_columnconfigure(0, weight=1)
        self.frame_db.grid_rowconfigure(0, weight=1)        
        
        #configuracion de colores en la tabla
        style = ttk.Style()
        style.theme_use("alt")
        style.configure("Treeview", background="#2E2C2C", foreground="#D0CFCF", fieldbackground="#2E2C2C")
        style.configure("Treeview.Heading", background="#2E2C2C", foreground="#F0F0F0")
        style.map("Treeview.Heading", background=[("active", "#393838")], foreground=[("selected", "#D0CFCF")])

        self.tabla_db = ttk.Treeview(self.frame_db,  columns=("Tipo", "Nombre", "Origen", "Fecha"), show="headings")
        self.tabla_db.grid(row = 0, column = 0, padx=10, pady=10, sticky="snwe")
        self.tabla_db.bind("<Double-1>", self._doble_click_tabla)
        self.tabla_db.heading("Tipo", text="Tipo")
        self.tabla_db.heading("Nombre", text="Nombre")
        self.tabla_db.heading("Origen", text="Origen")
        self.tabla_db.heading("Fecha", text="Fecha")
        
        self.tabla_db.column("Tipo", width=60)
        self.tabla_db.column("Nombre", width=280)
        self.tabla_db.column("Origen", width=360)
        self.tabla_db.column("Fecha", width=150)
        
    def insertar_datos_db(self):
        
        """
        METODO QUE LEE LA DB E INSERTA LOS DATOS EN LA TABLA CADA VEZ QUE ES LLAMADO
        """
        
        
        self.datos_db = Leer_crear_db()
        self.tabla_db.delete(*self.tabla_db.get_children())

        if self.datos_db:
            for dato in self.datos_db:
                self.tabla_db.insert("", "end", values=dato)
        
    def _doble_click_tabla (self, event):
        
        """
        Metodo que se ejecuta al hacer doble click en la tabla
        """
        
        seleccion = self.tabla_db.selection()
        if not seleccion:
            return
        
        fila = seleccion[0]
        ruta_select = self.tabla_db.item(fila, "values")
        self.nombre_select = ruta_select[1] #nombre del archivo, util para cuando queda renombrado como copia
        self.ruta_select = ruta_select[2] #ruta orignal del archivo
        self.recuperacion_registro()
        

    def recuperacion_registro (self):
        """
        METODO QUE RECUPERA LOS ARCHIVOS DE FORMA INDEPENDIENTE DESDE LA TABLA CUANDO HACEN DOBLE CLICK
        """

        proteccion = Proteccion()
        restaurado = proteccion.desproteger_individual(self.ruta_select, self.nombre_select)
        
        if restaurado:

            proteccion.actualizar_db()
            self.insertar_datos_db()
            msj = f"✔{Path(self.ruta_select).name} restaurado. - Ubicación: {self.ruta_select}"
            self._actualizar_actividad(msj)
            
        else:
            self._interfaz_error_recuperar_2_click()
        
        
    def _interfaz_error_recuperar_2_click (self):
        """
        Metodo que muestra cuando hay un error al ocultar o desocultar
        """
        ventana_error = ctk.CTkToplevel(self)
        ventana_error.title("Error")
        ventana_error.geometry("520x265")
        ventana_error.resizable(False, False)
        
        ventana_error.update_idletasks()  

        ancho = ventana_error.winfo_width()  
        alto = ventana_error.winfo_height()  
        
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
        ventana_error.geometry(f"+{x}+{y}")

        ventana_error.lift()
        ventana_error.grab_set()
        ventana_error.bind("<Escape>", lambda event: ventana_error.destroy())
        
        icono = tk.PhotoImage(file=ruta_logo_png)
        ventana_error.icono_ref = icono
        ventana_error.after(200, lambda: ventana_error.iconphoto(False, ventana_error.icono_ref))
        


        frame_error = ctk.CTkFrame(ventana_error, fg_color="transparent")
        frame_error.pack(padx = 2, pady = (5,10), fill = "both", expand=True)
        
        logo_error = ctk.CTkImage (light_image=Image.open(ruta_logo_error), size=(30, 30))
        label_logo_error = ctk.CTkLabel (frame_error, image=logo_error, text="",)
        label_logo_error.grid(row=0, column=0, padx=(18,10), sticky="ws")

        label_msj_error = ctk.CTkLabel (frame_error, text=f"Error al restaurar.", font=("Bahnschrift", 20,"bold" ), text_color="#CF4343",)
        label_msj_error.grid(row=0, column=1, pady=3, sticky="w")
        label_msj_error2 = ctk.CTkLabel (frame_error, text="Posibles causas:", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error2.grid(row=1, column=1, columnspan=2, sticky="ws")
        label_msj_error3 = ctk.CTkLabel (frame_error, text="  - La ruta original no existe o fue modificada", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error3.grid(row=2, column=1, columnspan=2, sticky="ws")
        label_msj_error4 = ctk.CTkLabel (frame_error, text="  - El acceso a la ubicación está restringido", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error4.grid(row=3, column=1, columnspan=2, sticky="ws")
        label_msj_error5 = ctk.CTkLabel (frame_error, text="  - El elemento se encuentra dentro de una carpeta protegida.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error5.grid(row=4, column=1, columnspan=2, sticky="ws")
        
        label_msj_error6 = ctk.CTkLabel (frame_error, text="Solución:", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error6.grid(row=5, column=1, columnspan=2, sticky="ws")
        label_msj_error7 = ctk.CTkLabel (frame_error, text="  - Verifica la ruta original en el registro de la tabla.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error7.grid(row=6, column=1, columnspan=2, sticky="ws")
        
        label_msj_error8 = ctk.CTkLabel (frame_error, text="  - Si está dentro de una carpeta protegida, desprotégela primero.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error8.grid(row=7, column=1, columnspan=2, sticky="ws")
        
        label_msj_error9 = ctk.CTkLabel (frame_error, text="  - Vuelve a intentar.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error9.grid(row=8, column=1, columnspan=2, sticky="ws")

    def interfaz_actividad_reciente (self):
        """
        METODO QUE DIBUJA UNICAMENTE LA SECCION INFERIOR DE ACTIVIDAD RECIENTE
        """
        
        Actividad_label = ctk.CTkLabel(self.frame_actividad, text="Actividad Reciente: ", font=("Bahnschrift", 14, "bold"), text_color="#E8E8E8")
        Actividad_label.grid(row = 0, column = 0, padx=(10,0),pady=5, sticky="wesn")
        self.actividad = ctk.CTkEntry(self.frame_actividad, placeholder_text="No se ha registrado ninguna actividad", font=("Bahnschrift", 14.5), fg_color="transparent", text_color="#D0CFCF", border_width=0)
        self.actividad.grid(row = 0, column = 1, padx=(0,5),pady=5, sticky="we", columnspan=2)
        self.actividad.configure(state="readonly")
    
    def _actualizar_actividad (self, actividad): 

        self.actividad.configure(state="normal")
        self.actividad.delete(0, "end")
        self.actividad.insert(0, actividad)
        self.actividad.configure(state="readonly")
    
    def _interfaz_acerca_de (self,event = None):

        """
        Metodo que muestra informacion de la aplicacion
        """
        ventana = ctk.CTkToplevel(self)
        ventana.title("Acerca de")
        ventana.geometry("500x450")
        ventana.resizable(False, False)
        
        ventana.update_idletasks()  

        ancho = ventana.winfo_width()  
        alto = ventana.winfo_height()  
        
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
        ventana.geometry(f"+{x}+{y}")

        ventana.lift()
        ventana.grab_set()
        ventana.bind("<Escape>", lambda event: ventana.destroy())
        
        icono = tk.PhotoImage(file=ruta_logo_acerca_de)
        ventana.icono_ref = icono
        ventana.after(200, lambda: ventana.iconphoto(False, ventana.icono_ref))
        
        
        
        ## frame superior
        frame_superior = ctk.CTkFrame (ventana, fg_color="transparent")
        frame_superior.pack(fill="both")
        frame_superior.grid_columnconfigure(0, weight=1)
        
        linea_label = ctk.CTkFrame(frame_superior, fg_color="#242424", height=2) 
        linea_label.grid(row = 0, column = 0, padx=0, pady=5, sticky="eswn")
        
        logo_app = ctk.CTkImage (light_image=Image.open(ruta_logo_png), size=(122, 90))
        logo_app_label = ctk.CTkLabel (frame_superior, image=logo_app, text="", anchor="n")
        logo_app_label.grid(row=1, column=0, padx=10, pady=(10,4))


        #frame de titulo
        frame_titulo = ctk.CTkFrame(frame_superior, fg_color="transparent")
        frame_titulo.grid(row = 2, column = 0, padx=10)

        #widget que estan en el frame frame_titulo
        titulo1 = ctk.CTkLabel(frame_titulo, text="ORS", font=("Bahnschrift", 20, "bold"), anchor="e")
        titulo1.grid(row = 0, column = 0)
        
        titulo2 = ctk.CTkLabel(frame_titulo, text="4", font=("Bahnschrift", 20, "bold"), text_color="red")
        titulo2.grid(row = 0, column =1)
        
        titulo3 = ctk.CTkLabel(frame_titulo, text="GHOST", font=("Bahnschrift", 20, "bold"), anchor="w")
        titulo3.grid(row = 0, column = 2)


        label_version = ctk.CTkLabel (frame_superior, text="Version: 1.0.0", font=("Arial", 14), text_color="#D0CFCF")
        label_version.grid(row = 3, column = 0, padx=10, pady=5)

        label_descripcion = ctk.CTkLabel (frame_superior, text="Herramienta para ocultar archivos y carpetas", font=("Arial", 13), text_color="#D0CFCF", anchor="s")
        label_descripcion.grid(row = 4, column = 0, padx=10)
        
        label_descripcion_1 = ctk.CTkLabel (frame_superior, text="haciendo que dejen de ser visibles incluso con las opciones estándar de Windows. ", font=("Arial", 13), text_color="#D0CFCF")
        label_descripcion_1.grid(row = 5, column = 0, padx=10,)
        
        label_descripcion_2 = ctk.CTkLabel (frame_superior, text="En entornos Linux también permanecen ocultos bajo condiciones normales. ", font=("Arial", 13), text_color="#D0CFCF", anchor="n")
        label_descripcion_2.grid(row = 6, column = 0, padx=10 )
        
        linea_label1 = ctk.CTkFrame(frame_superior, fg_color="#242424", height=2) 
        linea_label1.grid(row = 7, column = 0, padx=0, pady=5, sticky="eswn")


        #### Frame medio
        frame_medio = ctk.CTkFrame (ventana, fg_color="transparent")
        frame_medio.pack(fill="both")
        frame_medio.grid_columnconfigure(0, weight=1)
        
        
        label_desarrollo = ctk.CTkLabel (frame_medio, text="Desarrollado por: Nelson Arteaga", font=("Arial", 14, "bold"), text_color="#D0CFCF", anchor="w")
        label_desarrollo.grid(row = 0, column = 0, padx=10,columnspan=3)
        
        
        frame_logos = ctk.CTkFrame (frame_medio, fg_color="transparent")
        frame_logos.grid(row = 1, column = 0, padx=10)
                
        logo_GitHub = ctk.CTkImage (light_image=Image.open(ruta_logo_github), size=(25, 25))        
        label_logo_github = ctk.CTkLabel (frame_logos,image=logo_GitHub, text="", cursor = "hand2")
        label_logo_github.grid(row = 1, column = 0, padx=10, pady=(5,10))
        label_logo_github.bind("<Button-1>", self.abrir_github)
        
        logo_instagram = ctk.CTkImage (light_image=Image.open(ruta_logo_instagram), size=(22, 22))        
        label_logo_instagram = ctk.CTkLabel (frame_logos,image=logo_instagram, text="", cursor = "hand2")
        label_logo_instagram.grid(row = 1, column = 1, padx=10, pady=(5,10))
        label_logo_instagram.bind("<Button-1>", self.abrir_instagram)
        
        logo_youtube = ctk.CTkImage (light_image=Image.open(ruta_logo_youtube), size=(33, 21))        
        label_logo_youtube = ctk.CTkLabel (frame_logos,image=logo_youtube, text="", cursor = "hand2")
        label_logo_youtube.grid(row = 1, column = 2, padx=10, pady=(5,10))
        label_logo_youtube.bind("<Button-1>", self.abrir_youtube)
        
        ####
                
        Boton_documentacion = ctk.CTkButton (frame_medio, text="Ver en GitHub", font=("Bahnschrift", 15, "bold"), text_color="#D0CFCF", width=200, height=30, fg_color="#313131", hover_color="#363333", command=self.abrir_documentacion)
        Boton_documentacion.grid(row = 2, column = 0, columnspan=3, padx=10, pady=(5,10))
        
        linea_label2 = ctk.CTkFrame(frame_medio, fg_color="#242424", height=2) 
        linea_label2.grid(row = 3, column = 0, columnspan=3 , padx=0, pady=5, sticky="eswn")
        
        label_ors4 = ctk.CTkLabel (frame_medio, text="© 2026 ORS4TECH (n0rs4rt)", font=("Arial", 13, "bold"), text_color="#D0CFCF")
        label_ors4.grid(row = 4, column = 0, padx=10,columnspan=3)
        
    
    def abrir_github (self, event):
        webbrowser.open("https://github.com/n0rs4rt")
    
    def abrir_instagram (self, event):
        webbrowser.open("https://www.instagram.com/ors4tech/")
        
    def abrir_youtube (self, event):
        webbrowser.open("https://www.youtube.com/@ORS4TECH")
        
    def abrir_documentacion (self):
        webbrowser.open("https://github.com/n0rs4rt/ORS4GHOST")
        