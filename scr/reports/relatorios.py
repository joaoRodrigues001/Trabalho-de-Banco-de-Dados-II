from conexion.passphrase.mongo_queries import MongoQueries

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_aluno(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        
        # Pipeline de agregação para relatório de alunos
        pipeline = [
            {
                "$lookup": {
                    "from": "instrutores",
                    "localField": "id_instrutores",
                    "foreignField": "id_instrutores",
                    "as": "instrutor"
                }
            },
            {
                "$unwind": "$instrutor"
            },
            {
                "$project": {
                    "_id": 0,
                    "matricula": 1,
                    "nome": 1,
                    "email": 1,
                    "cpf": 1,
                    "telefone": 1,
                    "status": 1,
                    "instrutor": "$instrutor.nome"
                }
            }
        ]
        
        df = mongo.aggregate_to_dataframe("alunos", pipeline)
        print("\n📋 RELATÓRIO DE ALUNOS:\n")
        print(df.to_string(index=False))
        mongo.close()
        input("\nPressione Enter para Sair do Relatório de Alunos")

    def get_relatorio_tipo_plano(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        
        # Pipeline de agregação para relatório de planos
        pipeline = [
            {
                "$lookup": {
                    "from": "contrato_plano",
                    "localField": "id_plano",
                    "foreignField": "id_plano",
                    "as": "contratos"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "tipo_plano": 1,
                    "nome_plano": 1,
                    "valor": 1,
                    "total_contratos": {"$size": "$contratos"}
                }
            },
            {
                "$sort": {"total_contratos": -1}
            }
        ]
        
        df = mongo.aggregate_to_dataframe("planos", pipeline)
        print("\n💰 RELATÓRIO DE TIPO DE PLANOS:\n")
        print(df.to_string(index=False))
        mongo.close()
        input("\nPressione Enter para Sair do Relatório de Tipo de Planos")
