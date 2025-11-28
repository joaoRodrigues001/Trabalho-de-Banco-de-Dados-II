# Relatório de Alunos - MongoDB

## Query de Agregação

```javascript
db.alunos.aggregate([
    {
        $lookup: {
            from: "instrutores",
            localField: "id_instrutores",
            foreignField: "id_instrutores",
            as: "instrutor"
        }
    },
    {
        $unwind: "$instrutor"
    },
    {
        $project: {
            _id: 0,
            matricula: 1,
            nome: 1,
            email: 1,
            cpf: 1,
            telefone: 1,
            status: 1,
            instrutor: "$instrutor.nome"
        }
    }
])
```

## Descrição

Este pipeline de agregação realiza um JOIN entre as collections `alunos` e `instrutores`, retornando informações completas dos alunos incluindo o nome do instrutor responsável.
