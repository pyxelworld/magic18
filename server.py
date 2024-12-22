from __future__ import annotations
import os
from typing import AsyncIterable
import fastapi_poe as fp
from modal import App, Image, asgi_app
import google.generativeai as genai

# Configurar a API do Google
genai.configure(api_key="AIzaSyCuKxOa7GoY6id_aG-C3_uhvfJ1iI0SeQ0")

class WrapperBot(fp.PoeBot):
    async def get_response(self, request: fp.QueryRequest) -> AsyncIterable[fp.PartialResponse]:
        # Coletar mensagens do usuário
        messages = []
        for query in request.query[-5:]:
            messages.append({"role": query.role, "content": query.content[:50]})

        # Enviar mensagem para o modelo do Google e obter resposta
        chat_session = model.start_chat(history=messages)
        response = chat_session.send_message(request.query[-1].content)
        
        yield fp.PartialResponse(text=response.text)

# Configurar requisitos e imagem
REQUIREMENTS = ["fastapi-poe==0.0.48", "google-generativeai"]
image = (
    Image.debian_slim()
    .pip_install(*REQUIREMENTS)
    .env({
        "POE_ACCESS_KEY": "W4CgtzW6XzMBfvM8rAl8xSzYfeUzTlte",
        "GEMINI_API_KEY": "AIzaSyCuKxOa7GoY6id_aG-C3_uhvfJ1iI0SeQ0",
    })
)

app = App("wrapper-bot-poe")

@app.function(image=image)
@asgi_app()
def fastapi_app():
    bot = WrapperBot()
    app = fp.make_app(bot, access_key="uYr6O0dKHvgSH2nxLvQe4O8dCs0kPo31", bot_name="MagicServer")
    return app
