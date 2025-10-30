import os
import google.generativeai as genai
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente.")

genai.configure(api_key=api_key)

router = APIRouter(prefix="/analise", tags=["Análise com Gemini"])

class AnaliseRequest(BaseModel):
    image_url: str | None = None
    mensagem: str | None = None

@router.post("/gemini")
async def analisar_obra(req: AnaliseRequest):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")

        if req.image_url:
            try:
                response = model.generate_content([
                    "Descreva esta obra de arte em uma única frase curta e interessante, como se fosse uma legenda de museu.",
                    {"image_url": req.image_url},
                ])

                return {"resposta": response.text.strip()}
            except Exception:
                response = model.generate_content(
                    "Comente algo interessante sobre uma obra de arte genérica."
                )
                return {"resposta": response.text.strip()}

        elif req.mensagem:
            response = model.generate_content(req.mensagem)
            return {"resposta": response.text.strip()}

        else:
            raise HTTPException(status_code=400, detail="Nenhuma entrada fornecida.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
