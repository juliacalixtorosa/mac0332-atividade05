# Fase 3 — Aplicação dos Critérios de Cobertura

## 1. Retomada do Grafo de Fluxo de Controle (GFC)

O programa `calcular_desconto` foi decomposto em **nós elementares** (blocos de código indivisíveis) e **decisões**, resultando em um grafo de controle mais detalhado:

| Nº | Bloco de Código / Decisão                         |
| -- | ------------------------------------------------- |
| 1  | `valor_compra <= 0 ?`                             |
| 2  | `return 0`                                        |
| 3  | `tipo_cliente == "premium" ?`                     |
| 4  | `desconto = 0.15`                                 |
| 5  | `tipo_cliente == "regular" ?`                     |
| 6  | `desconto = 0.05`                                 |
| 7  | `desconto = 0`                                    |
| 8  | `cupom == "DESC10" and valor_compra > 100 ?`      |
| 9  | `desconto += 0.10`                                |
| 10 | `valor_final = valor_compra * (1 - desconto)`     |
| 11 | `valor_final < 50 ?`                              |
| 12 | `valor_final += 5`                                |
| 13 | `return round(valor_final, 2)`                    |

### Fluxos Principais (arestas)

```
1→2  (valor_compra <= 0)
1→3  (valor_compra > 0)
3→4  (premium)
3→5  (não premium)
5→6  (regular)
5→7  (outro tipo)
4,6,7→8
8→9  (cupom válido, valor_compra > 100)
8→10 (cupom inválido ou valor_compra <= 100)
9→10
10→11
11→12 (valor_final < 50)
11→13 (valor_final ≥ 50)
12→13
```

## 2. Caminhos Executáveis Identificados

A partir da estrutura acima, foram enumerados todos os caminhos lógicos possíveis, incluindo variações de `valor_compra`, `tipo_cliente` e `cupom`.

| Caminho | Descrição Lógica                                                 | Sequência de Nós                               |
| ------- | ---------------------------------------------------------------- | ---------------------------------------------- |
| **C1**  | Compra inválida (valor_compra ≤ 0)                               | 1 → 2                                          |
| **C2**  | Cliente premium, sem cupom                                       | 1 → 3 → 4 → 8 → 10 → 11 → 13                   |
| **C3**  | Cliente premium, cupom válido, valor_compra > 100                | 1 → 3 → 4 → 8 → 9 → 10 → 11 → 13          |
| **C4**  | Cliente premium, cupom válido, valor_compra ≤ 100                | 1 → 3 → 4 → 8 → 10 → 11 → 13               |
| **C5**  | Cliente regular, sem cupom                                       | 1 → 3 → 5 → 6 → 8 → 10 → 11 → 13               |
| **C6**  | Cliente regular, cupom válido e valor_compra > 100               | 1 → 3 → 5 → 6 → 8 → 9 → 10 → 11 → 13      |
| **C7**  | Cliente regular, cupom válido e valor_compra ≤ 100               | 1 → 3 → 5 → 6 → 8 → 10 → 11 → 13           |
| **C8**  | Outro cliente, sem cupom                                         | 1 → 3 → 5 → 7 → 8 → 10 → 11 → 13               |
| **C9**  | Outro cliente, cupom válido e valor_compra > 100                 | 1 → 3 → 5 → 7 → 8 → 9 → 10 → 11 → 13      |
| **C10** | Outro cliente, cupom válido e valor_compra ≤ 100                 | 1 → 3 → 5 → 7 → 8 → 10 → 11 → 13           |
| **C11** | Cliente premium, com cupom e taxa de entrega (valor_final < 50)  | 1 → 3 → 4 → 8 → 9 → 10 → 11 → 12 → 13     |
| **C12** | Cliente regular, com cupom e taxa de entrega (valor_final < 50)  | 1 → 3 → 5 → 6 → 8 → 9 → 10 → 11 → 12 → 13 |
| **C13** | Outro cliente, sem cupom, com taxa de entrega (valor_final < 50) | 1 → 3 → 5 → 7 → 8 → 10 → 11 → 12 → 13          |

## Aplicação dos Critérios Estruturais

### Critério 1 — Todos-Nós

Cada nó (1–14) deve ser atingido por pelo menos um caso de teste.

| Caso de Teste | Condição simulada                          | Nós cobertos                         |
| ------------- | ------------------------------------------ | ------------------------------------ |
| T1            | Compra inválida (valor_compra ≤ 0)         | 1, 2                                 |
| T2            | Premium sem cupom                          | 1, 3, 4, 8, 10, 11, 13               |
| T3            | Premium com cupom (>100)                   | 1, 3, 4, 8, 9, 10, 11, 13            |
| T4            | Regular sem cupom                          | 1, 3, 5, 6, 8, 10, 11, 13            |
| T5            | Regular com cupom (>100, valor_final < 50) | 1, 3, 5, 6, 8, 9, 10, 11, 12, 13     |
| T6            | Outro cliente sem cupom (valor_final < 50) | 1, 3, 5, 7, 8, 10, 11, 12, 13        |

### Critério 2 — Todas-Arestas

Cada decisão deve ter seus ramos (verdadeiro/falso) percorridos.

| Decisão                     | Caminhos/Casos que cobrem     |
| --------------------------- | ----------------------------- |
| `valor_compra <= 0`         | Verdadeiro: T1 / Falso: T2–T6 |
| `tipo_cliente == "premium"` | V: T2–T3 / F: T4–T6           |
| `tipo_cliente == "regular"` | V: T4–T5 / F: T6              |
| `cupom == "DESC10"`         | V: T3–T5 / F: T2–T4–T6        |
| `valor_compra > 100`        | V: T3–T5 / F: C4–C7–C10       |
| `valor_final < 50`          | V: T5–T6 / F: T2–T3–T4        |

### Critério 3 — Todos-Caminhos

Todos os caminhos executáveis do grafo foram mapeados e associados a um caso de teste.

| Caminho | Caso de Teste (planejado)  | Condição Lógica                      |
| ------- | -------------------------- | ------------------------------------ |
| C1      | T1                         | Compra inválida                      |
| C2      | T2                         | Premium sem cupom                    |
| C3      | T3                         | Premium cupom válido (>100)          |
| C4      | T3 (variação ≤100)         | Premium cupom ≤100                   |
| C5      | T4                         | Regular sem cupom                    |
| C6      | T5                         | Regular com cupom (>100)             |
| C7      | T5 (variação ≤100)         | Regular cupom ≤100                   |
| C8      | T6                         | Outro sem cupom                      |
| C9      | T6 (variação cupom válido) | Outro cupom >100                     |
| C10     | T6 (variação cupom ≤100)   | Outro cupom ≤100                     |
| C11     | T3                         | Premium cupom + taxa entrega (<50)   |
| C12     | T5                         | Regular cupom + taxa entrega (<50)   |
| C13     | T6                         | Outro sem cupom + taxa entrega (<50) |