# Sistema de Academia FIT - MongoDB

Sistema de gerenciamento de academia convertido de Oracle Database para MongoDB, mantendo toda a lógica e funcionalidades originais.

## 📋 Descrição

Este projeto é uma conversão completa do sistema de academia que originalmente utilizava Oracle Database para MongoDB. O sistema gerencia:

- **Alunos**: Cadastro e controle de alunos
- **Instrutores**: Gerenciamento de instrutores e suas especialidades
- **Gerentes**: Administração e supervisão
- **Treinos**: Programas de treinamento personalizados
- **Planos**: Diferentes modalidades de planos de assinatura
- **Contratos**: Controle de contratos entre alunos e planos
- **Pagamentos**: Registro de pagamentos e transações financeiras

## 🔄 Conversão Oracle → MongoDB

### Principais Mudanças

1. **Banco de Dados**
   - Oracle Database → MongoDB
   - Tabelas relacionais → Collections de documentos
   - SQL Queries → Aggregation Pipelines

2. **Conexão**
   - `cx_Oracle` → `pymongo`
   - `OracleQueries` → `MongoQueries`

3. **Operações CRUD**
   - `INSERT INTO` → `insert_one()`
   - `UPDATE SET` → `update_one()` com `$set`
   - `DELETE FROM` → `delete_one()`
   - `SELECT` → `find()` / `find_one()`

4. **Joins e Agregações**
   - SQL JOINs → `$lookup` no aggregation pipeline
   - GROUP BY → `$group`
   - ORDER BY → `$sort`

## 🚀 Instalação

### Pré-requisitos

- Python 3.8+
- MongoDB 4.4+
- pip (gerenciador de pacotes Python)

### Passos

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd Projeto-Academia-MongoDB
```

2. Instale as dependências:
```bash
cd scr
pip install -r requirements.txt
```

3. Configure o MongoDB:
   - Certifique-se de que o MongoDB está rodando em `localhost:27017`
   - Ou edite as credenciais em `scr/conexion/passphrase/authentication.mongo`

4. Crie as collections e insira dados de exemplo:
```bash
python create_collections_and_records.py
```

5. Execute o sistema:
```bash
python main.py
```

## 📁 Estrutura do Projeto

```
Projeto-Academia-MongoDB/
├── scr/
│   ├── conexion/
│   │   └── passphrase/
│   │       ├── mongo_queries.py      # Classe de conexão MongoDB
│   │       └── authentication.mongo   # Credenciais
│   ├── controller/
│   │   ├── controller_Aluno.py
│   │   ├── controller_Instrutores.py
│   │   ├── controller_treino.py
│   │   ├── controller_Detalhe_Treino.py
│   │   ├── controller_Plano.py
│   │   ├── controller_Contrato_Plano.py
│   │   ├── controller_Pagamentos.py
│   │   └── controller_Gerente.py
│   ├── model/
│   │   ├── Alunos.py
│   │   ├── Instrutores.py
│   │   ├── Treinos.py
│   │   ├── DetalheTreino.py
│   │   ├── Plano.py
│   │   ├── ContratoPlano.py
│   │   ├── Pagamentos.py
│   │   └── Gerente.py
│   ├── reports/
│   │   └── relatorios.py
│   ├── sql/
│   │   ├── relatorio_aluno.md
│   │   └── relatorio_tipo_plano.md
│   ├── utils/
│   │   └── splash_screen.py
│   ├── db.py
│   ├── main.py
│   ├── test.py
│   ├── create_collections_and_records.py
│   └── requirements.txt
└── README.md
```

## 🔧 Funcionalidades

### CRUD Completo

- **Inserir**: Adicionar novos registros em todas as entidades
- **Atualizar**: Modificar registros existentes
- **Excluir**: Remover registros do banco
- **Consultar**: Visualizar dados com filtros e agregações

### Relatórios

1. **Treinos por Aluno**: Lista todos os treinos de cada aluno
2. **Receita por Plano**: Calcula o total recebido por tipo de plano

## 💾 Estrutura das Collections

### alunos
```json
{
  "matricula": 1,
  "id_instrutores": 1,
  "id_gerente": 1,
  "nome": "Pedro Almeida",
  "email": "pedro@email.com",
  "cpf": "11122233344",
  "telefone": "11987654325",
  "status": 1
}
```

### instrutores
```json
{
  "id_instrutores": 1,
  "id_gerente": 1,
  "nome": "João Oliveira",
  "cpf": "12345678901",
  "email": "joao@academia.com",
  "telefone": "11987654323",
  "cref": "123456",
  "salario": 3500.00
}
```

### treino
```json
{
  "id_treino": 1,
  "matricula": 1,
  "nome_treino": "Treino A - Peito e Tríceps",
  "musculo_alvo": "Peitoral",
  "objetivo": "Hipertrofia",
  "duracao": 60
}
```

## 🔍 Exemplos de Queries MongoDB

### Buscar aluno por CPF
```python
mongo.find_one("alunos", {"cpf": "11122233344"})
```

### Atualizar status do aluno
```python
mongo.update_one(
    "alunos",
    {"cpf": "11122233344"},
    {"$set": {"status": 0}}
)
```

### Relatório com agregação
```python
pipeline = [
    {
        "$lookup": {
            "from": "treino",
            "localField": "matricula",
            "foreignField": "matricula",
            "as": "treinos"
        }
    },
    {"$unwind": "$treinos"},
    {"$sort": {"nome": 1}}
]
mongo.aggregate_to_dataframe("alunos", pipeline)
```

## 👥 Créditos

**Desenvolvido por:**
- Guilherme B. Toniato
- Murilo Reis
- João Pedro Nascimento
- Rafael Lucas
- Gabriel França

**Professor:** Howard Roatti  
**Disciplina:** Banco de Dados

**Conversão para MongoDB:** Mantendo a mesma lógica e estrutura do projeto original

## 📝 Licença

Este projeto é de uso educacional para a disciplina de Banco de Dados.
