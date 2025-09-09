from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Usuario
from schemas import UsuarioCreate, UsuarioOut
from passlib.hash import bcrypt

router = APIRouter(prefix="/usuario", tags=["usuario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UsuarioOut)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    hashed_password = bcrypt.hash(user.senha)
    new_user = Usuario(nome=user.nome, email=user.email, senha=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if not db_user or not bcrypt.verify(user.senha, db_user.senha):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    return {
        "message": "Login bem-sucedido",
        "user_id": db_user.id,
        "nome": db_user.nome,
        "email": db_user.email,
        "is_admin": db_user.is_admin,
    }


@router.get("/get_lista", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


