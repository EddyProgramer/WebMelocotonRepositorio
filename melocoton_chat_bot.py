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
        self.umbral_similitud = 0.7
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
            }
            # Agregar más productos y sus preguntas y respuestas asociadas aquí
        }

    def entrenar(self, datos_entrenamiento):
        for pregunta, respuesta in datos_entrenamiento:
            self.preguntas_entrenamiento.append(pregunta)
            self.memoria.append(respuesta)

        self.vectorizer.fit(self.preguntas_entrenamiento)

        for producto, info_producto in self.productos.items():
            for pregunta_producto, respuesta_producto in zip(info_producto["preguntas"], info_producto["respuestas"]):
                self.preguntas_entrenamiento.append(pregunta_producto)
                self.memoria.append(respuesta_producto)

    def responder(self, mensaje):
        if not hasattr(self.vectorizer, 'vocabulary_'):
            return "Lo siento, el ChatBot no está listo para responder. Por favor, entrena al ChatBot antes de usarlo."

        pregunta_vectorizada = self.vectorizer.transform([mensaje])
        similitudes = cosine_similarity(pregunta_vectorizada, self.vectorizer.transform(self.preguntas_entrenamiento))[0]
        max_similitud_idx = np.argmax(similitudes)

        max_similitud = 0
        pregunta_mas_similar = None
        respuesta_producto = None
        for producto, info_producto in self.productos.items():
            for pregunta_producto, respuesta_producto in zip(info_producto["preguntas"], info_producto["respuestas"]):
                similitud = SequenceMatcher(None, mensaje.lower(), pregunta_producto.lower()).ratio()
                if similitud > max_similitud:
                    max_similitud = similitud
                    pregunta_mas_similar = pregunta_producto
                    respuesta_producto = respuesta_producto

        if max_similitud > self.umbral_similitud:
            return respuesta_producto

        return self.memoria[max_similitud_idx]

    def preprocesar_texto(self, texto):
        tokens = word_tokenize(texto.lower())
        tokens = [t for t in tokens if t.isalnum()]
        tokens = [self.stemmer.stem(t) for t in tokens]
        tokens = [t for t in tokens if t not in set(stopwords.words('spanish'))]
        return tokens

