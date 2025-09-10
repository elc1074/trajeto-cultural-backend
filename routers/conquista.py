from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Conquista
from schemas import ConquistaOut
from usuario import get_db

router = APIRouter(prefix="/conquista", tags=["conquista"])

@router.get("/get_lista", response_model=list[ConquistaOut])
def listar_conquistas(db: Session = Depends(get_db)):
    return db.query(Conquista).all()

@router.get("/get_conquista", responde_model=ConquistaOut)
def get_conquista(id: int, db: Session = Depends(get_db)):
    conquista = db.query(Conquista).where(Conquista.id == id).first()
    if not conquista:
        raise HTTPException(status_code=404, detail="Conquista não encontrada")
    return conquista