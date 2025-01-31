import os
import subprocess
import logging
from flask import Flask, request, send_from_directory

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración básica del logging para mostrar información en la consola
logging.basicConfig(level=logging.DEBUG)

# Directorio donde se almacenarán los archivos descargados
DOWNLOAD_FOLDER = './descargas'

# Asegúrate de que el directorio de descargas exista
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def hello_world():
    return '¡Hola Mundo! La aplicación está funcionando.'

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return "Archivo no encontrado", 404

import threading
import subprocess
import logging

# Función para ejecutar la descarga en segundo plano
def descargar_musica(link):
    try:
        logging.info(f"Iniciando la descarga para el enlace: {link}")
        result = subprocess.run(
            ['gamdl', '--output-path', '/tmp', link],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            logging.info(f"Descarga completada con éxito. Salida: {result.stdout}")
        else:
            logging.error(f"Error durante la descarga. Detalles: {result.stderr}")
    except Exception as e:
        logging.error(f"Se produjo un error inesperado: {str(e)}")

@app.route('/descargar')
def iniciar_descarga():
    link = "https://music.apple.com/us/album/whenever-you-need-somebody-2022-remaster/1624945511"
    # Ejecutar la descarga en un hilo separado
    threading.Thread(target=descargar_musica, args=(link,)).start()
    return "Descarga iniciada en segundo plano."


# Verificar que el script se ejecute directamente
if __name__ == "__main__":
    app.run(debug=True)
