from pydantic import BaseModel
from datetime import datetime


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str
    is_admin: bool
    pontos: int

    class Config:
        orm_mode = True

class ConquistaCreate(BaseModel):
    nome: str
    descricao: str
    pontos: int

class ConquistaOut(ConquistaCreate):
    class Config:
        orm_mode = True

class ConquistaObtidaCreate(BaseModel):
    nome_conquista: str
    id_usuario: int


class ConquistaObtidaOut(BaseModel):
    nome_conquista: str
    id_usuario: int
    data_obtida: datetime

    class Config:
        from_attributes = True



class ObraVisitadaCreate(BaseModel):
    id_obra: int
    id_usuario: int

class ObraVisitadaOut(ObraVisitadaCreate):
    class Config:
        orm_mode = True