from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.usuario import router as usuario_router
from routers.acervo import router as acervo_router
from routers.conquista import router as conquista_router
from routers.conquista_obtida import router as conquista_obtida_router
from routers.obra_visitada import router as obra_visitada_router
from database import Base, engine
import models

app = FastAPI(title="Trajeto cultural", version="0.1.0")

origins = [
    "http://localhost:5173",
    "https://trajeto-cultural-frontend.vercel.app",
    "https://trajeto-cultural-backend.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_router)
app.include_router(acervo_router)
app.include_router(conquista_router)
app.include_router(conquista_obtida_router)
app.include_router(obra_visitada_router)


@app.get("/")
async def root():
    return {
        "message": "API Trajeto Cultural - Rota padrão",
        "endpoints_disponiveis": {
            "/acervo/get_lista": "Lista obras do acervo (Tainacan)",
            "/acervo/get_obra/{id}": "Detalhes de uma obra específica pelo ID",

            "/usuario/register": "Registrar novo usuário",
            "/usuario/login": "Login de usuário",
        }
    }

Base.metadata.create_all(bind=engine)