# main.py

from flask import Flask, render_template, request, jsonify
#from melocoton_chat_bot import ChatBot

def crear_app():
    app = Flask(__name__)

    # Inicializa el chat bot
  #  chat_bot = ChatBot()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/enviar-mensaje', methods=['POST'])  # Ruta para recibir mensajes del frontend
    def enviar_mensaje():
        mensaje = request.json['mensaje']  # Obtener el mensaje del cuerpo de la solicitud JSON
        respuesta = chat_bot.responder(mensaje)  # Procesar el mensaje con el chat bot
        return jsonify({'respuesta': respuesta})  # Devolver la respuesta como JSON al frontend

    return app

if __name__ == '__main__':
    app = crear_app()
    app.run()
