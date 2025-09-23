from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Conquista
from schemas import ConquistaCreate, ConquistaOut
from routers.usuario import get_db

router = APIRouter(prefix="/conquista", tags=["conquista"])

@router.post("/register", response_model=ConquistaCreate)
def register_conquista(achievement: ConquistaCreate, db: Session = Depends(get_db)):
    db_user = db.query(Conquista).filter(Conquista.nome == achievement.nome).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Conquista já registrada")

    new_achievement = Conquista(nome=achievement.nome, 
                                descricao=achievement.descricao, 
                                pontos=achievement.pontos)
    
    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)
    return new_achievement

@router.get("/get_lista", response_model=list[ConquistaOut])
def listar_conquistas(db: Session = Depends(get_db)):
    return db.query(Conquista).all()

@router.get("/get_conquista", response_model=ConquistaOut)
def get_conquista(nome: str, db: Session = Depends(get_db)):
    conquista = db.query(Conquista).filter(Conquista.nome == nome).first()
    if not conquista:
        raise HTTPException(status_code=404, detail="Conquista não encontrada")
    return conquista