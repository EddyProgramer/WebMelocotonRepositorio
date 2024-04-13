# melocoton_chat_bot.py

class ChatBot:
    def __init__(self):
        # Base de conocimientos inicial
        self.base_conocimientos = {
            "¿Cuál es tu nombre?": "Mi nombre es Melocotón Bot.",
            "¿Cuál es tu color favorito?": "Mi color favorito es el melocotón.",
            "¿Cómo estás?": "Estoy bien, ¡gracias por preguntar!"
        }

    def responder(self, mensaje):
        if mensaje in self.base_conocimientos:
            return self.base_conocimientos[mensaje]
        else:
            return "Lo siento, no tengo una respuesta para esa pregunta."
