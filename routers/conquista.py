from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Conquista
from schemas import ConquistaOut
from usuario import get_db

router = APIRouter(prefix="/conquista", tags=["conquista"])

@router.get("/get_lista", response_model=list[ConquistaOut])
def listar_conquistas(db: Session = Depends(get_db)):
    return db.query(Conquista).all()