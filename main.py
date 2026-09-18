import os
import pygame

# Inicializamos los subsistemas de Pygame de manera segura
pygame.init()

from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='assets', template_folder='assets')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/procesar_rostro', methods=['POST'])
def procesar_rostro():
    try:
        data = request.json
        imagen_data = data.get('imagen')
        return jsonify({
            'estatus': 'ok',
            'imagen_procesada': imagen_data 
        })
    except Exception as e:
        return jsonify({'estatus': 'error', 'mensaje': str(e)}), 500

if __name__ == '__main__':
    print("Iniciando servidor Flask local...")
    app.run(host='0.0.0.0', port=8080)
