from routers.obra_visitada import listar_obras_visitadas
from routers.conquista_obtida import listar_conquistas_obtidas, register_conquista_obtida
from routers.conquista import get_conquista
from schemas import ConquistaObtidaCreate
from database import SessionLocal

class AchievementService():
    def __init__(self, userId: int):
        self.userId = userId
        self.session = SessionLocal()
        self.conquistas_obtidas = [c.nome_conquista for c in listar_conquistas_obtidas(id_usuario=self.userId,db=self.session)]

    def testa_por_numero_de_obras_visitadas(self):
        conquistas_por_numero_de_obras = {
            'Primeiro Passo': 1,
            'Explorador em Treinamento': 5,
            'Turista Curioso': 10,
            'Roteiro Completo': 25,
            'Colecionador de Experiências': 50
        }

        obras_visitadas = listar_obras_visitadas(self.userId, self.session)
        numero_de_obras_visitadas = len(obras_visitadas)

        for nome, num_obras in conquistas_por_numero_de_obras.items():
            if numero_de_obras_visitadas == num_obras and nome not in self.conquistas_obtidas:
                conquista_buscada = get_conquista(nome=nome, db=self.session)
                if conquista_buscada:
                    nova_conquista_obtida = ConquistaObtidaCreate(
                        nome_conquista=nome,
                        id_usuario=self.userId
                    )
                    register_conquista_obtida(achievement=nova_conquista_obtida, db=self.session)

                    usuario = self.session.query(Usuario).filter(Usuario.id == self.userId).first()
                    usuario.pontos += conquista_buscada.pontos
                    self.session.commit()

                
