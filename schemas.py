from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str
    is_admin: bool

    class Config:
        orm_mode = True

class ConquistaOut(BaseModel):
    id: int
    nome: str
    descricao: str
    
    class Config:
        orm_mode = True

class ConquistaObtidaCreate(BaseModel):
    id_conquista: int
    id_usuario: int

class ConquistaObtidaOut(ConquistaObtidaCreate):
    class Config:
        orm_mode = True

class ObraVisitadaCreate(BaseModel):
    id_obra: int
    id_usuario: int

class ObraVisitadaOut(ObraVisitadaCreate):
    class Config:
        orm_mode = True