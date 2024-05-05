import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.probability import FreqDist
from nltk.corpus import wordnet
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class ChatBot:
    def __init__(self):
        self.memoria = []
        self.stemmer = SnowballStemmer('spanish')

    def entrenar(self, datos_entrenamiento):
        for entrada, respuesta in datos_entrenamiento:
            self.memoria.append((entrada, respuesta))


    def responder(self, mensaje):
        respuesta = self.generar_respuesta(mensaje)
        self.memoria.append((mensaje, respuesta))
        return respuesta

    def preprocesar_texto(self, texto):
        tokens = word_tokenize(texto.lower()) # Convertir a minúsculas y tokenizar
        tokens = [t for t in tokens if t.isalnum()] # Eliminar signos de puntuación
        tokens = [self.stemmer.stem(t) for t in tokens] # Stemming
        tokens = [t for t in tokens if t not in set(stopwords.words('spanish'))] # Eliminar stopwords
        return tokens

    def generar_respuesta(self, mensaje):
       # respuesta = "Lo siento, no tengo una respuesta para esa pregunta."
        
        interacciones_usuario = self.obtener_interacciones_usuario(mensaje)
        respuestas_entrenamiento = [respuesta_entrenamiento for entrada_entrenamiento, respuesta_entrenamiento in datos_entrenamiento if entrada_entrenamiento == mensaje]
        
        if interacciones_usuario:
            respuesta = self.generar_respuesta_con_memoria(interacciones_usuario)
        elif respuestas_entrenamiento:
            respuesta = respuestas_entrenamiento[0]
            
        return respuesta


    def obtener_interacciones_usuario(self, mensaje):
        interacciones_usuario = []
        for i in range(len(self.memoria) - 1, -1, -1):
            print("Comparando mensaje:", mensaje)
            print("Mensaje en memoria:", self.memoria[i][0])
            if self.memoria[i][0] == mensaje:
                print("Coincidencia encontrada:", self.memoria[i][1])
                interacciones_usuario.append(self.memoria[i][1])
            else:
                print("No hay coincidencia. Salir del bucle.")
                break
        return interacciones_usuario


    def generar_respuesta_con_memoria(self, interacciones_usuario):
        palabras_usuario = [word for interaccion in interacciones_usuario for word in self.preprocesar_texto(interaccion)]
        frecuencia_palabras = FreqDist(palabras_usuario)
        palabras_comunes = frecuencia_palabras.most_common(3)
        
        respuesta = f"Basado en nuestras conversaciones anteriores, parece que estás interesado en {', '.join(palabra[0] for palabra in palabras_comunes)}. ¿Puedo ayudarte con algo relacionado con esto?"
        return respuesta

# Instanciamos el ChatBot
chatbot = ChatBot()

# Datos de entrenamiento (entrada del usuario, respuesta)
datos_entrenamiento = [
    ("Hola", "Hola, ¿en qué puedo ayudarte?"),
    ("¿Cómo estás?", "Estoy bien, gracias por preguntar."),
    ("¿Cuál es su horario de atención?", "Nuestro horario de atención es de lunes a viernes de 9:00 a.m. a 6:00 p.m."),
    ("¿Cómo puedo realizar un pedido?", "Puedes realizar un pedido a través de nuestra página web o llamando a nuestro número de teléfono."),
    # Agrega más ejemplos de entrenamiento aquí
]

# Entrenar al ChatBot
chatbot.entrenar(datos_entrenamiento)


# Bucle para esperar la entrada del usuario y responder
while True:
    mensaje = input("Escribe tu pregunta: ")
    respuesta = chatbot.responder(mensaje)
    print("ChatBot:", respuesta)
