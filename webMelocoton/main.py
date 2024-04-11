from flask import Flask, render_template, request, jsonify

def crear_app():
    app = Flask(__name__)

    # Aquí importa tu chat bot o implementa la lógica directamente
    # from mi_chat_bot import ChatBot

    # Ejemplo de una función de chat bot simple
    def chat_bot_respuesta(mensaje):
        return "¡Hola! Soy Melocotón Bot y recibí tu mensaje: " + mensaje

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/enviar-mensaje', methods=['POST'])  # Ruta para recibir mensajes del frontend
    def enviar_mensaje():
        mensaje = request.json['mensaje']  # Obtener el mensaje del cuerpo de la solicitud JSON
        respuesta = chat_bot_respuesta(mensaje)  # Procesar el mensaje con el chat bot
        return jsonify({'respuesta': respuesta})  # Devolver la respuesta como JSON al frontend

    return app

if __name__ == '__main__':
    app = crear_app()
    app.run()
