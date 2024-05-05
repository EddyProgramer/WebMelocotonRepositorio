import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from difflib import SequenceMatcher

nltk.download('punkt')
nltk.download('stopwords')

class ChatBot:
    def __init__(self):
        self.umbral_similitud = 0.7  # Definir un umbral de similitud adecuado
        self.memoria = []
        self.stemmer = SnowballStemmer('spanish')
        self.vectorizer = TfidfVectorizer(tokenizer=self.preprocesar_texto)
        self.preguntas_entrenamiento = []
        self.productos = {
            "melocoton residencias": {
                "preguntas": [
                    "caracteristicasR",
                    "precio de los planes",
                    "disponen de alguna promocion"
                ],
                "respuestas": [
                    "administracion eficiente de las tareas y gastos del hogar.",
                    "El precio de los planes es el siguiente: Plan Semilla $50.40,plan Durazno $60.40,plan Cosecha $71.20.",
                    "si tenemos un 5% de descuento si llegas desde nuestra pagina de facebook."
                ]
            },
            "melocoton pets": {
                "preguntas": [
                    "característicasP",
                     "precio de los planes",
                    "disponen de alguna promocion"
                ],
                "respuestas": [
                     "administracion eficiente de las tareas y gastos del hogar.",
                    "El precio de los planes es el siguiente: Plan Semilla $50.40,plan Durazno $60.40,plan Cosecha $71.20.",
                    "si tenemos un 5% de descuento si llegas desde nuestra pagina de facebook."
                ]
            },
            # Agregar más productos y sus preguntas y respuestas asociadas aquí
        }

    def entrenar(self, datos_entrenamiento):
        for pregunta, respuesta in datos_entrenamiento:
            self.preguntas_entrenamiento.append(pregunta)
            self.memoria.append(respuesta)

        self.vectorizer.fit(self.preguntas_entrenamiento)

        # Agregar preguntas relacionadas con productos al conjunto de entrenamiento
        for producto, info_producto in self.productos.items():
            for pregunta_producto, respuesta_producto in zip(info_producto["preguntas"], info_producto["respuestas"]):
                self.preguntas_entrenamiento.append(pregunta_producto)
                self.memoria.append(respuesta_producto)

    def responder(self, mensaje):
        pregunta_vectorizada = self.vectorizer.transform([mensaje])
        similitudes = cosine_similarity(pregunta_vectorizada, self.vectorizer.transform(self.preguntas_entrenamiento))[0]
        max_similitud_idx = np.argmax(similitudes)

        print("Índice de mayor similitud:", max_similitud_idx)
        print("Similitudes:", similitudes)

        # Verificar si la pregunta es sobre productos
        max_similitud = 0
        pregunta_mas_similar = None
        respuesta_producto = None
        for producto, info_producto in self.productos.items():
            for pregunta_producto, respuesta_producto in zip(info_producto["preguntas"], info_producto["respuestas"]):
                similitud = SequenceMatcher(None, mensaje.lower(), pregunta_producto.lower()).ratio()
                print("Pregunta del usuario:", mensaje.lower())
                print("Pregunta del producto:", pregunta_producto.lower())
                print("Similitud:", similitud)
                if similitud > max_similitud:
                    max_similitud = similitud
                    pregunta_mas_similar = pregunta_producto
                    respuesta_producto = respuesta_producto

        print("Máxima similitud encontrada:", max_similitud)
        print("Pregunta más similar:", pregunta_mas_similar)

        if max_similitud > self.umbral_similitud:
            # Si se encontró una pregunta similar, devolver la respuesta correspondiente
            return respuesta_producto

        # Si no se encontró una pregunta similar, devolver la respuesta general
        return self.memoria[max_similitud_idx]



    def preprocesar_texto(self, texto):
        tokens = word_tokenize(texto.lower()) # Convertir a minúsculas y tokenizar
        tokens = [t for t in tokens if t.isalnum()] # Eliminar signos de puntuación
        tokens = [self.stemmer.stem(t) for t in tokens] # Stemming
        tokens = [t for t in tokens if t not in set(stopwords.words('spanish'))] # Eliminar stopwords
        return tokens

# Instanciamos el ChatBot
chatbot = ChatBot()

# Datos de entrenamiento (pregunta del usuario, respuesta)
datos_entrenamiento = [
    ("Hola", "Hola, ¿en qué puedo ayudarte?"),
    ("Buenos dias", "Buenos dias, ¿en qué puedo ayudarte?"),
    ("Buenas Tardes", "Buenas tardes, ¿en qué puedo ayudarte?"),
    ("Buenas noches", "Buenas noches, ¿en qué puedo ayudarte?"),
    ("Cómo estás", "Estoy bien, gracias por preguntar."),
    ("Cómo estás", "Estoy bien, gracias por preguntar."),
    ("¿Cuál es su horario de atención?", "Nuestro horario de atención es de lunes a viernes de 9:00 a.m. a 6:00 p.m."),
    ("¿Cómo puedo realizar un pedido?", "Puedes realizar un pedido a través de nuestra página web o llamando a nuestro número de teléfono."),
    # preguntas productos
    ("que productos disponen", "disponemos de: Melocoton residencias,Melocoton Reservas en cual estas interesado?"),
    ("Melocoton residencias", "es el plan perfecto para tu hogar y mantenerlo controlado y gestionado deseas mas informacion del mismo digita: caracteristicasR"),
    # Agrega más ejemplos de entrenamiento aquí
]

# Entrenar al ChatBot
chatbot.entrenar(datos_entrenamiento)

# Bucle para esperar la entrada del usuario y responder
while True:
    mensaje = input("Escribe tu pregunta: ")
    
    # Verificar si la entrada del usuario está vacía
    if not mensaje.strip():
        print("Por favor, ingresa una pregunta.")
        continue
    
    # Responder a las solicitudes de ayuda
    if mensaje.strip().lower() in ["ayuda", "help"]:
        print("Puedes hacerme preguntas sobre nuestros productos o servicios.")
        continue
    
    # Responder a preguntas irrelevantes
    if not any(pregunta.lower() in mensaje.lower() for pregunta in chatbot.preguntas_entrenamiento):
        print("Lo siento, no puedo responder a esa pregunta.")
        continue
    
    # Obtener respuesta del chatbot
    respuesta = chatbot.responder(mensaje)
    print("ChatBot:", respuesta)
