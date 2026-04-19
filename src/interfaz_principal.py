import customtkinter as ctk, logging, tkinter as tk
from PIL import Image

from core.RUTAS import *
from core.CONFIG_LOGS import configurar_logging
from core.USUARIO import Usuario
from interfaz_programa import PanelSistema

configurar_logging()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class Panel_principal(ctk.CTk ):
    def __init__(self):
        super().__init__()
        self.logging = logging.getLogger("LOGS")
    
        self.title("ORS4GHOST")
        self.resizable(False, False)
        self.update_idletasks()
        ancho = 700
        alto = 500

        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)

        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        self.iconbitmap(ruta_logo_ico)
        
        
        self.crear_frame_inicio()
        self.widget_frame_inicio()
        
        self.usuario = Usuario()

        
        
    def crear_frame_inicio (self):
        """
        Frame de la ventana inicial de login
        """
        
        self.frame_inicio = ctk.CTkFrame (self, fg_color="transparent")
        self.frame_inicio.pack(fill="both", expand=True)


    def widget_frame_inicio (self):
        """
        Widgets del frame de login
        """

        #frame de logo
        frame_ima_logo = ctk.CTkFrame(self.frame_inicio, fg_color="transparent")
        frame_ima_logo.pack(fill = "both", padx=10, pady=(5,3))

        #widget que estan en el frame frame_ima_logo
        imagen_logo = ctk.CTkImage (light_image=Image.open(ruta_logo_png), size=(180, 130))
        label_logo = ctk.CTkLabel(frame_ima_logo, image=imagen_logo, text="")
        label_logo.pack(padx=10, pady=(55,0))


        #frame de titulo
        frame_titulo = ctk.CTkFrame(self.frame_inicio, fg_color="transparent")
        frame_titulo.pack(pady=(0, 20))
        
        #widget que estan en el frame frame_titulo
        titulo1 = ctk.CTkLabel(frame_titulo, text="ORS", font=("Bahnschrift", 35, "bold"))
        titulo1.pack(side = "left")
        
        titulo2 = ctk.CTkLabel(frame_titulo, text="4", font=("Bahnschrift", 35, "bold"), text_color="red")
        titulo2.pack(side = "left")
        
        titulo3 = ctk.CTkLabel(frame_titulo, text="GHOST", font=("Bahnschrift", 35, "bold"))
        titulo3.pack(side = "left")


        #frame de login
        frame_login = ctk.CTkFrame(self.frame_inicio,border_width=2, fg_color="#1C1C1D")
        frame_login.pack( padx=20, pady=20)
        
        self.entry_usuario = ctk.CTkEntry(frame_login, placeholder_text="Usuario", border_width=2, width=350, height=30, font=("Bahnschrift", 15))
        self.entry_usuario.grid(row=0, column=0, padx=20, pady=(25,20), columnspan=2, sticky="nsew")
        self.entry_usuario.bind("<Return>", self.enter_ingresar)
        
        self.entry_password = ctk.CTkEntry(frame_login, placeholder_text="Contraseña", border_width=2, width=350, height=30, font=("Bahnschrift", 15), show="*")
        self.entry_password.grid(row=1, column=0, padx=20, pady=(0,20), columnspan=2, sticky="nsew")
        self.entry_password.bind("<Return>", self.enter_ingresar)
        
        boton_ingresar = ctk.CTkButton(frame_login, text="Ingresar", border_width=2, width=200, height=30, font=("Bahnschrift", 15),fg_color="#1C1C1D", hover_color="#840F0F", command=self.boton_ingresar)
        boton_ingresar.grid(row=2, column=0, padx=20, pady=(0,15), sticky="w")
        
        boton_Crear_Usuario = ctk.CTkButton(frame_login, text="Crear Usuario", border_width=2, width=200, height=30, font=("Bahnschrift", 15),fg_color= "#1C1C1D", hover_color="#840F0F", command= self.boton_crear_usuario)
        boton_Crear_Usuario.grid(row=2, column=1, padx=20, pady=(0,15), sticky="w")
        
        self.label_eliminar_user = ctk.CTkLabel(frame_login, text="¿Eliminar el Usuario?", fg_color="transparent", text_color="#AFAFAF", font=("Bahnschrift", 15))
        self.label_eliminar_user.grid(row=3, column=0, padx=20, pady=(0,20), columnspan=2, sticky="nsew")
        self.label_eliminar_user.bind("<Enter>", command= self._selecionar_elimiar_usuario)
        self.label_eliminar_user.bind("<Leave>", command= self._desselecionar_elimiar_usuario)
        self.label_eliminar_user.bind("<Button-1>", command= self._interfaz_eliminar_usuario)


                                            ###MODULOS CREAR USUARIO


