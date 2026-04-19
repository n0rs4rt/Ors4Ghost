import shutil, subprocess, json, sqlite3, uuid, logging, sys
from datetime import datetime
from pathlib import Path
from core.RUTAS import *


class Proteccion:
    def __init__(self):
        self.logging = logging.getLogger("LOGS")
        self.nombre_carpeta_baul = ".sys_cache" # carpeta oculta que guarda toda la informacion
        self.carpetas_en_baul = []
        self.ids_en_baul = []

    def _validar_carpeta (self, dir_file_proteger):

        ubicacion_app = Path(sys.executable) #para obterner la ruta del nuestro .exe
        ubicacion_app_dir = ubicacion_app.parent / "_internal"

        dir_file_proteger = Path(dir_file_proteger).resolve() #para normalizar la ruta  y asegurar que sea absoluta y no una ruta falsa

        carpetas = ["C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)"]

        for c in carpetas:

            if Path(c) == dir_file_proteger or dir_file_proteger == Path("C:\\") or dir_file_proteger == Path("C:\\Users") or dir_file_proteger == ubicacion_app or dir_file_proteger == ubicacion_app_dir:
                # print ("ruta no permitida")
                self.logging.warning(f"ruta {dir_file_proteger} no permitida")
                return False

            if Path(c) in dir_file_proteger.parents:
                self.logging.warning(f"ruta {dir_file_proteger} no permitida")
                # print ("ruta no permitida")
                return False

        # print ("ruta permitida")

        return True

    def _proteger_carpeta (self, carpeta_user):
        
        """
        METODO PROTEGE CARPETA Y LO AGREGA A LA DB
        """
        
        carpeta_user = Path(carpeta_user).resolve() #para normalizar la ruta  y asegurar que sea absoluta
        ruta_base = carpeta_user.parent #SUBIMOS UN NIVEL
        
        carpeta_oculta = ruta_base / self.nombre_carpeta_baul
        carpeta_oculta.mkdir(parents=True, exist_ok=True) #creamos la carpeta oculta la base

        comando = ["attrib", "+h", "+s", f"{str(carpeta_oculta)}"]

        resultado = subprocess.run(comando, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW) #ocultamos la carpeta
        
        if resultado.returncode != 0:
            self.logging.error(f"error al ocultar la carpeta: {carpeta_oculta} - {resultado.stderr} {resultado.stdout}")
            return None

            
        carpeta_destino = carpeta_oculta / carpeta_user.name

        i = 0
        while carpeta_destino.exists():
                if i == 0:
                    carpeta_destino = carpeta_oculta / f"{carpeta_user.name}_copy"
                
                else:
                    carpeta_destino = carpeta_oculta / f"{carpeta_user.name}_copy{i}"

                i += 1
        
        # print (carpeta_destino)
                    
        try:
            carpeta_user.rename(carpeta_destino)
            
            try:
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                self.logging.error(f"error al obtener la fecha: {e}")
                fecha = "Desconocida"
            
            id_file = uuid.uuid4().hex #generamos un id unico dificil de repetir
            
            nombre = carpeta_destino.name ## Nombre exacto con el que fue guardado (en caso de ser renombrada con copy para evitar fallas)
            
            metadatos = {"id":id_file, "app": "ORS4GHOST", "tipo": "carpeta", "nombre": nombre, "origen": str(carpeta_user), "fecha": fecha} 
                    
            ruta_metadatos = carpeta_destino / ".meta"
            
            try:
                with open (ruta_metadatos, "w", encoding="utf-8") as f_json:
                    json.dump(metadatos, f_json, indent=4, ensure_ascii=False)
                    
            except Exception as e:
                self.logging.error(f"error al crear el archivo de metadatos: {e} [{ruta_metadatos}]")
                
            try:
                metadatos_db = [(metadatos["id"], metadatos["tipo"], metadatos["nombre"], metadatos["origen"], metadatos["fecha"])]                    
                with sqlite3.connect (ruta_db_registro) as conn:
                    cursor = conn.cursor()
                    
                    cursor.executemany ("INSERT OR IGNORE INTO metadatos_db (id, tipo, nombre, origen, fecha) VALUES (?, ?, ?, ?, ?)", metadatos_db)
                    
                    if cursor.rowcount == 0:
                        self.logging.error(f"error al registrar la carpeta en la base de datos {id_file}")
                    
            except Exception as e:
                self.logging.error(f"error al registrar la carpeta en la base de datos: {e}")
                
            return True
        except Exception as e:
            self.logging.error(f"error al proteger la carpeta: {e}")
            return False

    def _proteger_archivo (self, archivo_user):
        
        """
        METODO PROTEGE ARCHIVO Y LO AGREGA A LA DB
        """
    
        archivo = Path(archivo_user).resolve() #para normalizar la ruta  y asegurar que sea absoluta y no una ruta falsa
        ruta_base = archivo.parent #SUBIMOS UN NIVEL

        carpeta_oculta = ruta_base / self.nombre_carpeta_baul
        carpeta_oculta.mkdir(parents=True, exist_ok=True) #creamos la carpeta oculta
        
        comando = ["attrib", "+h", "+s", f"{str(carpeta_oculta)}"]
        
        resultado = subprocess.run(comando, capture_output=True, text=True,creationflags=subprocess.CREATE_NO_WINDOW) #ocultamos la carpeta

        if resultado.returncode != 0:
            self.logging.error(f"error al ocultar la carpeta: {carpeta_oculta} - {resultado.stderr} - {resultado.stdout}")
            return None
        
        carpeta_destino = carpeta_oculta / archivo.name #RUTA DESTINO DEL ARCHIVO A OCULTAR colocamos el mismo nombre del archivo
        
        i = 0
        
        while carpeta_destino.exists(): #si existe un archivo con el mismo nombre le anexamos un "_copy"
            if i == 0:
                carpeta_destino = carpeta_oculta / f"{archivo.name}_copy"
            
            else:
                carpeta_destino = carpeta_oculta / f"{archivo.name}_copy{i}"

            i += 1
                    
        carpeta_destino.mkdir(parents=True, exist_ok=True) #creamos la carpeta con el nombre del archivo
        try:
            
            archivo.rename(carpeta_destino / archivo.name)
            
            try:
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                self.logging.error(f"error al obtener la fecha: {e}")
                fecha = "Desconocida"
            
            id_file = uuid.uuid4().hex #generamos un id unico dificil de repetir
            
            nombre =carpeta_destino.name # Nombre exacto con el que fue guardado (en caso de ser renombrada con copy para evitar fallas)
            
            metadatos = {"id":id_file, "tipo": "archivo", "nombre": nombre, "origen": str(archivo), "fecha": fecha}
                        
            ruta_metadatos = carpeta_destino / ".meta"
            
            try:
                with open (ruta_metadatos, "w", encoding="utf-8") as f_json:
                    json.dump(metadatos, f_json, indent=4, ensure_ascii=False)
            except Exception as e:
                self.logging.error(f"error al crear el archivo de metadatos: {e} [{ruta_metadatos}]")
        
            try:
                metadatos_db = [(metadatos["id"], metadatos["tipo"], metadatos["nombre"], metadatos["origen"], metadatos["fecha"])]
                
                with sqlite3.connect (ruta_db_registro) as conn:
                    cursor = conn.cursor()

                    cursor.executemany ("INSERT OR IGNORE INTO metadatos_db (id, tipo, nombre, origen, fecha) VALUES (?, ?, ?, ?, ?)", metadatos_db)
                    
                    if cursor.rowcount == 0:
                        self.logging.error(f"error al registrar la carpeta en la base de datos {id_file}")
                        
            except Exception as e:
                self.logging.error(f"error al registrar la carpeta en la base de datos: {e}")
        
        except Exception as e:
            self.logging.error(f"error al proteger la carpeta: {e}")
            return False
            
        return True

    def aplicar_proteccion (self, destino):

        if self._validar_carpeta(destino):
            
            if Path(destino).is_dir(): #si es una carpeta
                if self._proteger_carpeta(destino):
                    return True
                else:
                    return False
            
            elif Path(destino).is_file(): #si es un archivo
                if self._proteger_archivo(destino):
                    return True
                else:
                    return False
                
            else:
                return False

        else:
            return None

    def _buscar_carpetas_baul(self, origen):
        self.origen_user = Path(origen).resolve() #para normalizar la ruta  y asegurar que sea absoluta y no una ruta falsa
        carpeta_baul_existe = False
        if self.origen_user.exists():
            
            for carpeta in self.origen_user.iterdir():
                                
                if self.nombre_carpeta_baul != carpeta.name:
                    
                    carpeta_baul_existe = False
                    
                else:
                    carpeta_baul_existe = True
                    break
                
            if carpeta_baul_existe:
                
                for dir in carpeta.iterdir():
                    self.carpetas_en_baul.append(dir)
                
                return True
                
            else:
                self.logging.error(f"la carpeta {self.origen_user} no contiene ningun registro de proteccion para recuperar")
                return False
                    
        else:
            self.logging.error(f"la carpeta {self.origen_user} no existe")
            return False
        
    def _desproteger_carpeta(self):
        """
        METODO DESPROTEGE EL CONTENIDO DE UNA CARPETA
        """
        datos = ".meta"
        for carpeta in self.carpetas_en_baul:
            
            ruta_meta = carpeta / datos
            id = ""
            tipo = ""
            nombre = None
            if ruta_meta.exists():
                try:
                    with open (ruta_meta, "r", encoding="utf-8") as f_json:
                        metadatos = json.load(f_json)
                        try:
                            id = metadatos["id"]
                            tipo = metadatos["tipo"]
                            nombre = metadatos["nombre"]
                        except Exception as e:
                            self.logging.error(f"error de formato {e} [{ruta_meta}]")
                except Exception as e:
                    self.logging.error(f"error al leer el archivo de metadatos: {e} [{ruta_meta}]")
            
            try:

                if nombre:
    
                    destino = self.origen_user / nombre
                
                else:
                    destino = self.origen_user / carpeta.name

                if tipo == "archivo":
                    
                    try:
                        archivo = carpeta / nombre
                    except Exception as e:
                        self.logging.error(f"archivo no coincide con metadata posible modificación manual{e}")
                        continue
                    
                    nombre = Path(nombre)
                    i=0
                    
                    while destino.exists():
                        
                        if i == 0:
                            destino = self.origen_user / f"{nombre.stem}_copy{nombre.suffix}"
                            i += 1
                        elif i > 0:
                            destino = self.origen_user / f"{nombre.stem}_copy{i}{nombre.suffix}"
                            i += 1

                    archivo.rename(destino)
                    self.ids_en_baul.append(id)
                    
                    carpeta_con_meta = list(carpeta.iterdir())
                    if len(carpeta_con_meta) < 2:
                        
                        for f in carpeta_con_meta:
                            if f.name == datos:
                                try:
                                    shutil.rmtree(carpeta)
                                except Exception as e:
                                    self.logging.error(f"error al eliminar la carpeta: {e}")
                                
                else:
                    i=0
                    while destino.exists():
                        if i == 0:
                            destino = self.origen_user / f"{carpeta.name}_copy"
                            i += 1
                        elif i > 0:
                            destino = self.origen_user / f"{carpeta.name}_copy{i}"
                            i += 1
                    carpeta.rename(destino)
                    self.ids_en_baul.append(id)
                    
                    ruta_meta_destino = destino / datos
                    if ruta_meta_destino.exists():
                        try:
                            ruta_meta_destino.unlink()
                        except Exception as e:
                            self.logging.error(f"error al eliminar el archivo de metadatos: {e}")

            except Exception as e:
                self.logging.error(f"error al desproteger la carpeta: {e}")
        
    def actualizar_db(self):
        """
        METODO QUE UNICAMENTE (elimina registros) ACTUALIZA LA BASE DE DATOS DE REGISTRO
        """
        
        if ruta_db_registro.exists:
            
            if self.ids_en_baul == []:
                self.logging.error(f"No existen registros para eliminar en la db")
                return 
            
            cantidad_id = len(self.ids_en_baul)
            signos = ["?"] * cantidad_id
            signos = ",".join(signos)
            
            try:
                with sqlite3.connect (ruta_db_registro) as conn:
                    cursor = conn.cursor()
                    cursor.execute (f"DELETE FROM metadatos_db WHERE id IN ({signos})", self.ids_en_baul)
                
            except Exception as e:
                self.logging.error(f"error al actualizar la base de datos de registro: {e}")
                    
            
        else:
            self.logging.error(f"la base de datos de registro no existe")

    def desproteger_individual(self, ruta_elemento, nombre_elemento):
        """
        METODO DESPROTEGE UN ARCHIVO O CARPETA RECIBE LA RUTA ORIGEN Y EL NOMBRE QUE FUE ASIGNADO AL PROTEGER
        """
        
        datos = ".meta"
        
        ruta_elemento = Path(ruta_elemento).resolve()
        
        
        nombre_elemento = nombre_elemento #El nombre es usado ya que el archivo o carpeta puede ser renombrada automaticamente si esta ya existe y asi poder encontrar el archivo exacto
        
        ruta_elemento_oculto = ruta_elemento.parent / self.nombre_carpeta_baul / nombre_elemento #RUTA DEL ARCHIVO O CARPETA OCULTA
        
        # print (ruta_elemento_oculto)
        
        if ruta_elemento_oculto.exists():
            ruta_meta = ruta_elemento_oculto / datos
            id = ""
            tipo = ""
            nombre = None
            
            if ruta_meta.exists():
                
                try:
                    with open (ruta_meta, "r", encoding="utf-8") as f_json:
                        metadatos = json.load(f_json)
                        try:
                            id = metadatos["id"]
                            tipo = metadatos["tipo"]
                            nombre = ruta_elemento.name #Nombre exacto del archivo o carpeta original
                        except Exception as e:
                            self.logging.error(f"error de formato {e} [{ruta_meta}]")
                except Exception as e:
                    self.logging.error(f"error al leer el archivo de metadatos: {e} [{ruta_meta}]")
            
            if tipo == "archivo":
                if nombre:
                    origen = ruta_elemento_oculto / nombre
                    destino = ruta_elemento
                else:
                    origen = ruta_elemento_oculto
                    destino = ruta_elemento
                    self.logging.error(f"archivo no coincide con metadata posible modificación manual")

                try:
                    i =0
                    while destino.exists(): #si existe un archivo con el mismo nombre le anexamos un "_copy"
                        
                        if i == 0:
                            
                            destino =  ruta_elemento.parent /f"{ruta_elemento.stem}_copy{ruta_elemento.suffix}"
                            i += 1  
                        elif i > 0:
                            destino =  ruta_elemento.parent /f"{ruta_elemento.stem}_copy{i}{ruta_elemento.suffix}"
                            i += 1
                            
                    origen.rename(destino)
                    self.ids_en_baul.append(id)
                    
                    carpeta_con_meta = list(ruta_elemento_oculto.iterdir()) #convertimos a lista para poder calcular el tamano 

                    if len(carpeta_con_meta) < 2:
                        
                        for archivos in carpeta_con_meta:
                            
                            if archivos.name == datos:
                                try:
                                    carpeta = archivos.parent #retrocedemos un nivel para obtener la ruta de la carpeta del archivo
                                    shutil.rmtree(str(carpeta))

                                except Exception as e:
                                    self.logging.error(f"error al eliminar la carpeta: {e}")
                    return True
                
                except Exception as e:
                    self.logging.error(f"error al desproteger el archivo: {e}")
                    return False
            
            else:
                origen = ruta_elemento_oculto
                destino = ruta_elemento
                
                try:
                    i = 0
                    while destino.exists():
                        if i == 0:
                            destino = ruta_elemento.parent / f"{ruta_elemento.name}_copy"
                            i += 1
                        elif i > 0:
                            destino = ruta_elemento.parent / f"{ruta_elemento.name}_copy{i}"
                            i += 1
                    
                    origen.rename(destino)
                    self.ids_en_baul.append(id)
                    meta = destino / datos
                    if meta.exists():
                        
                        try:
                            meta.unlink()
                        except Exception as e:
                            self.logging.error(f"error al eliminar meta: {e}")
                            
                    return True
                except Exception as e:
                    self.logging.error(f"error al desproteger la carpeta: {e}")
                    return False
            
        else:
            self.logging.error(f"No se pudo encontrar el archivo o carpeta oculta {ruta_elemento_oculto.name}")
            return False
