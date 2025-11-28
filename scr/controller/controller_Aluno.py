from model.Alunos import Aluno
from conexion.passphrase.mongo_queries import MongoQueries

class Controller_Aluno:
    def __init__(self):
        pass

    def inserir_aluno(self) -> Aluno:
        '''
        Insere um novo aluno na collection alunos.
        '''
        mongo = MongoQueries(can_write=True)
        mongo.connect()

        cpf = input("CPF (Novo): ")

        # Verifica se o CPF já existe
        if self.verifica_existencia_aluno(mongo, cpf):
            nome = input("Nome (Novo): ")
            email = input("E-mail: ")
            telefone = input("Telefone: ")
            id_instrutor = int(input("ID do Instrutor: "))
            id_gerente = int(input("ID do Gerente: "))
            status = int(input("Status (1 = ativo / 0 = inativo): "))

            # Gera nova matrícula (ID)
            matricula = mongo.get_next_id("alunos", "matricula")

            # Insere o documento
            documento = {
                "matricula": matricula,
                "id_instrutores": id_instrutor,
                "id_gerente": id_gerente,
                "nome": nome,
                "email": email,
                "cpf": cpf,
                "telefone": telefone,
                "status": status
            }
            
            mongo.insert_one("alunos", documento)

            # Busca o aluno inserido
            aluno_doc = mongo.find_one("alunos", {"cpf": cpf})

            novo_aluno = Aluno(
                matricula=aluno_doc["matricula"],
                id_instrutores=aluno_doc["id_instrutores"],
                id_gerente=aluno_doc["id_gerente"],
                nome=aluno_doc["nome"],
                email=aluno_doc["email"],
                cpf=aluno_doc["cpf"],
                telefone=aluno_doc["telefone"],
                status=aluno_doc["status"]
            )

            print("\nAluno inserido com sucesso!")
            print(novo_aluno.to_string())
            mongo.close()
            return novo_aluno
        else:
            print(f"O CPF {cpf} já está cadastrado.")
            mongo.close()
            return None

    def atualizar_aluno(self) -> Aluno:
        '''
        Atualiza os dados de um aluno existente.
        '''
        mongo = MongoQueries(can_write=True)
        mongo.connect()

        cpf = input("CPF do aluno que deseja atualizar: ")

        if not self.verifica_existencia_aluno(mongo, cpf):
            nome = input("Novo nome: ")
            email = input("Novo e-mail: ")
            telefone = input("Novo telefone: ")
            status = int(input("Novo status (1 = ativo / 0 = inativo): "))

            # Atualiza o documento
            mongo.update_one(
                "alunos",
                {"cpf": cpf},
                {"$set": {
                    "nome": nome,
                    "email": email,
                    "telefone": telefone,
                    "status": status
                }}
            )

            # Busca o aluno atualizado
            aluno_doc = mongo.find_one("alunos", {"cpf": cpf})

            aluno_atualizado = Aluno(
                matricula=aluno_doc["matricula"],
                id_instrutores=aluno_doc["id_instrutores"],
                id_gerente=aluno_doc["id_gerente"],
                nome=aluno_doc["nome"],
                email=aluno_doc["email"],
                cpf=aluno_doc["cpf"],
                telefone=aluno_doc["telefone"],
                status=aluno_doc["status"]
            )

            print("\nAluno atualizado com sucesso!")
            print(aluno_atualizado.to_string())
            mongo.close()
            return aluno_atualizado
        else:
            print(f"O CPF {cpf} não existe.")
            mongo.close()
            return None

    def excluir_aluno(self):
        '''
        Exclui um aluno da collection alunos.
        '''
        mongo = MongoQueries(can_write=True)
        mongo.connect()

        cpf = input("CPF do aluno que deseja excluir: ")

        if not self.verifica_existencia_aluno(mongo, cpf):
            # Busca o aluno antes de excluir
            aluno_doc = mongo.find_one("alunos", {"cpf": cpf})

            # Remove o documento
            mongo.delete_one("alunos", {"cpf": cpf})

            aluno_excluido = Aluno(
                matricula=aluno_doc["matricula"],
                id_instrutores=aluno_doc["id_instrutores"],
                id_gerente=aluno_doc["id_gerente"],
                nome=aluno_doc["nome"],
                email=aluno_doc["email"],
                cpf=aluno_doc["cpf"],
                telefone=aluno_doc["telefone"],
                status=aluno_doc["status"]
            )

            print("\nAluno removido com sucesso!")
            print(aluno_excluido.to_string())
            mongo.close()
        else:
            print(f"O CPF {cpf} não existe.")
            mongo.close()

    def verifica_existencia_aluno(self, mongo: MongoQueries, cpf: str = None) -> bool:
        '''
        Verifica se um aluno com o CPF informado já existe.
        Retorna True se não existe (pode inserir), False se já existe.
        '''
        aluno = mongo.find_one("alunos", {"cpf": cpf})
        return aluno is None
