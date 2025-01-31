import os
import subprocess
import logging
from flask import Flask, send_from_directory

# Crear la aplicación Flask
app = Flask(__name__)

# Directorio de almacenamiento para los archivos descargados
DOWNLOAD_FOLDER = '/tmp/music_downloads'  # Directorio temporal donde se guardarán los archivos

# Crear el directorio si no existe
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def hello_world():
    return '¡Hola Mundo! La aplicación está funcionando.'

# Ruta para descargar el archivo
@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return "Archivo no encontrado", 404

# Función para descargar música
def descargar_musica(link):
    try:
        logging.info(f"Iniciando la descarga para el enlace: {link}")

        # Ejecutamos el comando gamdl y capturamos tanto stdout como stderr
        result = subprocess.run(
            ['gamdl', '--output-path', DOWNLOAD_FOLDER, link],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            logging.info(f"Descarga completada con éxito. Salida: {result.stdout}")

            # Suponiendo que el archivo se descargó correctamente, extraemos el nombre del archivo.
            filename = result.stdout.splitlines()[-1].split()[-1]  # Ajusta según la salida de gamdl

            logging.info(f"El archivo descargado es: {filename}")
            
            # Llamar a la ruta para descargar el archivo
            return download_file(filename)

        else:
            logging.error(f"Error durante la descarga. Detalles: {result.stderr}")
            return f"Hubo un error al descargar el archivo: {result.stderr}", 500

    except Exception as e:
        logging.error(f"Se produjo un error inesperado: {str(e)}")
        return f"Error inesperado durante la descarga: {str(e)}", 500

# Ruta para iniciar la descarga
@app.route('/descargar')
def iniciar_descarga():
    # Coloca el enlace de la música que deseas descargar
    enlace = "https://music.apple.com/us/album/whenever-you-need-somebody-2022-remaster/1624945511"
    return descargar_musica(enlace)

# Iniciar el servidor Flask
if __name__ == "__main__":
    app.run(debug=True)

