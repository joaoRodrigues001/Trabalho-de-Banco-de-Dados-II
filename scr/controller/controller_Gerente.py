from model.Gerente import Gerente
from conexion.passphrase.mongo_queries import MongoQueries

class Controller_Gerente:
    def __init__(self):
        pass

    def inserir_gerente(self) -> Gerente:
        '''Insere um novo gerente na base de dados'''
        
        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_gerente = int(input("ID do Gerente (Novo): "))

        if self.verifica_existencia_gerente(mongo, id_gerente):
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            email = input("Email: ")
            senha = input("Senha: ")
            salario = float(input("Salário: "))

            documento = {
                "id_gerente": id_gerente,
                "nome": nome,
                "telefone": telefone,
                "email": email,
                "senha": senha,
                "salario": salario
            }

            mongo.insert_one("gerente", documento)

            gerente_doc = mongo.find_one("gerente", {"id_gerente": id_gerente})

            novo_gerente = Gerente(
                gerente_doc["id_gerente"],
                gerente_doc["nome"],
                gerente_doc["telefone"],
                gerente_doc["email"],
                gerente_doc["senha"],
                gerente_doc["salario"],
            )

            print(novo_gerente.to_string())
            mongo.close()
            return novo_gerente
        else:
            print(f"O ID {id_gerente} já está cadastrado.")
            mongo.close()
            return None

    def atualizar_gerente(self) -> Gerente:
        '''Atualiza os dados de um gerente existente'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_gerente = int(input("ID do Gerente que deseja alterar: "))

        if not self.verifica_existencia_gerente(mongo, id_gerente):
            nome = input("Novo Nome: ")
            telefone = input("Novo Telefone: ")
            email = input("Novo Email: ")
            senha = input("Nova Senha: ")
            salario = float(input("Novo Salário: "))

            mongo.update_one(
                "gerente",
                {"id_gerente": id_gerente},
                {"$set": {
                    "nome": nome,
                    "telefone": telefone,
                    "email": email,
                    "senha": senha,
                    "salario": salario
                }}
            )

            gerente_doc = mongo.find_one("gerente", {"id_gerente": id_gerente})

            gerente_atualizado = Gerente(
                gerente_doc["id_gerente"],
                gerente_doc["nome"],
                gerente_doc["telefone"],
                gerente_doc["email"],
                gerente_doc["senha"],
                gerente_doc["salario"],
            )

            print(gerente_atualizado.to_string())
            mongo.close()
            return gerente_atualizado
        else:
            print(f"O ID {id_gerente} não existe.")
            mongo.close()
            return None

    def excluir_gerente(self):
        '''Remove um gerente da base de dados'''

        mongo = MongoQueries(can_write=True)
        mongo.connect()

        id_gerente = int(input("ID do Gerente que deseja excluir: "))

        if not self.verifica_existencia_gerente(mongo, id_gerente):
            gerente_doc = mongo.find_one("gerente", {"id_gerente": id_gerente})

            mongo.delete_one("gerente", {"id_gerente": id_gerente})

            gerente_excluido = Gerente(
                gerente_doc["id_gerente"],
                gerente_doc["nome"],
                gerente_doc["telefone"],
                gerente_doc["email"],
                gerente_doc["senha"],
                gerente_doc["salario"],
            )

            print("Gerente removido com sucesso! 🗑️")
            print(gerente_excluido.to_string())
            mongo.close()
        else:
            print(f"O ID {id_gerente} não existe.")
            mongo.close()

    def verifica_existencia_gerente(self, mongo: MongoQueries, id_gerente: int = None) -> bool:
        '''Verifica se um gerente existe na base de dados'''
        gerente = mongo.find_one("gerente", {"id_gerente": id_gerente})
        return gerente is None
