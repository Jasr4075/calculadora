from flask import Flask, request, jsonify
import os
import sys

app = Flask(__name__)

# Ruta para la calculadora
@app.route('/')
def index():
    return open("src/index.html").read()

# Ruta para realizar los cálculos
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '')
    try:
        # Evaluar la expresión de forma segura
        result = eval(expression)
    except:
        result = 'Error'
    return jsonify({'result': result})

# Función para verificar la versión y actualizar
def verificar_versao_atual():
    url_versao = "http://seu-servidor.com/versao"  # URL de la versión actual
    versao_atual = "1.0"  # Versión local actual del app
    try:
        resposta = requests.get(url_versao)
        if resposta.status_code == 200:
            versao_remota = resposta.text.strip()
            if versao_remota != versao_atual:
                baixar_e_atualizar(versao_remota)
    except Exception as e:
        print("Error al verificar la version:", e)

# Función para bajar y actualizar el archivo (a completar según sea necesario)
def baixar_e_atualizar(nova_versao):
    print(f"Atualizando para a versao {nova_versao}")
    # Lógica de descarga y actualización

if __name__ == '__main__':
    verificar_versao_atual()  # Verificar si hay una versión nueva antes de iniciar el servidor
    app.run(debug=True, port=8080)  # Inicia el servidor en el puerto 8080
