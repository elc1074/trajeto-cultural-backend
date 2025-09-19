from sqlalchemy import text
from database import engine

try:
    with engine.connect() as connection:
        with connection.begin():

            print("Adicionando a coluna 'pontos'...")
            connection.execute(text("ALTER TABLE conquistas ADD COLUMN pontos INTEGER NOT NULL;"))

            connection.execute(text("ALTER TABLE conquistas_obtidas ADD COLUMN nome_conquista VARCHAR(255) NOT NULL;"))
            connection.execute(text("ALTER TABLE conquistas_obtidas DROP CONSTRAINT conquistas_obtidas_pkey;"))
            connection.execute(text("ALTER TABLE conquistas_obtidas DROP COLUMN id_conquista;"))
            connection.execute(text("ALTER TABLE conquistas_obtidas ADD CONSTRAINT fk_nome_conquista FOREIGN KEY (nome_conquista) REFERENCES conquistas (nome);"))
            connection.execute(text("ALTER TABLE conquistas_obtidas ADD PRIMARY KEY (nome_conquista);"))

            print("Removendo a chave primária 'id'...")
            connection.execute(text("ALTER TABLE conquistas DROP CONSTRAINT conquistas_pkey;"))

            print("Removendo a coluna 'id'...")
            connection.execute(text("ALTER TABLE conquistas DROP COLUMN id;"))

            print("Definindo 'nome' como a nova chave primária...")
            connection.execute(text("ALTER TABLE conquistas ADD PRIMARY KEY (nome);"))
            
            print("Tabela 'conquistas' alterada com sucesso!")

except Exception as e:
    print(f"Ocorreu um erro: {e}")
    print("Nenhuma alteração foi aplicada ao banco de dados.")

finally:
    engine.dispose()