# Relatório de Tipo de Plano - MongoDB

## Query de Agregação

```javascript
db.planos.aggregate([
    {
        $lookup: {
            from: "contrato_plano",
            localField: "id_plano",
            foreignField: "id_plano",
            as: "contratos"
        }
    },
    {
        $unwind: "$contratos"
    },
    {
        $lookup: {
            from: "pagamentos",
            localField: "contratos.id_contrato",
            foreignField: "id_contrato",
            as: "pagamentos"
        }
    },
    {
        $unwind: "$pagamentos"
    },
    {
        $group: {
            _id: "$tipo_plano",
            total_recebido: { $sum: "$pagamentos.valor_pago" }
        }
    },
    {
        $project: {
            _id: 0,
            tipo_plano: "$_id",
            total_recebido: 1
        }
    },
    {
        $sort: { total_recebido: -1 }
    }
])
```

## Descrição

Este pipeline de agregação calcula o total recebido por tipo de plano, realizando JOINs entre as collections `planos`, `contrato_plano` e `pagamentos`, agrupando os resultados por tipo de plano e ordenando por valor total recebido.
