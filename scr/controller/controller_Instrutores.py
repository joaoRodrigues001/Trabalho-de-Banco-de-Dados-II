from model.Instrutores import Instrutor
from conexion.passphrase.mongo_queries import MongoQueries

class Controller_Instrutor:
    def __init__(self):
        pass

    def inserir_instrutor(self) -> Instrutor:
        '''Insere um novo instrutor na base de dados'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_instrutor = int(input("ID do Instrutor (Novo): "))

        if self.verifica_existencia_instrutor(mongo, id_instrutor):
            id_gerente = int(input("ID do Gerente Responsável: "))
            nome = input("Nome: ")
            cpf = input("CPF: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            cref = input("CREF: ")
            salario = float(input("Salário: "))

            documento = {
                "id_instrutores": id_instrutor,
                "id_gerente": id_gerente,
                "nome": nome,
                "cpf": cpf,
                "email": email,
                "telefone": telefone,
                "cref": cref,
                "salario": salario
            }

            mongo.insert_one("instrutores", documento)

            instrutor_doc = mongo.find_one("instrutores", {"id_instrutores": id_instrutor})

            novo_instrutor = Instrutor(
                instrutor_doc["id_instrutores"],
                instrutor_doc["id_gerente"],
                instrutor_doc["nome"],
                instrutor_doc["cpf"],
                instrutor_doc["email"],
                instrutor_doc["telefone"],
                instrutor_doc["cref"],
                instrutor_doc["salario"],
            )

            print(novo_instrutor.to_string())
            mongo.close()
            return novo_instrutor
        else:
            print(f"O ID {id_instrutor} já está cadastrado.")
            mongo.close()
            return None

    def atualizar_instrutor(self) -> Instrutor:
        '''Atualiza os dados de um instrutor existente'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_instrutor = int(input("ID do Instrutor que deseja alterar: "))

        if not self.verifica_existencia_instrutor(mongo, id_instrutor):
            id_gerente = int(input("Novo ID do Gerente: "))
            nome = input("Novo Nome: ")
            cpf = input("Novo CPF: ")
            email = input("Novo Email: ")
            telefone = input("Novo Telefone: ")
            cref = input("Novo CREF: ")
            salario = float(input("Novo Salário: "))

            mongo.update_one(
                "instrutores",
                {"id_instrutores": id_instrutor},
                {"$set": {
                    "id_gerente": id_gerente,
                    "nome": nome,
                    "cpf": cpf,
                    "email": email,
                    "telefone": telefone,
                    "cref": cref,
                    "salario": salario
                }}
            )

            instrutor_doc = mongo.find_one("instrutores", {"id_instrutores": id_instrutor})

            instrutor_atualizado = Instrutor(
                instrutor_doc["id_instrutores"],
                instrutor_doc["id_gerente"],
                instrutor_doc["nome"],
                instrutor_doc["cpf"],
                instrutor_doc["email"],
                instrutor_doc["telefone"],
                instrutor_doc["cref"],
                instrutor_doc["salario"],
            )

            print(instrutor_atualizado.to_string())
            mongo.close()
            return instrutor_atualizado
        else:
            print(f"O ID {id_instrutor} não existe.")
            mongo.close()
            return None

    def excluir_instrutor(self):
        '''Remove um instrutor da base de dados'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_instrutor = int(input("ID do Instrutor que deseja excluir: "))

        if not self.verifica_existencia_instrutor(mongo, id_instrutor):
            instrutor_doc = mongo.find_one("instrutores", {"id_instrutores": id_instrutor})

            mongo.delete_one("instrutores", {"id_instrutores": id_instrutor})

            instrutor_excluido = Instrutor(
                instrutor_doc["id_instrutores"],
                instrutor_doc["id_gerente"],
                instrutor_doc["nome"],
                instrutor_doc["cpf"],
                instrutor_doc["email"],
                instrutor_doc["telefone"],
                instrutor_doc["cref"],
                instrutor_doc["salario"],
            )

            print("Instrutor removido com sucesso! 🗑️")
            print(instrutor_excluido.to_string())
            mongo.close()
        else:
            print(f"O ID {id_instrutor} não existe.")
            mongo.close()

    def verifica_existencia_instrutor(self, mongo: MongoQueries, id_instrutor: int = None) -> bool:
        '''Verifica se um instrutor existe na base de dados'''
        instrutor = mongo.find_one("instrutores", {"id_instrutores": id_instrutor})
        return instrutor is None
