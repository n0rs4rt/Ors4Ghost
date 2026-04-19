import sqlite3, bcrypt, secrets , time, hashlib, logging
from pathlib import Path
from datetime import datetime
from core.RUTAS import *

class Usuario:
    def __init__ (self):
        self.logging = logging.getLogger("LOGS")
        self.nombre_user = None
        self.password = None
        self.fecha_creacion = None
        self.fecha_ultimo_acceso = None #guarda la ultima fecha de acceso en la db
        self.acceso = None #MUESTRA EL ULTIMO ACCESO
        self.key_recovery = None
        
        self.key_recovery_hash = None
        
        self.hash_db = None
        self.db_modif = False
        

    def verificar_db(self):
        """Verifica si la base de datos existe"""
        
        if ruta_db.exists():
            return True
        else:
            return False
        
    def crear_usuario(self, nombre_user, password):
        """Crea un nuevo usuario"""
        
        self.nombre_user = str(nombre_user).lower() #nombre de usuario
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.fecha_ultimo_acceso = ""
        
        try:
            self.key_recovery = secrets.token_hex(8) #llave de recuperacion
        
            pass_bytes = str(password).encode("utf-8") #pasamos la clave a bytes
            salt_pass = bcrypt.gensalt() #generamos el salt
            
            self.password = bcrypt.hashpw(pass_bytes, salt_pass).decode("utf-8") #obtenemos el hash en string
        
            key_bytes = self.key_recovery.encode("utf-8")
            salt_key = bcrypt.gensalt()
            self.key_recovery_hash = bcrypt.hashpw(key_bytes, salt_key).decode("utf-8") #hash d la llave de recuperacion
            
            
            hash_db = f"ors4_{self.nombre_user}_{self.password}_{self.key_recovery_hash}"
            
            self.hash_db = hashlib.sha256(hash_db.encode("utf-8")).hexdigest()
    
            # print ("hasdb: ", self.hash_db)

            return True
            
        except Exception as e:
            self.logging.error(f"error de cifrado: {e}")
            return False
        
        
    def crear_db(self):
        
        """Crea la base de datos con los datos del usuario"""
        
        credenciales_user =[(self.nombre_user, self.password, self.key_recovery_hash, self.fecha_creacion, self.fecha_ultimo_acceso, self.hash_db)]
        try:
            with sqlite3.connect(ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("""
                                CREATE TABLE IF NOT EXISTS USUARIOS (
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    NOMBRE_USER TEXT,
                                    PASSWORD TEXT,
                                    KEY_RECOVERY TEXT,
                                    FECHA_CREACION TEXT,
                                    FECHA_ULTIMO_ACCESO TEXT,
                                    ID_DB TEXT 
                                )
                                """)
                cursor.executemany ("INSERT OR IGNORE INTO USUARIOS (NOMBRE_USER, PASSWORD, KEY_RECOVERY, FECHA_CREACION, FECHA_ULTIMO_ACCESO, ID_DB) VALUES (?, ?, ?, ?, ?, ?)", credenciales_user)
                
                if cursor.rowcount == 0:
                    return False
            return True
        
        except Exception as e:
            self.logging.error(f"error al crear la base de datos: {e}")
            return False
    

    def _db_manipulada(self,nombre_user, hash_password, hash_key_recovery, id_db):
        
        """Verifica si la base de datos fue manipulada
        este metodo se usa unicamente en el login"""
        
        db_id = f"ors4_{nombre_user}_{hash_password}_{hash_key_recovery}"
        
        has_db = hashlib.sha256(db_id.encode("utf-8")).hexdigest()
        
        # print ("hasdb: ", has_db)
        
        if has_db == id_db:
            return False
        else:
            return True
        
    
    def _registro_ultimo_acceso(self):
        
        """Guarda la ultima fecha de acceso en la db
        este metodo se usa unicamente en el login"""
        
        acceso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("UPDATE usuarios SET fecha_ultimo_acceso = ? WHERE id = ?", (acceso, 1))
            
            return acceso
        
        except Exception as e:
            self.logging.error(f"Error al actualizar el ultimo acceso: {e}")
            return False

    def login (self, user, password):
        
        """Verifica si el usuario y la password son correctos
        si la base de datos fue manipulada
        y registra la ultima fecha de acceso
        """
        self.nombre_user = None #Las llamamos nuevamente para que se inicialicen cuand se llame el metodo en la interfaz
        self.password = None
        
        nombre_user = str(user).lower()
        password = str(password)
        
        try:
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("SELECT nombre_user, password, key_recovery, fecha_ultimo_acceso, id_db FROM usuarios")
                datos_db = cursor.fetchall()
        except Exception as e:
            self.logging.error(f"error al acceder a la base de datos: {e}")
            return None
        
        try:
            
            user_db = datos_db[0][0]
            pass_db = datos_db[0][1]
            key_recovery = datos_db[0][2]
            self.acceso = datos_db[0][3]
            id_db = datos_db[0][4]
            # print(user_db, pass_db)
            
            ##convertimos a bytes
            pass_db_bytes = pass_db.encode("utf-8") #password de la db
            password_bytes = password.encode("utf-8") #password qque el usuario ingresa
            

            if nombre_user == user_db:
                self.nombre_user = True
            
            if bcrypt.checkpw(password_bytes, pass_db_bytes): #verificamos la password
                self.password = True
                
            if self.password and self.nombre_user:
                
                self.db_modif =self._db_manipulada(user_db, pass_db, key_recovery, id_db)
                if self.db_modif:
                    self.logging.warning("La base de datos fue modificada - Acceso denegado")
                    return None
                            
                self._registro_ultimo_acceso()
                
                return True
            else:
                return False
        
        except Exception as e:
            self.logging.error(f"error al acceder a la base de datos: {e}")
            return None

    def reset_db(self, key):
        
        """Resetea la base de datos"""
        
        key = str(key).encode("utf-8")
        if not ruta_db.exists():
            self.logging.warning("La base de datos no existe")
            return None
        try:
            with sqlite3.connect (ruta_db) as conn:
                cursor = conn.cursor()
                cursor.execute ("SELECT key_recovery FROM usuarios")
                datos_db = cursor.fetchall()
        except Exception as e:
            self.logging.error(f"error al acceder a la base de datos: {e}")
            return None
        
        conn.close() #forzar la desconexión
        
        try:
            key_db = datos_db[0][0]
            
            key_db_bytes = key_db.encode("utf-8")
            
            if bcrypt.checkpw(key, key_db_bytes):
                
                ruta_db.unlink()
                self.logging.warning("Credenciales de usuario reseteadas")
                
                return True
            else:
                self.logging.warning("Intento de reseteo de credenciales fallido")
                return False
            
        except Exception as e:
            self.logging.error(f"error al acceder a la base de datos: {e}")
            return None

