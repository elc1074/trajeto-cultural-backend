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

class ConquistaBase(BaseModel):
    nome: str
    descricao: str

class ConquistaOut(ConquistaBase):
    id: int

    class Config:
        orm_mode = True

class ConquistaObtidaBase(BaseModel):
    id_conquista: int
    id_usuario: int

class ConquistaObtidaOut(ConquistaObtidaBase):

    class Config:
        orm_mode = True

class ObraVisitadaBase(BaseModel):
    id_obra: int
    id_usuario: int

class ObraVisitadaOut(ObraVisitadaBase):
    class Config:
        orm_mode = True