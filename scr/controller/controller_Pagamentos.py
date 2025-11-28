from model.Pagamentos import Pagamentos
from conexion.passphrase.mongo_queries import MongoQueries
from datetime import datetime

class Controller_Pagamentos:
    def __init__(self):
        pass

    def inserir_pagamento(self) -> Pagamentos:
        '''Insere um novo registro de pagamento na base de dados'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_pagamentos = int(input("ID do Pagamento (Novo): "))

        if self.verifica_existencia_pagamento(mongo, id_pagamentos):
            matricula = int(input("Matrícula do Cliente: "))
            id_contrato = int(input("ID do Contrato Relacionado: "))
            
            data_pagamento_str = input("Data do Pagamento (DD/MM/AAAA): ")
            
            valor_pago = float(input("Valor Pago: "))
            metodo_pagamento = input("Método de Pagamento (ex: Crédito, Pix, Dinheiro): ")
            tipo_transacao = input("Tipo de Transação (ex: Mensalidade, Taxa, Serviço): ")

            documento = {
                "id_pagamentos": id_pagamentos,
                "matricula": matricula,
                "id_contrato": id_contrato,
                "data_pagamento": data_pagamento_str,
                "valor_pago": valor_pago,
                "metodo_pagamento": metodo_pagamento,
                "tipo_transacao": tipo_transacao
            }

            mongo.insert_one("pagamentos", documento)

            pagamento_doc = mongo.find_one("pagamentos", {"id_pagamentos": id_pagamentos})

            novo_pagamento = Pagamentos(
                pagamento_doc["id_pagamentos"],
                pagamento_doc["matricula"],
                pagamento_doc["id_contrato"],
                pagamento_doc["data_pagamento"],
                pagamento_doc["valor_pago"],
                pagamento_doc["metodo_pagamento"],
                pagamento_doc["tipo_transacao"]
            )

            print(novo_pagamento.to_string())
            mongo.close()
            return novo_pagamento
        else:
            print(f"O ID do Pagamento {id_pagamentos} já está cadastrado.")
            mongo.close()
            return None

    def atualizar_pagamento(self) -> Pagamentos:
        '''Atualiza os dados de um pagamento existente'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_pagamentos = int(input("ID do Pagamento que deseja alterar: "))

        if not self.verifica_existencia_pagamento(mongo, id_pagamentos):
            matricula = int(input("Nova Matrícula do Cliente: "))
            id_contrato = int(input("Novo ID do Contrato: "))
            data_pagamento_str = input("Nova Data do Pagamento (DD/MM/AAAA): ")
            valor_pago = float(input("Novo Valor Pago: "))
            metodo_pagamento = input("Novo Método de Pagamento: ")
            tipo_transacao = input("Novo Tipo de Transação: ")

            mongo.update_one(
                "pagamentos",
                {"id_pagamentos": id_pagamentos},
                {"$set": {
                    "matricula": matricula,
                    "id_contrato": id_contrato,
                    "data_pagamento": data_pagamento_str,
                    "valor_pago": valor_pago,
                    "metodo_pagamento": metodo_pagamento,
                    "tipo_transacao": tipo_transacao
                }}
            )

            pagamento_doc = mongo.find_one("pagamentos", {"id_pagamentos": id_pagamentos})

            pagamento_atualizado = Pagamentos(
                pagamento_doc["id_pagamentos"],
                pagamento_doc["matricula"],
                pagamento_doc["id_contrato"],
                pagamento_doc["data_pagamento"],
                pagamento_doc["valor_pago"],
                pagamento_doc["metodo_pagamento"],
                pagamento_doc["tipo_transacao"]
            )

            print(pagamento_atualizado.to_string())
            mongo.close()
            return pagamento_atualizado
        else:
            print(f"O ID do Pagamento {id_pagamentos} não existe.")
            mongo.close()
            return None

    def excluir_pagamento(self):
        '''Remove um pagamento da base de dados'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_pagamentos = int(input("ID do Pagamento que deseja excluir: "))

        if not self.verifica_existencia_pagamento(mongo, id_pagamentos):
            pagamento_doc = mongo.find_one("pagamentos", {"id_pagamentos": id_pagamentos})

            mongo.delete_one("pagamentos", {"id_pagamentos": id_pagamentos})

            pagamento_excluido = Pagamentos(
                pagamento_doc["id_pagamentos"],
                pagamento_doc["matricula"],
                pagamento_doc["id_contrato"],
                pagamento_doc["data_pagamento"],
                pagamento_doc["valor_pago"],
                pagamento_doc["metodo_pagamento"],
                pagamento_doc["tipo_transacao"]
            )

            print("Pagamento removido com sucesso! 🗑️")
            print(pagamento_excluido.to_string())
            mongo.close()
        else:
            print(f"O ID do Pagamento {id_pagamentos} não existe.")
            mongo.close()

    def verifica_existencia_pagamento(self, mongo: MongoQueries, id_pagamentos: int = None) -> bool:
        '''Verifica se um pagamento existe na base de dados'''
        pagamento = mongo.find_one("pagamentos", {"id_pagamentos": id_pagamentos})
        return pagamento is None
