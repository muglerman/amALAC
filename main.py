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

@app.route('/descargar')
def descargar_musica():
    link = "https://music.apple.com/us/album/whenever-you-need-somebody-2022-remaster/1624945511"
    if not link:
        return "Por favor, proporciona un enlace válido", 400

    try:
        logging.info(f"Iniciando la descarga para el enlace: {link}")

        # Ejecutamos el comando gamdl y capturamos tanto stdout como stderr
        result = subprocess.run(
            ['gamdl', link, '--output', DOWNLOAD_FOLDER],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            logging.info(f"Descarga completada con éxito. Salida: {result.stdout}")
            return "Descarga completada con éxito", 200
        else:
            logging.error(f"Error durante la descarga. Detalles: {result.stderr}")
            return f"Error durante la descarga: {result.stderr}", 500

    except Exception as e:
        logging.error(f"Se produjo un error inesperado: {str(e)}")
        return f"Se produjo un error inesperado: {str(e)}", 500

# Verificar que el script se ejecute directamente
if __name__ == "__main__":
    app.run(debug=True)
