from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
import requests

router = APIRouter(prefix="/analise", tags=["analise"])

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ImageInput(BaseModel):
    image_url: str

@router.post("/gemini")
def comentar_obra(input_data: ImageInput):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        image_bytes = requests.get(input_data.image_url).content
        response = model.generate_content([
            {"mime_type": "image/jpeg", "data": image_bytes},
            "Faça uma breve análise artística e histórica da imagem acima, em português, com no máximo 3 frases."
        ])
        return {"comentario": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
