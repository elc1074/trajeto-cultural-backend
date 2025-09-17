from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import ConquistaObtida
from schemas import ConquistaObtidaCreate, ConquistaObtidaOut
from routers.usuario import get_db

router = APIRouter(prefix="/conquistaobtida", tags=["conquistaobtida"])

@router.post("/register", response_model=ConquistaObtidaOut)
def register(achievement: ConquistaObtidaCreate, db: Session = Depends(get_db)):
    db_conquista = db.query(ConquistaObtida).filter(
        ConquistaObtida.id_conquista == achievement.id_conquista,
        ConquistaObtida.id_usuario == achievement.id_usuario
    ).first()
    if db_conquista:
        raise HTTPException(status_code=400, detail="Conquista já obtida")

    new_achievement = ConquistaObtida(id_conquista=achievement.id_conquista, id_usuario=achievement.id_usuario)
    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)
    return new_achievement

@router.get("/get_lista", response_model=list[ConquistaObtidaOut])
def listar_conquistas_obtidas(db: Session = Depends(get_db)):
    return db.query(ConquistaObtida).all()

@router.get("/get_conquista_obtida", response_model=ConquistaObtidaOut)
def get_conquista_obtida(id_conquista: int, id_usuario: int, db: Session = Depends(get_db)):
    conquista_obtida = db.query(ConquistaObtida).where(ConquistaObtida.id_conquista == id_conquista
                                                and ConquistaObtida.id_usuario == id_usuario).first()
    if not conquista_obtida:
        raise HTTPException(status_code=404, detail="Conquista não obtida")
    return conquista_obtida