####### BOTON INGRESAR INICIAR SESION

    def enter_ingresar(self, event=None):
        self.boton_ingresar()

    def boton_ingresar(self):
        
        """
        METODO QUE REALIZA EL LOGIN, ACTUALIZA LA FECHA DE LOGIN, Y LLAMA A LA SEGUNDA VENTANA
        """
        
        
        if not self.usuario.verificar_db():
            self._interfaz_sin_usuarios()
            return
        
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        
        login = self.usuario.login(usuario, password)

        if login:
            fecha_ultimo_login = "No disponible"
            ultimo_acceso = self.usuario._registro_ultimo_acceso()
            if ultimo_acceso:
                fecha_ultimo_login = self.usuario.acceso
            
            
            self.frame_inicio.destroy()
            
            self.panel = PanelSistema(self,usuario, fecha_ultimo_login)
            self.panel.pack(fill="both", expand=True)
            
        
        elif login is False:
            self._interfaz_user_invalido()
        
        else:
            self._interfaz_error_db()
    
    def _interfaz_sin_usuarios(self):
        
        """
        Metodo que disena la ventana cuando no existe usuarios
        """
        
        ventana_error = ctk.CTkToplevel(self)
        ventana_error.title("Inicio de sesion")
        ventana_error.geometry("350x90")
        ventana_error.resizable(False, False)

        ventana_error.update_idletasks()  

        ancho = ventana_error.winfo_width()  
        alto = ventana_error.winfo_height()  
        
        x = self.winfo_x() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_y() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
        ventana_error.geometry(f"+{x}+{y}")

        ventana_error.lift()
        ventana_error.grab_set()
        ventana_error.bind("<Escape>", lambda event: ventana_error.destroy())
        
        icono = tk.PhotoImage(file=ruta_logo_png)
        ventana_error.icono_ref = icono
        ventana_error.after(200, lambda: ventana_error.iconphoto(False, ventana_error.icono_ref))

        frame_error = ctk.CTkFrame(ventana_error, fg_color="transparent")
        frame_error.pack(padx = 2, pady = (5,10), fill = "both", expand=True)
        frame_error.grid_columnconfigure(1, weight=1)

        logo_error = ctk.CTkImage (light_image=Image.open(ruta_logo_alerta), size=(30, 25))
        label_logo_error = ctk.CTkLabel (frame_error, image=logo_error, text="",anchor="s")
        label_logo_error.grid(row=0, column=0, padx=(18,10), sticky="ws")

        label_msj_error = ctk.CTkLabel (frame_error, text="No se detecto ningun usuario registrado", font=("Bahnschrift", 14,"bold" ), text_color="#DCAA21", anchor="s")
        label_msj_error.grid(row=0, column=1, pady=3, sticky="ws")
        label_msj_error2 = ctk.CTkLabel (frame_error, text="Por favor cree un usuario primero", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="w")
        label_msj_error2.grid(row=1, column=1, sticky="w")


    def _interfaz_user_invalido(self):
        """
        Metodo que disena la ventana de usuario invalido
        """
        
        ventana_error = ctk.CTkToplevel(self)
        ventana_error.title("Inicio de sesion")
        ventana_error.geometry("300x80")
        ventana_error.resizable(False, False)

        ventana_error.update_idletasks()  

        ancho = ventana_error.winfo_width()  
        alto = ventana_error.winfo_height()  
        
        x = self.winfo_x() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_y() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
        ventana_error.geometry(f"+{x}+{y}")

        ventana_error.lift()
        ventana_error.grab_set()
        ventana_error.bind("<Escape>", lambda event: ventana_error.destroy())

        icono = tk.PhotoImage(file=ruta_logo_png)
        ventana_error.icono_ref = icono
        ventana_error.after(200, lambda: ventana_error.iconphoto(False, ventana_error.icono_ref))

        frame_error = ctk.CTkFrame(ventana_error, fg_color="transparent")
        frame_error.pack(padx = 2, pady = (5,10), fill = "both", expand=True)

        logo_error = ctk.CTkImage (light_image=Image.open(ruta_logo_alerta), size=(30, 25))
        label_logo_error = ctk.CTkLabel (frame_error, image=logo_error, text="",anchor="s")
        label_logo_error.grid(row=0, column=0, padx=(18,10), sticky="ws")

        label_msj_error = ctk.CTkLabel (frame_error, text="Usuario o contraseña incorrecta", font=("Bahnschrift", 14,"bold" ), text_color="#DCAA21", anchor="s")
        label_msj_error.grid(row=0, column=1, pady=3, sticky="w")
        label_msj_error2 = ctk.CTkLabel (frame_error, text="Intentalo de nuevo", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error2.grid(row=1, column=1,sticky="w")
        
    def _interfaz_error_db (self):
        """
        Metodo que hay un error en la db al iniciar login
        """
        ventana_error = ctk.CTkToplevel(self)
        ventana_error.title("Error")
        ventana_error.geometry("350x70")
        ventana_error.resizable(False, False)
        
        ventana_error.update_idletasks()  

        ancho = ventana_error.winfo_width()  
        alto = ventana_error.winfo_height()  
        
        x = self.winfo_x() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_y() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
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

        label_msj_error = ctk.CTkLabel (frame_error, text="Error al acceder a la base de datos", font=("Bahnschrift", 14,"bold" ), text_color="#CF4343",)
        label_msj_error.grid(row=0, column=1, pady=3, sticky="w")
        label_msj_error2 = ctk.CTkLabel (frame_error, text="Problema de integridad en base de datos", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error2.grid(row=1, column=1, columnspan=2, sticky="ws")


#### boton crear usuario
    def boton_crear_usuario(self):
        """
        Boton para crear un nuevo usuario, 
        si no existe una base de datos, se abre una ventana para confirmar la contraseña
        """

        if not self.usuario.verificar_db():

            self.nombre_usuario = self.entry_usuario.get().strip()
            self.password_usuario = self.entry_password.get().strip()
            if self.nombre_usuario and self.password_usuario:
                self._ventana_crear_user()     #Abre la ventana para confirmar la contraseña
            else:
                self._interfaz_datos_vacio()
        else:
            self._interfaz_error_usuario_existe()

    def _interfaz_error_usuario_existe (self):
        
        """
        Metodo que se ejecuta cuando el existe un usuario registro falla
        """
        ventana_error = ctk.CTkToplevel(self)
        ventana_error.title("Crear Usuario")
        ventana_error.geometry("255x110")
        ventana_error.resizable(False, False)

        ventana_error.update_idletasks()  

        ancho = ventana_error.winfo_width()  
        alto = ventana_error.winfo_height()  
        
        x = self.winfo_x() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_y() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
        ventana_error.geometry(f"+{x}+{y}")

        ventana_error.lift()
        ventana_error.grab_set()
        ventana_error.bind("<Escape>", lambda event: ventana_error.destroy())

        icono = tk.PhotoImage(file=ruta_logo_png)
        ventana_error.icono_ref = icono
        ventana_error.after(200, lambda: ventana_error.iconphoto(False, ventana_error.icono_ref))

        frame_error = ctk.CTkFrame(ventana_error, fg_color="transparent")
        frame_error.pack(padx = 2, pady = (5,10), fill = "both", expand=True)
        frame_error.grid_columnconfigure(1, weight=1)

        logo_error = ctk.CTkImage (light_image=Image.open(ruta_logo_alerta), size=(30, 25))
        label_logo_error = ctk.CTkLabel (frame_error, image=logo_error, text="",anchor="s")
        label_logo_error.grid(row=0, column=0, padx=(18,10), sticky="ws")

        label_msj_error = ctk.CTkLabel (frame_error, text="Error al crear usuario", font=("Bahnschrift", 14,"bold" ), text_color="#DCAA21", anchor="s")
        label_msj_error.grid(row=0, column=1, pady=3, sticky="ws")
        label_msj_error2 = ctk.CTkLabel (frame_error, text="Ya existe un usuario registrado.", font=("Bahnschrift", 14 ), text_color="#E8E8E8", anchor="s")
        label_msj_error2.grid(row=1, column=0, padx=20, columnspan=2, sticky="ws")
        label_msj_error3 = ctk.CTkLabel (frame_error, text="No es posible crear otro.", font=("Bahnschrift", 14 ), text_color="#E8E8E8", anchor="n")
        label_msj_error3.grid(row=2, column=0, padx=20, columnspan=2, sticky="wn")

    def _interfaz_datos_vacio (self):
        
        """
        Metodo que se ejecuta cuando el registro fallals campos stan vacios
        """
        
        ventana_error = ctk.CTkToplevel(self)
        ventana_error.title("Crear Usuario")
        ventana_error.geometry("325x100")
        ventana_error.resizable(False, False)

        ventana_error.update_idletasks()  

        ancho = ventana_error.winfo_width()  
        alto = ventana_error.winfo_height()  
        
        x = self.winfo_x() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_y() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
        ventana_error.geometry(f"+{x}+{y}")

        ventana_error.lift()
        ventana_error.grab_set()
        ventana_error.bind("<Escape>", lambda event: ventana_error.destroy())

        icono = tk.PhotoImage(file=ruta_logo_png)
        ventana_error.icono_ref = icono
        ventana_error.after(200, lambda: ventana_error.iconphoto(False, ventana_error.icono_ref))


        frame_error = ctk.CTkFrame(ventana_error, fg_color="transparent")
        frame_error.pack(padx = 2, pady = (5,10), fill = "both", expand=True)
        frame_error.grid_columnconfigure(1, weight=1)

        logo_error = ctk.CTkImage (light_image=Image.open(ruta_logo_alerta), size=(30, 25))
        label_logo_error = ctk.CTkLabel (frame_error, image=logo_error, text="",anchor="s")
        label_logo_error.grid(row=0, column=0, padx=(18,10), sticky="ws")

        label_msj_error = ctk.CTkLabel (frame_error, text="Datos incompletos", font=("Bahnschrift", 14,"bold" ), text_color="#DCAA21", anchor="s")
        label_msj_error.grid(row=0, column=1, pady=3, sticky="ws")
        label_msj_error2 = ctk.CTkLabel (frame_error, text="Debes escribir un usuario y una contraseña.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="s")
        label_msj_error2.grid(row=1, column=0, padx=20, columnspan=2, sticky="ws")
        label_msj_error3 = ctk.CTkLabel (frame_error, text="Solo se permite un usuario en la aplicacion.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error3.grid(row=2, column=0, padx=20, columnspan=2, sticky="wn")
        
    def _ventana_crear_user (self):
        """
        Ventana para escribir la confirmacion de la contrasena
        """
        
        self.ventana_confimar = None
        if self.ventana_confimar is None or not self.ventana_confimar.winfo_exists():
            self.ventana_confimar = ctk.CTkToplevel(self)

            self.ventana_confimar.title("Confirmar contraseña")
            self.ventana_confimar.geometry("300x125")

            self.ventana_confimar.update_idletasks()  
            ancho = self.ventana_confimar.winfo_width()  
            alto = self.ventana_confimar.winfo_height()  
            
            x = self.winfo_x() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
            y = self.winfo_y() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
            self.ventana_confimar.geometry(f"+{x}+{y}")
            self.ventana_confimar.resizable(False, False)
            self.ventana_confimar.lift()
            self.ventana_confimar.grab_set()
            self.ventana_confimar.attributes("-topmost", True)
            self.ventana_confimar.grid_rowconfigure(0, weight=1)
            self.ventana_confimar.grid_columnconfigure(0, weight=1)
            self.ventana_confimar.bind("<Escape>", lambda event: self.ventana_confimar.destroy())

            icono = tk.PhotoImage(file=ruta_logo_png)
            self.ventana_confimar.icono_ref = icono
            self.ventana_confimar.after(200, lambda: self.ventana_confimar.iconphoto(False, self.ventana_confimar.icono_ref))

            self.widget_ventana_crear_user()
            
    def widget_ventana_crear_user (self):
        """
        Widget de la ventana para crear un nuevo usuario
        """
        self.frame_confirmar = ctk.CTkFrame(self.ventana_confimar, fg_color="transparent")
        self.frame_confirmar.pack(fill = "both", expand=True)
        
        #widgeets del frame
        label_titulo = ctk.CTkLabel(self.frame_confirmar, text="Confirmar Contraseña", font=("Bahnschrift", 16, "bold"))
        label_titulo.pack(pady=5)
        
        self.entry_password2 = ctk.CTkEntry(self.frame_confirmar, placeholder_text="Contraseña", border_width=2, width=250, height=30, font=("Bahnschrift", 15), show="*")
        self.entry_password2.pack(pady=5)
        self.entry_password2.bind("<Return>", self._confirmar_pass)
        
        
        boton_confirmar = ctk.CTkButton(self.frame_confirmar, text="Confirmar", border_width=2, width=200, height=30, font=("Bahnschrift", 15),fg_color="#1C1C1D", hover_color="#840F0F",command=self._confirmar_pass)
        boton_confirmar.pack(pady=5)

    def _confirmar_pass(self, event=None):
        """
        Es llamada por el boton de confirmar, 
        metodo que Confirma que las contraseñas sean iguales para crear un nuevo usuario
        y crea el frame en pantalla con los widget
        """
        self.password2 = self.entry_password2.get()

        # print (password1, password2)
        
        if self.password_usuario != self.password2:
            self.ventana_confimar.geometry ("300x155")
            msj_error = ctk.CTkLabel(self.frame_confirmar, text="Las contraseñas no coinciden", font=("Bahnschrift", 14, "bold"), text_color="#AB1B1B")
            msj_error.pack(pady=5)
            return
        
        else:
            
            if len(self.password2) <6:
                self.ventana_confimar.geometry ("320x155")
                msj_error = ctk.CTkLabel(self.frame_confirmar, text="La contraseña debe tener minimo 6 caracteres", font=("Bahnschrift", 14, "bold"), text_color="#AB1B1B")
                msj_error.pack(pady=5)
                return
            
            usuario_creado =self.usuario.crear_usuario(self.nombre_usuario, self.password2)
            
            if usuario_creado:
                if self.usuario.crear_db():
                    self._interfaz_registro_concluido()
                else:
                    self._interfaz_registro_fallido()
            else:
                self._interfaz_registro_fallido()

    def _interfaz_registro_concluido(self):
        
        """
        Metodo que se ejecuta cuando el registro es concluido
        """
        
        self.ventana_confimar.geometry ("650x310")
        self.frame_confirmar.destroy()
        
        self.ventana_confimar.update_idletasks()  

        ancho = self.ventana_confimar.winfo_width()  
        alto = self.ventana_confimar.winfo_height()  
        
        x = self.winfo_x() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_y() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
        self.ventana_confimar.geometry(f"+{x}+{y}")
    
        #FRAME REGISTRO contenedor de widgets
        frame_registro = ctk.CTkFrame(self.ventana_confimar, )
        frame_registro.grid(row = 0, column = 0, padx=0, pady=5, sticky="wsen")
        frame_registro.grid_columnconfigure(0, weight=0)
        frame_registro.grid_columnconfigure(1, weight=1)

        titulo = ctk.CTkLabel (frame_registro, text="!Usuario Creado Correctamente!", font=("Bahnschrift", 20, "bold"), fg_color="#242323",text_color="#E7E7E7",anchor="center")
        titulo.grid(row = 0, column = 0, padx=0, pady=0, sticky="wsen", columnspan=2) 

        linea = ctk.CTkFrame(frame_registro, fg_color="#0D0C0C", height=2)
        linea.grid(row = 1, column = 0, padx=0, pady=5, sticky="eswn", columnspan=2)

        label_nom_usuario = ctk.CTkLabel (frame_registro, text=f"Usuario: {self.nombre_usuario}", font=("Bahnschrift", 16), text_color="#E7E7E7")
        label_nom_usuario.grid(row =2 , column = 0, padx=20, pady=5, sticky="w")

        label_pass = ctk.CTkLabel (frame_registro, text=f"Contraseña: {self.password_usuario}", font=("Bahnschrift", 16,"bold" ), text_color="#E7E7E7")
        label_pass.grid(row = 3, column = 0, padx=20, pady=1, sticky="w")

        label_key = ctk.CTkLabel (frame_registro, text=f"Llave de Recuperacion:", font=("Bahnschrift", 16,"bold" ), text_color="#E7E7E7")
        label_key.grid(row = 4, column = 0, padx=(20,0), pady=1, sticky="w") 
        
        self.label_key_recovery = ctk.CTkEntry(frame_registro, font=("Bahnschrift", 24,"bold" ), text_color="#DCAA21", fg_color="transparent", border_color="trasparent", border_width=0)
        self.label_key_recovery.insert(0, f"{self.usuario.key_recovery}") 
        self.label_key_recovery.grid(row = 4, column = 1, padx=10, pady=1, sticky="ew")
        self.label_key_recovery.bind("<Button-3>", command=self._menu_click_derecho)

        #frame externo para el borde
        frame_externo_msj =  ctk.CTkFrame(frame_registro, border_color="#DCAA21", border_width=2 , fg_color="#363636")
        frame_externo_msj.grid(row = 5, column = 0, padx=20, pady=5, stick = "nsew", columnspan=2)
        frame_externo_msj.grid_columnconfigure(0, weight=1)
        
        #frame interno
        frame_interno_msj =  ctk.CTkFrame(frame_externo_msj, fg_color="transparent")
        frame_interno_msj.grid(row = 0, column = 0, padx = 20,pady=20, stick = "nsew")
        
        logo_alerta = ctk.CTkImage (light_image=Image.open(ruta_logo_alerta), size=(32, 30))
        label_alerta = ctk.CTkLabel (frame_interno_msj, image=logo_alerta, text="")
        label_alerta.grid(row = 0, column = 0, padx= (1,5), sticky="w", rowspan=2)
        
        msj = ctk.CTkLabel (frame_interno_msj, text="IMPORTANTE: Guarda la llave recuperación en un lugar seguro.!", font=("Bahnschrift", 16,"bold" ), text_color="#DCAA21", anchor="w")
        msj.grid(row = 0, column = 1, padx=(5), sticky="w")

        msj2 = ctk.CTkLabel (frame_interno_msj, text="Si la pierdes, no podrás restablecer el acceso a tu cuenta.", font=("Bahnschrift", 16 ),text_color="#DCAA21", anchor="w")
        msj2.grid(row = 1, column = 1, padx=(5), sticky="wn")
        
        boton_aceptar= ctk.CTkButton(frame_registro, text="Aceptar", border_width=2, width=200, height=30, font=("Bahnschrift", 15),fg_color="#1C1C1D", hover_color="#840F0F",command=self._cerrar_ventana_crear_user)
        boton_aceptar.grid(row = 7, column = 1, padx=20, pady=5, sticky="w", columnspan=2)

    def _interfaz_registro_fallido(self):
        """
        Metodo que se ejecuta cuando el registro falla
        """
        ventana_error = ctk.CTkToplevel(self)
        ventana_error.title("Error")
        ventana_error.geometry("280x100")
        ventana_error.resizable(False, False)

        ventana_error.update_idletasks()  

        ancho = ventana_error.winfo_width()  
        alto = ventana_error.winfo_height()  
        
        x = self.winfo_x() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_y() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
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
        label_logo_error = ctk.CTkLabel (frame_error, image=logo_error, text="",anchor="s")
        label_logo_error.grid(row=0, column=0, padx=(18,10), sticky="ws")

        label_msj_error = ctk.CTkLabel (frame_error, text="No fue posible crear el usuario", font=("Bahnschrift", 14,"bold" ), text_color="#CF4343", anchor="s")
        label_msj_error.grid(row=0, column=1, pady=3, sticky="ws")
        label_msj_error2 = ctk.CTkLabel (frame_error, text="Se produjo un error inesperado.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="s")
        label_msj_error2.grid(row=1, column=0, padx=20, columnspan=2, sticky="ws")
        label_msj_error3 = ctk.CTkLabel (frame_error, text="Por favor, intenta nuevamente.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="n")
        label_msj_error3.grid(row=2, column=0, padx=20, columnspan=2, sticky="wn")
        
    def _menu_click_derecho(self, event):
        "Metodo que crea el click derecho"
        
        menu_click = tk.Menu(self, tearoff=0, bg="#1C1C1D", fg="#E7E7E7", activebackground="#1C1C1D", activeforeground="#E7E7E7")
        menu_click.add_command(label="Copiar", command=self._copiar_portapapeles)
        menu_click.tk_popup(event.x_root, event.y_root) #calcula la posicion donde se haga click
        
    def _copiar_portapapeles(self):
        """
        Metodo que copia el texto de la llave de recuperacion al portapapeles
        """
        
        self.label_key_recovery.clipboard_clear()
        try:
            texo_copiado = self.label_key_recovery.selection_get()
            self.update() 
        except:
            texo_copiado =""
        self.label_key_recovery.clipboard_append(texo_copiado)

    def _cerrar_ventana_crear_user(self):
        self.ventana_confimar.destroy()

    
    #                   ###MODULOO ELIMINAR USUARIO####
    def _selecionar_elimiar_usuario(self, event):
        """
        Metodo que cambia de color cuando el usuario pasa el cursor por encima
        """
        self.label_eliminar_user.configure(text_color="#CF4343")

    def _desselecionar_elimiar_usuario(self, event):
        """
        Metodo que cambia de color cuando el usuario sale del cursor
        """
        self.label_eliminar_user.configure(text_color="#AFAFAF")

    
    def _interfaz_eliminar_usuario(self, event):
        """
        Metodo que crea la interfaz para elimina el usuario
        """
        if not self.usuario.verificar_db():
            self._interfaz_usuarios_no_existe() #Si no existe la base de datos mostramos el error
            return
        
        self.ventana_eliminar = ctk.CTkToplevel(self)
        self.ventana_eliminar.title("Eliminar Usuario")
        self.ventana_eliminar.geometry("500x290")
        self.ventana_eliminar.resizable(False, False)

        self.ventana_eliminar.update_idletasks()  

        ancho = self.ventana_eliminar.winfo_width()  
        alto = self.ventana_eliminar.winfo_height()  
        
        x = self.winfo_x() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_y() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
        self.ventana_eliminar.geometry(f"+{x}+{y}")

        self.ventana_eliminar.lift()
        self.ventana_eliminar.grab_set()
        self.ventana_eliminar.grid_columnconfigure(0, weight=1)
        self.ventana_eliminar.bind("<Escape>", lambda event: self.ventana_eliminar.destroy())
        
        icono = tk.PhotoImage(file=ruta_logo_png)
        self.ventana_eliminar.icono_ref = icono
        self.ventana_eliminar.after(200, lambda: self.ventana_eliminar.iconphoto(False, self.ventana_eliminar.icono_ref))

        
        #frame header
        frame_contenedor_msjs = ctk.CTkFrame (self.ventana_eliminar, fg_color="transparent")
        frame_contenedor_msjs.grid(row=0, column=0, padx=5,pady=20, sticky="we")
        frame_contenedor_msjs.grid_columnconfigure(0, weight=1)
        frame_contenedor_msjs.grid_columnconfigure(1, weight=1)

        logo_alerta = ctk.CTkImage (light_image=Image.open(ruta_logo_alerta), size=(25, 22))
        label_logo_alerta = ctk.CTkLabel (frame_contenedor_msjs, image=logo_alerta, text="")
        label_logo_alerta.grid(row=0, column=0, padx=10, sticky="e")

        label_msj_confirmar = ctk.CTkLabel (frame_contenedor_msjs, text="¿Estás seguro de eliminar el usuario?", font=("Bahnschrift", 17), text_color="#DCAA21", anchor="w")
        label_msj_confirmar.grid(row=0, column=1, sticky="w", padx=(0,10))
        
        
        #Frame nota
        frame_contenedor_nota = ctk.CTkFrame (self.ventana_eliminar, fg_color="transparent")
        frame_contenedor_nota.grid(row=1, column=0, padx=10, sticky="we")
        frame_contenedor_nota.grid_columnconfigure(0, weight=0)
        frame_contenedor_nota.grid_columnconfigure(1, weight=0)
        frame_contenedor_nota.grid_columnconfigure(2, weight=0)

        label_nota = ctk.CTkLabel (frame_contenedor_nota, text="Nota:", font=("Bahnschrift", 15,"bold"), text_color="#E8E8E8", anchor="w")
        label_nota.grid(row=0, column=0, padx=5, sticky="w")

        label_nota1 = ctk.CTkLabel (frame_contenedor_nota, text="Esta acción únicamente eliminará el usuario.", font=("Bahnschrift", 15), text_color="#E8E8E8", anchor="e")
        label_nota1.grid(row=0, column=1, padx=5,sticky="e")

        label_nota2 = ctk.CTkLabel (frame_contenedor_nota, text="Los archivos y configuraciones no se borrarán.", font=("Bahnschrift", 15), text_color="#E8E8E8", anchor="n")
        label_nota2.grid(row=1, column=0, padx=5,sticky="w", columnspan=2)

        label_nota3 = ctk.CTkLabel (self.ventana_eliminar, text="Ingresa la Llave de Recuperación para confirmar", font=("Bahnschrift", 18), text_color="#E8E8E8", anchor="s")
        label_nota3.grid(row=2, column=0, padx=15,pady=5,sticky="w", columnspan=3)
        
        #widget ventana principal
        self.entry_key_recovery = ctk.CTkEntry(self.ventana_eliminar, placeholder_text="Llave de Recuperación", placeholder_text_color="#AFAFAF", font=("Bahnschrift", 14), text_color="#E8E8E8", width=200, height=30)
        self.entry_key_recovery.grid(row=4, column=0, padx=(10,10),pady=(10,0),sticky="wesn")
        self.entry_key_recovery.bind("<Button-3>", self._menu_pegar)
        self.entry_key_recovery.bind("<Return>", self.eliminar_usuario)


        label_nota4 = ctk.CTkLabel (self.ventana_eliminar, text="Importante! Esta acción es irreversible.", font=("Bahnschrift", 15), text_color="#DCAA21")
        label_nota4.grid(row=5, column=0, padx=15,pady=7,sticky="w")

        boton_eliminar = ctk.CTkButton (self.ventana_eliminar, text="Eliminar", font=("Bahnschrift", 15), text_color="#E8E8E8", fg_color= "#840F0F",hover_color="#952424", width=100, height=30, command=self.eliminar_usuario)
        boton_eliminar.grid(row=6, column=0, padx=15,sticky="e") 

    
    def _menu_pegar(self, event=None):
        """
        Metodo que abre el menu de pegar
        """
        self.menu_pega = tk.Menu(self, tearoff=0, bg="#1C1C1D", fg="#E7E7E7", activebackground="#1C1C1D", activeforeground="#E7E7E7")
        self.menu_pega.add_command(label="Pegar", command=self._pegar)
        self.menu_pega.tk_popup(event.x_root, event.y_root)
        
    def _pegar (self):
        """
        Metodo que pega el contenido del portapapeles
        """
        try:
            self.entry_key_recovery.delete(0, "end")
            texto = self.clipboard_get()
            self.entry_key_recovery.insert(0, texto)
        except:
            pass
    
    def _interfaz_usuarios_no_existe(self):
        """
        Metodo que muestra la interfaz cuando no existen usuarios
        """
        
        ventana_error = ctk.CTkToplevel(self)
        ventana_error.title("Error")
        ventana_error.geometry("310x80")
        ventana_error.resizable(False, False)

        ventana_error.update_idletasks()  

        ancho = ventana_error.winfo_width()  
        alto = ventana_error.winfo_height()  
        
        x = self.winfo_x() + (self.winfo_width() // 2) - (ancho // 2)#Ventana principal
        y = self.winfo_y() + (self.winfo_height() // 2) - (alto // 2)#Ventana principal  
        ventana_error.geometry(f"+{x}+{y}")

        ventana_error.lift()
        ventana_error.grab_set()
        ventana_error.bind("<Escape>", lambda event: ventana_error.destroy())

        icono = tk.PhotoImage(file=ruta_logo_png)
        ventana_error.icono_ref = icono
        ventana_error.after(200, lambda: ventana_error.iconphoto(False, ventana_error.icono_ref))


        frame_error = ctk.CTkFrame(ventana_error, fg_color="transparent")
        frame_error.pack(padx = 2, pady = (5,10), fill = "both", expand=True)
        frame_error.grid_columnconfigure(1, weight=1)

        logo_error = ctk.CTkImage (light_image=Image.open(ruta_logo_alerta), size=(30, 25))
        label_logo_error = ctk.CTkLabel (frame_error, image=logo_error, text="",anchor="s")
        label_logo_error.grid(row=0, column=0, padx=(18,10), sticky="ws")

        label_msj_error = ctk.CTkLabel (frame_error, text="Usuario no dectado", font=("Bahnschrift", 14,"bold" ), text_color="#DCAA21", anchor="s")
        label_msj_error.grid(row=0, column=1, pady=3, sticky="ws")
        label_msj_error2 = ctk.CTkLabel (frame_error, text="No se detecto ningun usuario registrado.", font=("Bahnschrift", 14), text_color="#E8E8E8", anchor="s")
        label_msj_error2.grid(row=1, column=0, padx=20, columnspan=2, sticky="ws")

    def eliminar_usuario(self, event=None):
        """
        Metodo que elimina el usuario
        """

        key_recovery = self.entry_key_recovery.get().strip()
        usuario_eliminado = self.usuario.reset_db(key_recovery)
        
        if usuario_eliminado:
            self.ventana_eliminar.destroy()
        
        elif usuario_eliminado is False:
            self.entry_key_recovery.delete(0, "end")
            self.entry_key_recovery.configure(placeholder_text="Llave de Recuperación Incorrecta", placeholder_text_color="#EB4E4E")
        
        elif usuario_eliminado is None:
            self.entry_key_recovery.delete(0, "end")
            self.entry_key_recovery.configure(placeholder_text="ERROR INTERNO EN LA DB", placeholder_text_color="#EB4E4E")

app = Panel_principal()
app.mainloop()  