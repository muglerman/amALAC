from flask import Flask, render_template, request
import subprocess
import os
import telebot

app = Flask(__name__)


# Función para descargar música con gamdl
def descargar_musica(url):
    try:
        # Ejecutamos el comando gamdl para descargar la música
        comando = f'gamdl "{url}"'
        result = subprocess.run(comando, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')  # Output del comando
        return output  # Devuelve el nombre del archivo descargado
    except subprocess.CalledProcessError as e:
        return f"Error al ejecutar gamdl: {e.stderr.decode()}"



# Ruta principal: carga la página web
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para procesar la descarga
@app.route('/descargar', methods=['POST'])
def descargar():
    url = request.form.get('url')

    if not url:
        return "Por favor, introduce un enlace válido."

    # Descargar música usando gamdl
    archivo = descargar_musica(url)
    
    

# Configuración del servidor en Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
