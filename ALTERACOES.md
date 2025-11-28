# Resumo das Alterações - Oracle para MongoDB

## 📊 Estatísticas da Conversão

- **Arquivos Python Originais**: 29
- **Arquivos Python Convertidos**: 30
- **Estrutura de Diretórios**: Mantida 100%
- **Lógica de Negócio**: Preservada integralmente

## 🔄 Principais Conversões

### 1. Conexão com Banco de Dados

**Oracle (Original)**
```python
import cx_Oracle

connection = cx_Oracle.connect(
    user="LABDATABASE",
    password="1234",
    dsn="localhost/xe"
)
```

**MongoDB (Convertido)**
```python
from pymongo import MongoClient

client = MongoClient(
    host="localhost",
    port=27017,
    username="admin",
    password="1234"
)
db = client["academia_db"]
```

### 2. Classe de Queries

**Oracle: `OracleQueries`**
- `sqlToDataFrame()` - Executa SQL e retorna DataFrame
- `write()` - Executa INSERT, UPDATE, DELETE
- `executeDDL()` - Executa CREATE, DROP, ALTER

**MongoDB: `MongoQueries`**
- `sqlToDataFrame()` - Busca documentos e retorna DataFrame
- `aggregate_to_dataframe()` - Executa pipeline de agregação
- `insert_one()` - Insere documento
- `update_one()` - Atualiza documento
- `delete_one()` - Remove documento
- `find_one()` - Busca um documento
- `get_next_id()` - Gera próximo ID sequencial

### 3. Operações CRUD

#### INSERT
**Oracle**
```python
oracle.write(f"""
    INSERT INTO alunos (matricula, nome, email, cpf)
    VALUES ({matricula}, '{nome}', '{email}', {cpf})
""")
```

**MongoDB**
```python
documento = {
    "matricula": matricula,
    "nome": nome,
    "email": email,
    "cpf": cpf
}
mongo.insert_one("alunos", documento)
```

#### UPDATE
**Oracle**
```python
oracle.write(f"""
    UPDATE alunos
    SET nome = '{nome}', email = '{email}'
    WHERE cpf = {cpf}
""")
```

**MongoDB**
```python
mongo.update_one(
    "alunos",
    {"cpf": cpf},
    {"$set": {"nome": nome, "email": email}}
)
```

#### DELETE
**Oracle**
```python
oracle.write(f"DELETE FROM alunos WHERE cpf = {cpf}")
```

**MongoDB**
```python
mongo.delete_one("alunos", {"cpf": cpf})
```

#### SELECT
**Oracle**
```python
df = oracle.sqlToDataFrame(f"""
    SELECT matricula, nome, email, cpf
    FROM alunos
    WHERE cpf = {cpf}
""")
```

**MongoDB**
```python
aluno = mongo.find_one("alunos", {"cpf": cpf})
# ou para DataFrame:
df = mongo.sqlToDataFrame("alunos", {"cpf": cpf})
```

### 4. Joins e Agregações

#### Relatório de Treinos por Aluno

**Oracle (SQL JOIN)**
```sql
SELECT a.nome AS aluno,
       t.nome_treino,
       t.musculo_alvo,
       t.objetivo,
       t.duracao
FROM LABDATABASE.ALUNOS a
JOIN LABDATABASE.TREINO t ON t.matricula = a.matricula
ORDER BY a.nome, t.nome_treino
```

**MongoDB (Aggregation Pipeline)**
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
    {
        "$project": {
            "aluno": "$nome",
            "nome_treino": "$treinos.nome_treino",
            "musculo_alvo": "$treinos.musculo_alvo",
            "objetivo": "$treinos.objetivo",
            "duracao": "$treinos.duracao"
        }
    },
    {"$sort": {"aluno": 1, "nome_treino": 1}}
]
```

#### Relatório de Receita por Plano

**Oracle (SQL com múltiplos JOINs e GROUP BY)**
```sql
SELECT p.tipo_plano,
       SUM(pg.valor_pago) AS total_recebido
