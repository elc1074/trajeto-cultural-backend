from routers.obra_visitada import listar_obras_visitadas
from routers.conquista_obtida import listar_conquistas_obtidas
from database import SessionLocal

class AchievementService():
    def __init__(self, userId: int):
        self.userId = userId
        self.session = SessionLocal()
        self.conquistas_obtidas = listar_conquistas_obtidas(self.userId, self.session)

    def testa_por_numero_de_obras_visitadas(self):
        conquistas_por_numero_de_obras = ['Primeiro Passo', 'Explorador em Treinamento',
                                          'Turista Curioso', 'Roteiro Completo',
                                          'Colecionador de Experiências']
        
        obras_visitadas = listar_obras_visitadas(self.userId, self.session)
        numero_de_obras_visitadas = len(obras_visitadas)

        for conquista in conquistas_por_numero_de_obras:
            if conquista in self.conquistas_obtidas:
                print(conquista)