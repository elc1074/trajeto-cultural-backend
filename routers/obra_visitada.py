from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import ObraVisitada
from schemas import ObraVisitadaCreate, ObraVisitadaOut
from routers.usuario import get_db

router = APIRouter(prefix="/obravisitada", tags=["obravisistada"])

@router.post("/register", response_model=ObraVisitadaOut)
def register(achievement: ObraVisitadaCreate, db: Session = Depends(get_db)):
    db_conquista = db.query(ObraVisitada).filter(ObraVisitada.id_conquista == achievement.id_conquista 
                                            and ObraVisitada.id_usuario == achievement.id_usuario).first()
    if db_conquista:
        raise HTTPException(status_code=400, detail="Conquista já obtida")

    new_achievement = ObraVisitada(id_conquista=achievement.id_conquista, id_usuario=achievement.id_usuario)
    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)
    return new_achievement

@router.get("/get_lista", response_model=list[ObraVisitadaOut])
def listar_conquistas_obtidas(db: Session = Depends(get_db)):
    return db.query(ObraVisitada).all()


@router.get("/get_obra_visitada", response_model=ObraVisitadaOut)
def get_obra_visitada(id_obra: int, id_usuario: int, db: Session = Depends(get_db)):
    obra_visitada = db.query(ObraVisitada).where(ObraVisitada.id_obra == id_obra
                                                and ObraVisitada.id_usuario == id_usuario).first()
    if not obra_visitada:
        raise HTTPException(status_code=404, detail="Obra não visitada")
    return obra_visitada