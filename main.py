from flask import Flask, render_template, request
import subprocess
import logging

# Configuración básica de logging para capturar todos los logs
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Función para descargar música con gamdl
def descargar_musica(url):
    try:
        # Log de inicio del proceso de descarga
        logging.info(f"Iniciando la descarga para el enlace: {url}")

        # Ejecutar el comando gamdl
        comando = f'gamdl "{url}"'
        result = subprocess.run(comando, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Si la descarga fue exitosa, mostrar el resultado
        output = result.stdout.decode('utf-8')
        logging.info(f"Descarga completada con éxito. Salida: {output}")
        return output

    except subprocess.CalledProcessError as e:
        # Error al ejecutar el comando
        error_message = f"Error al ejecutar gamdl: {e.stderr.decode()}"
        logging.error(error_message)
        return error_message

    except Exception as e:
        # Excepción general
        error_message = f"Excepción general: {str(e)}"
        logging.error(error_message)
        return error_message

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/descargar', methods=['POST'])
def descargar():
    url = request.form.get('url')

    if not url:
        mensaje = "Por favor, introduce un enlace válido."
        logging.warning("Se intentó hacer una descarga sin enlace válido.")
        return render_template('index.html', mensaje=mensaje)

    # Descargar música usando gamdl
    archivo = descargar_musica(url)

    if archivo:
        mensaje = f"Descarga completada: {archivo}"
        logging.info(f"Descarga exitosa: {archivo}")
    else:
        mensaje = "Hubo un error al intentar descargar la música."
        logging.error("Error durante la descarga.")

    return render_template('index.html', mensaje=mensaje)

# Manejo de errores globales en Flask
@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Error interno en el servidor: {error}")
    return "Error interno del servidor. Reintenta más tarde.", 500

@app.errorhandler(404)
def not_found_error(error):
    logging.warning(f"Recurso no encontrado: {error}")
    return "Página no encontrada", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
