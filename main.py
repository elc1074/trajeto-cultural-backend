from fastapi import FastAPI
from routers.usuario import router as usuario_router
from routers.acervo import router as acervo_router

app = FastAPI(title="Trajeto cultural", version="0.1.0")

app.include_router(usuario_router)
app.include_router(acervo_router)

