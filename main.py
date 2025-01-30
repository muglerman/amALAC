import subprocess
import logging

# Configuración básica del logging para mostrar información en la consola
logging.basicConfig(level=logging.DEBUG)

def descargar_musica(link):
    try:
        logging.info(f"Iniciando la descarga para el enlace: {link}")

        # Ejecutamos el comando gamdl y capturamos tanto stdout como stderr
        result = subprocess.run(
            ['gamdl', link],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Si el proceso fue exitoso, result.returncode será 0
        if result.returncode == 0:
            logging.info(f"Descarga completada con éxito. Salida: {result.stdout}")
        else:
            # Si hubo un error, mostramos stderr con detalles del problema
            logging.error(f"Error durante la descarga. Detalles: {result.stderr}")

    except Exception as e:
        logging.error(f"Se produjo un error inesperado: {str(e)}")

# Ejemplo de uso
descargar_musica("https://music.apple.com/us/album/never-gonna-give-you-up-2022-remaster/1624945511?i=1624945512")
