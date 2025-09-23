from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import ConquistaObtida
from schemas import ConquistaObtidaCreate, ConquistaObtidaOut
from routers.usuario import get_db

router = APIRouter(prefix="/conquistaobtida", tags=["conquistaobtida"])

@router.post("/register", response_model=ConquistaObtidaOut)
def register_conquista_obtida(achievement: ConquistaObtidaCreate, db: Session = Depends(get_db)):
    db_conquista = db.query(ConquistaObtida).filter(
        ConquistaObtida.nome_conquista == achievement.nome_conquista,
        ConquistaObtida.id_usuario == achievement.id_usuario
    ).first()

    if db_conquista:
        raise HTTPException(status_code=400, detail="Conquista já obtida")

    new_achievement = ConquistaObtida(nome_conquista=achievement.nome_conquista,
                                      id_usuario=achievement.id_usuario)
    
    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)
    return new_achievement

@router.get("/get_lista", response_model=list[ConquistaObtida])
def listar_conquistas_obtidas(id_usuario: int, db: Session = Depends(get_db)):
    return db.query(ConquistaObtida).filter(ConquistaObtida.id_usuario == id_usuario).all()

@router.get("/get_conquista_obtida", response_model=ConquistaObtidaOut)
def get_conquista_obtida(nome_conquista: str, id_usuario: int, db: Session = Depends(get_db)):
    conquista_obtida = db.query(ConquistaObtida).filter(ConquistaObtida.nome_conquista == nome_conquista
                                                and ConquistaObtida.id_usuario == id_usuario).first()
    if not conquista_obtida:
        raise HTTPException(status_code=404, detail="Conquista não obtida")
    return conquista_obtida