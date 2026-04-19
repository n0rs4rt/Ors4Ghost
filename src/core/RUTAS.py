from pathlib import Path

rutas_inicial = Path(__file__).parents[1]

ruta_log = rutas_inicial / "LOGS"
ruta_log.mkdir(parents=True, exist_ok=True)

ruta_db = rutas_inicial / ".data_store"

ruta_db_registro = rutas_inicial / ".data_store2"


ruta_imagenes = rutas_inicial / "assets"

ruta_logo_ico = ruta_imagenes / "logo.ico"

ruta_logo_png = ruta_imagenes / "logo.png"

ruta_logo_alerta = rutas_inicial / "assets" / "alerta.png"
ruta_logo_error = rutas_inicial / "assets" / "error.png"

ruta_logo_acerca_de = rutas_inicial / "assets" / "acerca_de.png"
ruta_logo_github = rutas_inicial / "assets" / "github.png"
ruta_logo_instagram = rutas_inicial / "assets" / "instagram.png"
ruta_logo_youtube = rutas_inicial / "assets" / "youtube.png"




ruta_logo_carpeta_oculta = rutas_inicial / "assets" / "logo_ocultar.png"
ruta_logo_desocultar = rutas_inicial / "assets" / "logo_desocultar.png"