FROM LABDATABASE.PLANOS p
JOIN LABDATABASE.CONTRATO_PLANO cp ON cp.id_plano = p.id_plano
JOIN LABDATABASE.PAGAMENTOS pg ON pg.id_contrato = cp.id_contrato
GROUP BY p.tipo_plano
ORDER BY total_recebido DESC
```

**MongoDB (Aggregation Pipeline com $lookup e $group)**
```python
pipeline = [
    {
        "$lookup": {
            "from": "contrato_plano",
            "localField": "id_plano",
            "foreignField": "id_plano",
            "as": "contratos"
        }
    },
    {"$unwind": "$contratos"},
    {
        "$lookup": {
            "from": "pagamentos",
            "localField": "contratos.id_contrato",
            "foreignField": "id_contrato",
            "as": "pagamentos"
        }
    },
    {"$unwind": "$pagamentos"},
    {
        "$group": {
            "_id": "$tipo_plano",
            "total_recebido": {"$sum": "$pagamentos.valor_pago"}
        }
    },
    {
        "$project": {
            "tipo_plano": "$_id",
            "total_recebido": 1
        }
    },
    {"$sort": {"total_recebido": -1}}
]
```

### 5. Geração de IDs Sequenciais

**Oracle (usando MAX + 1)**
```python
df_matricula = oracle.sqlToDataFrame(
    "SELECT NVL(MAX(matricula), 0) + 1 AS nova_matricula FROM alunos"
)
matricula = int(df_matricula.nova_matricula.values[0])
```

**MongoDB (método auxiliar)**
```python
matricula = mongo.get_next_id("alunos", "matricula")
```

### 6. Verificação de Existência

**Oracle**
```python
df_aluno = oracle.sqlToDataFrame(f"SELECT cpf FROM alunos WHERE cpf = {cpf}")
return df_aluno.empty  # True se não existe
```

**MongoDB**
```python
aluno = mongo.find_one("alunos", {"cpf": cpf})
return aluno is None  # True se não existe
```

## 📦 Estrutura de Dados

### Tabelas Oracle → Collections MongoDB

| Oracle | MongoDB |
|--------|---------|
| GERENTE | gerente |
| INSTRUTORES | instrutores |
| ALUNOS | alunos |
| PLANOS | planos |
| CONTRATO_PLANO | contrato_plano |
| TREINO | treino |
| DETALHE_TREINO | detalhe_treino |
| PAGAMENTOS | pagamentos |

### Tipos de Dados

| Oracle | MongoDB |
|--------|---------|
| NUMBER | int / float |
| VARCHAR2 | str |
| DATE | str (formato DD/MM/AAAA) |

## 🔧 Arquivos Modificados

### Criados/Convertidos

1. **scr/conexion/passphrase/mongo_queries.py** - Nova classe de conexão MongoDB
2. **scr/conexion/passphrase/authentication.mongo** - Credenciais MongoDB
3. **scr/db.py** - Função de conexão simplificada
4. **scr/controller/** - Todos os 8 controllers convertidos
5. **scr/model/** - Todos os 8 models mantidos (ajustes mínimos)
6. **scr/main.py** - Lógica principal com agregações MongoDB
7. **scr/reports/relatorios.py** - Relatórios com pipelines
8. **scr/utils/splash_screen.py** - Adaptado para MongoDB
9. **scr/create_collections_and_records.py** - Substituiu create_tables_and_records.py
10. **scr/test.py** - Testes adaptados para MongoDB
11. **scr/sql/relatorio_aluno.md** - Documentação de queries
12. **scr/sql/relatorio_tipo_plano.md** - Documentação de queries
13. **README.md** - Documentação completa do projeto

## ✅ Funcionalidades Preservadas

- ✅ CRUD completo para todas as entidades
- ✅ Validação de existência antes de inserir
- ✅ Geração automática de IDs sequenciais
- ✅ Relatórios com agregações complexas
- ✅ Splash screen com contagem de registros
- ✅ Estrutura MVC (Model-View-Controller)
- ✅ Separação de responsabilidades
- ✅ Tratamento de erros

## 🎯 Vantagens da Conversão para MongoDB

1. **Flexibilidade de Schema**: Documentos podem ter estruturas variadas
2. **Escalabilidade Horizontal**: Fácil distribuição de dados
3. **Performance em Leituras**: Documentos completos em uma única operação
4. **JSON Nativo**: Estrutura natural para aplicações modernas
5. **Agregações Poderosas**: Pipeline de agregação muito expressivo
6. **Sem Necessidade de Joins Físicos**: Dados relacionados podem ser embedados

## 📚 Dependências

**Original (Oracle)**
- cx-Oracle==8.3.0
- pandas==1.4.4
- numpy==1.23.2

**Convertido (MongoDB)**
- pymongo==4.6.0
- pandas==1.4.4
- numpy==1.23.2

## 🚀 Como Usar

1. Instale o MongoDB
2. Execute: `pip install -r requirements.txt`
3. Execute: `python create_collections_and_records.py`
4. Execute: `python main.py`

## 📝 Notas Importantes

- Todas as operações foram testadas para manter a mesma lógica
- Os IDs são mantidos como inteiros para compatibilidade
- Datas são armazenadas como strings no formato DD/MM/AAAA
- A estrutura de pastas foi mantida idêntica ao original
- Todos os comentários e docstrings foram preservados
