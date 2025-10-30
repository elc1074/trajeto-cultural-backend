import os
import io
import requests
import google.generativeai as genai
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente.")

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.8,
    "max_output_tokens": 256,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

router = APIRouter(prefix="/analise", tags=["Análise com Gemini"])

class AnaliseRequest(BaseModel):
    image_url: str | None = None
    mensagem: str | None = None


@router.post("/gemini")
async def analisar_obra(req: AnaliseRequest):
    try:
        if req.image_url:
            print(f"📸 Baixando imagem de: {req.image_url}")

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36"
            }

            response = requests.get(req.image_url, headers=headers, timeout=10)
            response.raise_for_status()

            image_bytes = io.BytesIO(response.content)
            image_bytes.name = "obra.jpg"

            print("📤 Enviando imagem ao Gemini...")

            prompt = (
                "Analise a imagem e escreva uma frase curta e criativa "
                "em português que descreva o estilo e o sentimento da obra."
            )

            gemini_response = model.generate_content(
                [
                    {"mime_type": "image/jpeg", "data": image_bytes.getvalue()},
                    prompt,
                ]
            )

            texto = None
            try:
                if gemini_response.candidates:
                    parts = gemini_response.candidates[0].content.parts
                    if parts and hasattr(parts[0], "text"):
                        texto = parts[0].text
            except Exception as e:
                print("⚠️ Erro ao ler texto:", e)

            if hasattr(gemini_response.candidates[0], "finish_reason"):
                print("🧠 finish_reason:", gemini_response.candidates[0].finish_reason)

            if not texto:
                print("⚠️ Modelo não retornou texto. Resposta bruta:")
                print(gemini_response.to_dict())
                return {"resposta": "Não foi possível gerar uma descrição para esta imagem."}

            print("✅ Resposta recebida com sucesso.")
            return {"resposta": texto.strip()}

        elif req.mensagem:
            gemini_response = model.generate_content(req.mensagem)
            if hasattr(gemini_response, "text"):
                return {"resposta": gemini_response.text.strip()}
            else:
                return {"resposta": "Não foi possível gerar resposta para a mensagem."}

        else:
            raise HTTPException(status_code=400, detail="Nenhuma entrada fornecida.")

    except Exception as e:
        print("❌ Erro durante o processamento:", e)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
