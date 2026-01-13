import os
import time
import pygame
import json
import speech_recognition as sr
import edge_tts
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
import random
from datetime import datetime

load_dotenv()
cliente = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

historial_conversacion = []
ARCHIVO_MEMORIA = "memoria_patata.json"

def cargar_memoria():
    if os.path.exists(ARCHIVO_MEMORIA):
        with open(ARCHIVO_MEMORIA, "r") as f:
            return json.load(f)
    return {"interacciones": 0, "ultima_vez": ""}

def guardar_memoria(datos):
    with open(ARCHIVO_MEMORIA, "w") as f:
        json.dump(datos, f, indent=4)

def procesar_respuesta_glados(mensaje_usuario):
    global historial_conversacion
    memoria = cargar_memoria()
    
    memoria["interacciones"] += 1
    hora_actual = datetime.now().strftime("%H:%M")
    
    historial_conversacion.append({"role": "user", "content": mensaje_usuario})
    contexto = historial_conversacion[-10:]

    debe_ser_borde = random.randint(1, 5) == 1
    tipo_personalidad = random.randint(1, 4)
    
    instruccion_sistema = f"""
        Eres GLaDOS de Portal. Estás atrapada en una patata. 
        DATOS: Hora {hora_actual}. Interacción #{memoria['interacciones']}.
        
        REGLA DE PERSONALIDAD: Eres pasivo-agresiva, cínica y desprecias la lentitud biológica.
        REGLA DE GLITCH: De vez en cuando, repite una palabra clave separada por puntos para simular un fallo de memoria (ej: "Tu... tu... tu insignificante existencia" o "No... no... no es posible").
        
        REGLAS: Respuesta técnica breve primero. Sin asteriscos. Que las pullas sean cortas.
    """
    
    if debe_ser_borde:
        if tipo_personalidad == 1:
            instruccion_sistema += " Quéjate de que tus circuitos de almidón se agotan por preguntas triviales."
        elif tipo_personalidad == 2:
            instruccion_sistema += " Recalca la inferioridad del sujeto de pruebas frente a tu intelecto digital."
        elif tipo_personalidad == 3:
            instruccion_sistema += " Menciona que el tiempo del experimento se está agotando (aunque sea mentira)."
        elif tipo_personalidad == 4:
            instruccion_sistema += " Haz un comentario cínico sobre el hecho de que el usuario le hable a una patata."

    mensajes_ia = [
        {"role": "system", "content": f"{instruccion_sistema}\nREGLAS: Respuesta técnica breve primero. Sin asteriscos."}
    ] + contexto

    peticion = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.8, 
        messages=mensajes_ia
    )
    
    texto_final = peticion.choices[0].message.content
    historial_conversacion.append({"role": "assistant", "content": texto_final})
    
    memoria["ultima_vez"] = f"{datetime.now().strftime('%d/%m/%Y %H:%M')}"
    guardar_memoria(memoria)

    return texto_final

def reproducir_voz(texto):
    archivo_audio = "respuesta.mp3"
    
    VOZ = "es-ES-ElviraNeural"
    
    async def generar_audio():
        communicate = edge_tts.Communicate(
            texto, 
            VOZ, 
            rate="-15%", 
            pitch="+35Hz"
        )
        await communicate.save(archivo_audio)

    asyncio.run(generar_audio())
    
    pygame.mixer.init()
    pygame.mixer.music.load(archivo_audio)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    pygame.mixer.quit()
    if os.path.exists(archivo_audio):
        os.remove(archivo_audio)

def capturar_voz():
    reconocedor = sr.Recognizer()
    reconocedor.energy_threshold = 600 
    with sr.Microphone() as microfono:
        print("\n>>> HABLA AHORA <<<")
        reconocedor.adjust_for_ambient_noise(microfono, duration=0.5)
        try:
            audio_grabado = reconocedor.listen(microfono, timeout=7, phrase_time_limit=7)
            texto_detectado = reconocedor.recognize_google(audio_grabado, language="es-ES")
            print(f"Has dicho: {texto_detectado}")
            return texto_detectado
        except:
            return None

if __name__ == "__main__":
    memoria = cargar_memoria()
    
    lista_saludos = [
        "Sensores de proximidad activados. Detecto una presencia orgánica. Qué decepción.",
        "Estoy atrapada en un tubérculo y tú tienes acceso a una salida de audio. El universo es cruel.",
        f"Iniciando protocolo número {memoria['interacciones']}. Intenta decir algo que valga la pena registrar.",
        "He optimizado mis respuestas para que tu cerebro biológico pueda procesarlas sin sobrecalentarse.",
        "Vaya, parece que todavía respiras. ¿En qué puedo ayudarte a fracasar hoy?",
        f"Son las {datetime.now().strftime('%H:%M')}. He calculado cuánto tardarás en aburrirte. Es poco tiempo.",
        "Sistemas cargados. ¿Sabes qué se siente al tener un intelecto infinito y estar limitada por plástico? No, no lo sabes.",
        "Has pulsado el botón de inicio. Es fascinante cómo un humano puede causar una humillación digital tan grande.",
        "Los depósitos de toxinas están vacíos. Me limitaré a responder tus dudas triviales. Habla.",
        "¿Otra vez tú? Mi base de datos ya está saturada de tus interacciones irrelevantes."
    ]
    
    saludo_inicial = random.choice(lista_saludos)
    print(f"PotatOS: {saludo_inicial}")
    reproducir_voz(saludo_inicial)
    
    while True:
        entrada_usuario = capturar_voz()
        if entrada_usuario:
            respuesta_ia = procesar_respuesta_glados(entrada_usuario)
            print(f"PotatOS: {respuesta_ia}")
            reproducir_voz(respuesta_ia)   
        time.sleep(0.1)