from model.Treinos import Treino
from conexion.passphrase.mongo_queries import MongoQueries

class Controller_Treino:
    def __init__(self):
        pass

    def inserir_treino(self) -> Treino:
        '''Insere um novo treino na base de dados'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_treino = int(input("ID do Treino (Novo): "))

        if self.verifica_existencia_treino(mongo, id_treino):
            matricula = int(input("Matrícula do Cliente: "))
            nome_treino = input("Nome do Treino: ")
            musculo_alvo = input("Músculo Alvo: ")
            objetivo = input("Objetivo do Treino: ")
            duracao = int(input("Duração em minutos: "))

            documento = {
                "id_treino": id_treino,
                "matricula": matricula,
                "nome_treino": nome_treino,
                "musculo_alvo": musculo_alvo,
                "objetivo": objetivo,
                "duracao": duracao
            }

            mongo.insert_one("treino", documento)

            treino_doc = mongo.find_one("treino", {"id_treino": id_treino})

            novo_treino = Treino(
                treino_doc["id_treino"],
                treino_doc["matricula"],
                treino_doc["nome_treino"],
                treino_doc["musculo_alvo"],
                treino_doc["objetivo"],
                treino_doc["duracao"]
            )

            print(novo_treino.to_string())
            mongo.close()
            return novo_treino
        else:
            print(f"O ID do Treino {id_treino} já está cadastrado.")
            mongo.close()
            return None

    def atualizar_treino(self) -> Treino:
        '''Atualiza os dados de um treino existente'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_treino = int(input("ID do Treino que deseja alterar: "))

        if not self.verifica_existencia_treino(mongo, id_treino):
            matricula = int(input("Nova Matrícula do Cliente: "))
            nome_treino = input("Novo Nome do Treino: ")
            musculo_alvo = input("Novo Músculo Alvo: ")
            objetivo = input("Novo Objetivo do Treino: ")
            duracao = int(input("Nova Duração em minutos: "))

            mongo.update_one(
                "treino",
                {"id_treino": id_treino},
                {"$set": {
                    "matricula": matricula,
                    "nome_treino": nome_treino,
                    "musculo_alvo": musculo_alvo,
                    "objetivo": objetivo,
                    "duracao": duracao
                }}
            )

            treino_doc = mongo.find_one("treino", {"id_treino": id_treino})

            treino_atualizado = Treino(
                treino_doc["id_treino"],
                treino_doc["matricula"],
                treino_doc["nome_treino"],
                treino_doc["musculo_alvo"],
                treino_doc["objetivo"],
                treino_doc["duracao"]
            )

            print(treino_atualizado.to_string())
            mongo.close()
            return treino_atualizado
        else:
            print(f"O ID do Treino {id_treino} não existe.")
            mongo.close()
            return None

    def excluir_treino(self):
        '''Remove um treino da base de dados'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_treino = int(input("ID do Treino que deseja excluir: "))

        if not self.verifica_existencia_treino(mongo, id_treino):
            treino_doc = mongo.find_one("treino", {"id_treino": id_treino})

            mongo.delete_one("treino", {"id_treino": id_treino})

            treino_excluido = Treino(
                treino_doc["id_treino"],
                treino_doc["matricula"],
                treino_doc["nome_treino"],
                treino_doc["musculo_alvo"],
                treino_doc["objetivo"],
                treino_doc["duracao"]
            )

            print("Treino removido com sucesso! 🗑️")
            print(treino_excluido.to_string())
            mongo.close()
        else:
            print(f"O ID do Treino {id_treino} não existe.")
            mongo.close()

    def verifica_existencia_treino(self, mongo: MongoQueries, id_treino: int = None) -> bool:
        '''Verifica se um treino existe na base de dados'''
        treino = mongo.find_one("treino", {"id_treino": id_treino})
        return treino is None
