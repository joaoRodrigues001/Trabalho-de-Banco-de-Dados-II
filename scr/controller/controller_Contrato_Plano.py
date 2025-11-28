from model.ContratoPlano import ContratoPlano
from conexion.passphrase.mongo_queries import MongoQueries
from datetime import datetime

class Controller_ContratoPlano:
    def __init__(self):
        pass

    def inserir_contrato(self) -> ContratoPlano:
        '''Insere um novo contrato_plano na base de dados'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_contrato = int(input("ID do Contrato (Novo): "))

        if self.verifica_existencia_contrato(mongo, id_contrato):
            matricula = int(input("Matrícula do Cliente: "))
            id_plano = int(input("ID do Plano Contratado: "))
            
            data_inicio_str = input("Data de Início (DD/MM/AAAA): ")
            data_fim_str = input("Data de Fim (DD/MM/AAAA): ")
            
            status = int(input("Status (1-Ativo, 0-Inativo): "))

            documento = {
                "id_contrato": id_contrato,
                "matricula": matricula,
                "id_plano": id_plano,
                "data_inicio": data_inicio_str,
                "data_fim": data_fim_str,
                "status": status
            }

            mongo.insert_one("contrato_plano", documento)

            contrato_doc = mongo.find_one("contrato_plano", {"id_contrato": id_contrato})

            novo_contrato = ContratoPlano(
                contrato_doc["id_contrato"],
                contrato_doc["matricula"],
                contrato_doc["id_plano"],
                contrato_doc["data_inicio"],
                contrato_doc["data_fim"],
                contrato_doc["status"]
            )

            print(novo_contrato.to_string())
            mongo.close()
            return novo_contrato
        else:
            print(f"O ID do Contrato {id_contrato} já está cadastrado.")
            mongo.close()
            return None

    def atualizar_contrato(self) -> ContratoPlano:
        '''Atualiza os dados de um contrato existente'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_contrato = int(input("ID do Contrato que deseja alterar: "))

        if not self.verifica_existencia_contrato(mongo, id_contrato):
            matricula = int(input("Nova Matrícula do Cliente: "))
            id_plano = int(input("Novo ID do Plano: "))
            data_inicio_str = input("Nova Data de Início (DD/MM/AAAA): ")
            data_fim_str = input("Nova Data de Fim (DD/MM/AAAA): ")
            status = int(input("Novo Status (1-Ativo, 0-Inativo): "))

            mongo.update_one(
                "contrato_plano",
                {"id_contrato": id_contrato},
                {"$set": {
                    "matricula": matricula,
                    "id_plano": id_plano,
                    "data_inicio": data_inicio_str,
                    "data_fim": data_fim_str,
                    "status": status
                }}
            )

            contrato_doc = mongo.find_one("contrato_plano", {"id_contrato": id_contrato})

            contrato_atualizado = ContratoPlano(
                contrato_doc["id_contrato"],
                contrato_doc["matricula"],
                contrato_doc["id_plano"],
                contrato_doc["data_inicio"],
                contrato_doc["data_fim"],
                contrato_doc["status"]
            )

            print(contrato_atualizado.to_string())
            mongo.close()
            return contrato_atualizado
        else:
            print(f"O ID do Contrato {id_contrato} não existe.")
            mongo.close()
            return None

    def excluir_contrato(self):
        '''Remove um contrato da base de dados'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_contrato = int(input("ID do Contrato que deseja excluir: "))

        if not self.verifica_existencia_contrato(mongo, id_contrato):
            contrato_doc = mongo.find_one("contrato_plano", {"id_contrato": id_contrato})

            mongo.delete_one("contrato_plano", {"id_contrato": id_contrato})

            contrato_excluido = ContratoPlano(
                contrato_doc["id_contrato"],
                contrato_doc["matricula"],
                contrato_doc["id_plano"],
                contrato_doc["data_inicio"],
                contrato_doc["data_fim"],
                contrato_doc["status"]
            )

            print("Contrato removido com sucesso! 🗑️")
            print(contrato_excluido.to_string())
            mongo.close()
        else:
            print(f"O ID do Contrato {id_contrato} não existe.")
            mongo.close()

    def verifica_existencia_contrato(self, mongo: MongoQueries, id_contrato: int = None) -> bool:
        '''Verifica se um contrato existe na base de dados'''
        contrato = mongo.find_one("contrato_plano", {"id_contrato": id_contrato})
        return contrato is None
