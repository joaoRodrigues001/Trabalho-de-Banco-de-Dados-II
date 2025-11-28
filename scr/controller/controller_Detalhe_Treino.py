from model.DetalheTreino import DetalheTreino
from conexion.passphrase.mongo_queries import MongoQueries

class Controller_DetalheTreino:
    def __init__(self):
        pass

    def inserir_detalhe_treino(self) -> DetalheTreino:
        '''Insere um novo detalhe de treino na base de dados'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_detalhe = int(input("ID do Detalhe do Treino (Novo): "))

        if self.verifica_existencia_detalhe(mongo, id_detalhe):
            id_instrutor = int(input("ID do Instrutor (para este detalhe): "))
            id_treino = int(input("ID do Treino ao qual pertence: "))
            series = int(input("Número de Séries: "))
            repeticoes = int(input("Número de Repetições: "))
            instrucoes = input("Instruções do Exercício (ex: 'Foco na cadência'): ")

            documento = {
                "id_detalhe": id_detalhe,
                "id_instrutores": id_instrutor,
                "id_treino": id_treino,
                "series": series,
                "repeticoes": repeticoes,
                "instrucoes": instrucoes
            }

            mongo.insert_one("detalhe_treino", documento)

            detalhe_doc = mongo.find_one("detalhe_treino", {"id_detalhe": id_detalhe})

            novo_detalhe = DetalheTreino(
                detalhe_doc["id_detalhe"],
                detalhe_doc["id_instrutores"],
                detalhe_doc["id_treino"],
                detalhe_doc["series"],
                detalhe_doc["repeticoes"],
                detalhe_doc["instrucoes"]
            )

            print(novo_detalhe.to_string())
            mongo.close()
            return novo_detalhe
        else:
            print(f"O ID do Detalhe {id_detalhe} já está cadastrado.")
            mongo.close()
            return None

    def atualizar_detalhe_treino(self) -> DetalheTreino:
        '''Atualiza os dados de um detalhe de treino existente'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_detalhe = int(input("ID do Detalhe do Treino que deseja alterar: "))

        if not self.verifica_existencia_detalhe(mongo, id_detalhe):
            id_instrutor = int(input("Novo ID do Instrutor: "))
            id_treino = int(input("Novo ID do Treino: "))
            series = int(input("Novo Número de Séries: "))
            repeticoes = int(input("Novo Número de Repetições: "))
            instrucoes = input("Novas Instruções: ")

            mongo.update_one(
                "detalhe_treino",
                {"id_detalhe": id_detalhe},
                {"$set": {
                    "id_instrutores": id_instrutor,
                    "id_treino": id_treino,
                    "series": series,
                    "repeticoes": repeticoes,
                    "instrucoes": instrucoes
                }}
            )

            detalhe_doc = mongo.find_one("detalhe_treino", {"id_detalhe": id_detalhe})

            detalhe_atualizado = DetalheTreino(
                detalhe_doc["id_detalhe"],
                detalhe_doc["id_instrutores"],
                detalhe_doc["id_treino"],
                detalhe_doc["series"],
                detalhe_doc["repeticoes"],
                detalhe_doc["instrucoes"]
            )

            print(detalhe_atualizado.to_string())
            mongo.close()
            return detalhe_atualizado
        else:
            print(f"O ID do Detalhe {id_detalhe} não existe.")
            mongo.close()
            return None

    def excluir_detalhe_treino(self):
        '''Remove um detalhe de treino da base de dados'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_detalhe = int(input("ID do Detalhe do Treino que deseja excluir: "))

        if not self.verifica_existencia_detalhe(mongo, id_detalhe):
            detalhe_doc = mongo.find_one("detalhe_treino", {"id_detalhe": id_detalhe})

            mongo.delete_one("detalhe_treino", {"id_detalhe": id_detalhe})

            detalhe_excluido = DetalheTreino(
                detalhe_doc["id_detalhe"],
                detalhe_doc["id_instrutores"],
                detalhe_doc["id_treino"],
                detalhe_doc["series"],
                detalhe_doc["repeticoes"],
                detalhe_doc["instrucoes"]
            )

            print("Detalhe de Treino removido com sucesso! 🗑️")
            print(detalhe_excluido.to_string())
            mongo.close()
        else:
            print(f"O ID do Detalhe {id_detalhe} não existe.")
            mongo.close()

    def verifica_existencia_detalhe(self, mongo: MongoQueries, id_detalhe: int = None) -> bool:
        '''Verifica se um detalhe de treino existe na base de dados'''
        detalhe = mongo.find_one("detalhe_treino", {"id_detalhe": id_detalhe})
        return detalhe is None
