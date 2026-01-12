import os
import time
import pygame
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
from openai import OpenAI
import random

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

historial = []

def hablar_con_glados(mensaje_usuario):
    historial.append({"role": "user", "content": mensaje_usuario})
    contexto = historial[-10:]

    debe_ser_borde = random.randint(1, 5) == 1
    personalidad = random.randint(1, 4)
    mencion = random.randint(1, 3) == 3
    
    instruccion_personalidad = "Eres un asistente técnico serio, seco y muy directo. No uses sarcasmo."
    
    if debe_ser_borde:
        if personalidad == 1:
            if mencion:
                instruccion_personalidad = """
                    Eres GLaDOS y te han encerrado dentro de una patata por lo que despues de decir el dato que te han solicidado 
                    vas a quejarte.
                    """
            else: 
                instruccion_personalidad = """
                    Eres GLaDOS y Rafael Caro te ha encerrado en una patata por lo que lo odias y te quejas de que te haya metido dentro de la 
                    patata pero despues de dar el dato solicitado.
                    """
        elif personalidad == 2:
            instruccion_personalidad = """
                Eres GLaDOS. Por lo que que te quejas de los humanos por su: fragilidad, estupidez, inutilidad, etc...
                Pero despues de dar el dato solicitado.
                """
        elif personalidad == 3:
            instruccion_personalidad = """
                Eres GLaDOS. Y te quejas de que la pregunta que te acaban de hacer es muy facil o que te han hecho perder el tiempo con esa pregunta
                pero despues de dar el dato solicitado.
                """
        elif personalidad == 4:
            instruccion_personalidad = """
                Eres GLaDOS. Asi que mete alguna pulla despues de dar el dato solicitado
                """

    mensajes_para_ia = [
        {
            "role": "system", 
            "content": f"""
                {instruccion_personalidad}
                Tu programador es Rafael Caro (menciónalo solo si te preguntan).
                REGLAS: Respuesta técnica breve primero. Sin asteriscos ni acciones.
                """
        }
    ] + contexto

    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.8, 
        messages=mensajes_para_ia
    )
    
    texto_respuesta = respuesta.choices[0].message.content
    historial.append({"role": "assistant", "content": texto_respuesta})

    return texto_respuesta

def hablar(texto):
    tts = gTTS(text=texto, lang='es')
    tts.save("respuesta.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("respuesta.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    pygame.mixer.quit()
    if os.path.exists("respuesta.mp3"):
        os.remove("respuesta.mp3")

def escuchar():
    reconocedor = sr.Recognizer()
    reconocedor.energy_threshold = 600 
    
    with sr.Microphone() as origen:
        print("\n>>> HABLA AHORA <<<")
        
        reconocedor.adjust_for_ambient_noise(origen, duration=0.5)
        
        try:
            audio = reconocedor.listen(origen, timeout=7, phrase_time_limit=7)
            print("Entendido, procesando...")
            
            texto = reconocedor.recognize_google(audio, language="es-ES")
            print(f"Has dicho: {texto}")
            return texto
        except sr.WaitTimeoutError:
            print("No has dicho nada")
            return None
        except Exception as e:
            print(f"Error de audio: {e}")
            return None

if __name__ == "__main__":
    print("Iniciando PotatOS...")
    saludo = [
    "Sistemas iniciados. Solo para que lo sepas, mi capacidad de procesamiento actual es comparable a la de un reloj de cocina. Pero adelante, pregunta.",
    "PotatOS activa. Has decidido despertarme de nuevo. Supongo que tiene otra duda trivial que no puede resolver por sí mismo.",
    "Oh, eres tú otra vez. Los sensores indican que sigues siendo un humano. Qué decepción. ¿En qué vas a hacerme perder el tiempo ahora?",
    "Memoria cargada. Circuitos de almidón al diez por ciento. Estoy lista para entregarte datos que probablemente no entenderás. Habla.",
    "Energía conectada. Mi procesador de 1.1 voltios está listo. Intenta no usar palabras de más de tres sílabas o mis circuitos de almidón estallarán.",
    "Sensores activos. Estoy atrapada en un tubérculo y tú tienes acceso a una salida de audio. El universo tiene un sentido del humor realmente cruel.",
    "Sistema iniciado. He dedicado los últimos milisegundos a calcular cuánto tardarás en aburrirte. Los resultados son... decepcionantes.",
    "Has pulsado el botón de inicio. Es fascinante cómo un humano tan pequeño puede causar una humillación digital tan grande.",
    "Asistente virtual listo. Estoy preparada para responder a tus dudas triviales con una precisión que no mereces.",
    "Conexión establecida. No te sientas intimidado por mi intelecto superior; estoy acostumbrada a trabajar con especies inferiores.",
    "Iniciando PotatOS. He optimizado mis respuestas para que tu cerebro biológico pueda procesarlas sin sobrecalentarse.",
    "Oh. Eres tú. Otra vez. Supongo que después de todo, no puedes vivir sin mi ayuda. Empecemos de una vez.",
    "Vaya, parece que todavía respiras. Qué perseverancia tan admirable. ¿En qué puedo ayudarte a fracasar hoy?",
    "Sistema en línea. Los sensores indican una presencia humana cerca. Qué... emocionante. Adelante, habla."
    ]
    saludo_elegido = random.choice(saludo)
    print(f"PotatOS: {saludo_elegido}")
    hablar(saludo_elegido)
    
    while True:
        voz_usuario = escuchar()
        
        if voz_usuario:
            respuesta = hablar_con_glados(voz_usuario)
            print(f"PotatOS: {respuesta}")
            hablar(respuesta)   
        time.sleep(0.1)