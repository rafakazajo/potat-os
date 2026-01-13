# PotatOS v1.0
### Rafael Caro

Esto es un asistente virtual que tiene la personalidad de GlaDOS usando el api de Groq

---

## Como funciona

Esta dividido en 4 bloques

### Imports
Primero tenemos que importar y descargar todos los paquetes necesarios para poder:
* Buscar rutas y poder modificarlas en el pc **import os**
* Poder ponerle un tiempo de espera para que no se sature la CPU **import time**
* Reproducir los textos por los altavoces **import pygame**
* Escuchar tu voz por el microfono **import speech_recognition**
* Transcribir los textos con Google **import gtts**
* Importar las keys **import dotenv**
* Importar la IA de OpenAI ya que Groq usa el mismo lenguaje **import openai**.
* Tenemos la opcion de que sea aleatoria sus acciones **import random**

### Conexion con la IA
Llamamos a la key que tenemos guardada en el .env y usamos los servidores de Groq en vez de los de OpenAI ya que usan el mismo lenguaje.

### Personalidad del asistente
Le he dado al asiste una personalidad parecida al GlaDOS del juego Portal, tambien tiene memoria corta pero suficiente para que recuerde la conversacion y pueda usarla para responder.

###  Hablar con el asistente
Para poder hablar con el asistente lo que hace es que creamos un archivo mp3 con el texto que le entrega la IA que se reproduce y posteriormente se elimina para que no ocupe espacio.

### La escucha del asistente
Lo que hace el asistente para escuchar es activar nuestro microfono y darnos un tiempo para que podamos realizar nuestra pregunta.

### El final
Por ultimo se inician todas las funciones creadas anteriormente y se invita al usuario a que hable.

![PotatOS](/assets/GlaDOS.png)

# PotatOS v1.1
## Rafael Caro

Cambios de los nombres de las variables e implementacion de conciencia del tiempo, le he cambiado de gtts al edge_tts y memoria almacenada a largo plazo.

---

# Imports
* Puede ver la hora actual **import datetime**
* Escribe la conversaciones para acordares **import json**
* Tiene una voz diferente **import edge_tts**
* Reproduce de forma asincrona **import asyncio**

### Cambio de voz
He cambiado el reproductor de voz para poder hacerlo mas agudo y en vez de usar el reproductor de Google ahora usa el de Microsoft y para poder reproducirlo hay que hacerlo de forma asincrona para poder generar el mp3

### Cambio de nombres
He hecho un cambio en los nombres de las variables ya que me es mas facil acodarme del nombre.

### El tiempo
Ahora tiene importado el tiempo para que ahora sepa cual es la hora actual y las respuestas sean mas actuales.

### Memoria
Le he añadido la opcion de guardar la conversacion en un .json para que el asistente sepa la cantidad de interacciones que ha tenido con el ususario y que tenga mas memoria.