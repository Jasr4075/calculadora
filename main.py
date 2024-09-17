import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# Función para obtener la versión local
def obtener_version_local():
    try:
        # Obtener el último tag local
        version_local = subprocess.check_output(["git", "describe", "--tags"]).strip().decode()
        return version_local
    except subprocess.CalledProcessError:
        return "No version"

# Función para obtener la última versión remota
def obtener_version_remota():
    try:
        # Actualiza la información remota
        subprocess.check_output(["git", "fetch", "--tags"])
        # Obtiene el último tag remoto
        version_remota = subprocess.check_output(["git", "describe", "--tags", "origin/main"]).strip().decode()
        return version_remota
    except subprocess.CalledProcessError:
        return "No version"

# Función para actualizar el repositorio si la versión está desactualizada
def actualizar_versao():
    version_local = obtener_version_local()
    version_remota = obtener_version_remota()

    if version_local != version_remota:
        print(f"Actualizando de la vesión {version_local} a la {version_remota}")
        try:
            # Hacer pull para traer los cambios
            subprocess.check_output(["git", "pull", "origin", "main"])
            # Reiniciar la aplicación si es necesario
            os.execl(sys.executable, sys.executable, *sys.argv)
        except subprocess.CalledProcessError as e:
            print(f"Error al actualizar: {e}")
    else:
        print(f"Ya está en la versión más reciente: {version_local}")

# Verificación de la versión antes de iniciar el servidor
actualizar_versao()

@app.route('/')
def index():
    return open("src/index.html").read()

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '')
    try:
        result = eval(expression)
    except:
        result = 'Error'
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
