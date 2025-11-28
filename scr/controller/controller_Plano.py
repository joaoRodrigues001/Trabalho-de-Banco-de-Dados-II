from model.Plano import Plano
from conexion.passphrase.mongo_queries import MongoQueries

class Controller_Plano:
    def __init__(self):
        pass

    def inserir_plano(self) -> Plano:
        '''Insere um novo plano na base de dados'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_plano = int(input("ID do Plano (Novo): "))

        if self.verifica_existencia_plano(mongo, id_plano):
            nome_plano = input("Nome do Plano: ")
            valor = float(input("Valor: "))
            tipo_plano = input("Tipo do Plano: ")

            documento = {
                "id_plano": id_plano,
                "nome_plano": nome_plano,
                "valor": valor,
                "tipo_plano": tipo_plano
            }

            mongo.insert_one("planos", documento)

            plano_doc = mongo.find_one("planos", {"id_plano": id_plano})

            novo_plano = Plano(
                plano_doc["id_plano"],
                plano_doc["nome_plano"],
                plano_doc["valor"],
                plano_doc["tipo_plano"]
            )

            print(novo_plano.to_string())
            mongo.close()
            return novo_plano
        else:
            print(f"O ID {id_plano} já está cadastrado.")
            mongo.close()
            return None

    def atualizar_plano(self) -> Plano:
        '''Atualiza os dados de um plano existente'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_plano = int(input("ID do Plano que deseja alterar: "))

        if not self.verifica_existencia_plano(mongo, id_plano):
            nome_plano = input("Novo Nome do Plano: ")
            valor = float(input("Novo Valor: "))
            tipo_plano = input("Novo Tipo do Plano: ")

            mongo.update_one(
                "planos",
                {"id_plano": id_plano},
                {"$set": {
                    "nome_plano": nome_plano,
                    "valor": valor,
                    "tipo_plano": tipo_plano
                }}
            )

            plano_doc = mongo.find_one("planos", {"id_plano": id_plano})

            plano_atualizado = Plano(
                plano_doc["id_plano"],
                plano_doc["nome_plano"],
                plano_doc["valor"],
                plano_doc["tipo_plano"]
            )

            print(plano_atualizado.to_string())
            mongo.close()
            return plano_atualizado
        else:
            print(f"O ID {id_plano} não existe.")
            mongo.close()
            return None

    def excluir_plano(self):
        '''Remove um plano da base de dados'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_plano = int(input("ID do Plano que deseja excluir: "))

        if not self.verifica_existencia_plano(mongo, id_plano):
            plano_doc = mongo.find_one("planos", {"id_plano": id_plano})

            mongo.delete_one("planos", {"id_plano": id_plano})

            plano_excluido = Plano(
                plano_doc["id_plano"],
                plano_doc["nome_plano"],
                plano_doc["valor"],
                plano_doc["tipo_plano"]
            )

            print("Plano removido com sucesso! 🗑️")
            print(plano_excluido.to_string())
            mongo.close()
        else:
            print(f"O ID {id_plano} não existe.")
            mongo.close()

    def verifica_existencia_plano(self, mongo: MongoQueries, id_plano: int = None) -> bool:
        '''Verifica se um plano existe na base de dados'''
        plano = mongo.find_one("planos", {"id_plano": id_plano})
        return plano is None
