# PotatOS
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