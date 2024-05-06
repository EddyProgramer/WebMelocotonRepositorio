from flask import Flask, render_template, request, jsonify
from melocoton_chat_bot import ChatBot

def crear_app():
    app = Flask(__name__)
    
    # Inicializa el chat bot
    chat_bot = ChatBot()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/enviar-mensaje', methods=['POST'])  # Ruta para recibir mensajes del frontend
    def enviar_mensaje():
        mensaje = request.json['mensaje']  # Obtener el mensaje del cuerpo de la solicitud JSON
        
        # Verificar si el ChatBot está entrenado
        if not chat_bot.memoria:
            return jsonify({'respuesta': "Lo siento, el ChatBot no está listo para responder. Por favor, entrena al ChatBot antes de usarlo."})
        
        # Responder con el ChatBot
        respuesta = chat_bot.responder(mensaje)  
        return jsonify({'respuesta': respuesta})  

    # Entrenar al ChatBot con datos de entrenamiento
    datos_entrenamiento = [
        ("Hola", "Hola, ¿en qué puedo ayudarte?"),
        ("Buenos días", "Buenos días, ¿en qué puedo ayudarte?"),
        ("Buenas tardes", "Buenas tardes, ¿en qué puedo ayudarte?"),
        ("Buenas noches", "Buenas noches, ¿en qué puedo ayudarte?"),
        ("¿Cómo estás?", "Estoy bien, gracias por preguntar."),
        ("¿Cuál es su horario de atención?", "Nuestro horario de atención es de lunes a viernes de 9:00 a.m. a 6:00 p.m."),
        ("¿Cómo puedo realizar un pedido?", "Puedes realizar un pedido a través de nuestra página web o llamando a nuestro número de teléfono."),
        ("¿Qué métodos de pago aceptan?", "Aceptamos pagos con tarjeta de crédito, transferencia bancaria y PayPal."),
        ("¿Cuánto tiempo tarda en llegar mi pedido?", "El tiempo de entrega depende de tu ubicación y del tipo de envío seleccionado. Normalmente, tarda entre 3 y 5 días hábiles."),
        ("¿Ofrecen envío internacional?", "Sí, ofrecemos envío internacional a la mayoría de los países. Los costos y tiempos de entrega pueden variar."),
        ("¿Tienen política de devolución?", "Sí, tenemos una política de devolución de 30 días. Si no estás satisfecho con tu compra, puedes devolver el producto y te reembolsaremos el dinero."),
        ("¿Puedo cancelar mi pedido?", "Sí, puedes cancelar tu pedido antes de que sea enviado. Ponte en contacto con nuestro equipo de atención al cliente para obtener ayuda."),
        ("¿Cómo puedo contactar al servicio al cliente?", "Puedes contactar a nuestro servicio al cliente llamando a nuestro número de teléfono o enviando un correo electrónico a nuestro equipo de soporte."),
        ("¿Tienen atención al cliente en otros idiomas?", "Sí, ofrecemos atención al cliente en varios idiomas. Por favor, indícanos tu idioma preferido y te ayudaremos en ese idioma."),
        ("¿Tienen algún programa de recompensas o fidelización?", "Sí, tenemos un programa de fidelización donde acumulas puntos con cada compra que luego puedes canjear por descuentos en futuras compras."),
        ("¿Tienen servicio de instalación o soporte técnico?", "Sí, ofrecemos servicios de instalación y soporte técnico para nuestros productos. Ponte en contacto con nosotros para más información."),
        ("¿Tienen alguna promoción o descuento disponible?", "Sí, tenemos promociones y descuentos especiales en determinadas épocas del año. Te recomendamos que te suscribas a nuestra lista de correo para recibir nuestras ofertas."),
        ("¿Ofrecen garantía en sus productos?", "Sí, ofrecemos garantía en todos nuestros productos contra defectos de fabricación. Si tienes algún problema, por favor, ponte en contacto con nosotros para que podamos ayudarte."),
        ("¿Pueden personalizar un pedido según mis necesidades?", "Sí, ofrecemos servicios de personalización para adaptar nuestros productos a tus necesidades específicas. Ponte en contacto con nuestro equipo de ventas para más detalles.")
    
        # Añade más ejemplos de entrenamiento aquí
    ]
    chat_bot.entrenar(datos_entrenamiento)  # Entrenar al ChatBot

    return app

if __name__ == '__main__':
    app = crear_app()
    app.run()
