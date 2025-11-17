# dynamic_gs.py — README

Este README descreve o arquivo `dynamic_gs.py` e explica, passo a passo, cada função presente no código, entradas/saídas, comportamento recursivo e uso de memoização.

## Integrantes
- Bruno Biletsky RM:554739
- Victor Freire RM:556191

## Entrada

O código possui uma listas de cards com titulo, custo e impacto. O usuário pode inserir mais cards durante a execução do programa.

## Objetivo

O código busca ajudar o funcionário a decidir quais tarefas escolher para obter maios impacto (produtividade) dentro das 8 horas de trabalho disponíveis. Uma espécie de problema da mochila, porém para produtividade e tomada de decisão no ambiente de trabalho. 

## Saida

O código exibe um dataframe ordenado e uma lista contendo a combinação das tarefas que causará maior impacto em vista do limite de tempo (8 horas).

## Visão geral

O script modela uma lista de "cards" (items) com `titulo`, `custo` (horas) e `impacto` (valor numérico). Ele contém implementações recursivas/memoizadas de algoritmos de ordenação (`merge_sort`, `quick_sort`), a função `merge` para o `merge_sort`, o algoritmo da mochila (`mochila`) para selecionar cards com base em capacidade (horas) maximizando impacto, e `gerar_relatorio` para formatar e imprimir o resultado.

O código também mantém caches (dicionários) para memoizar resultados e evitar recomputação em chamadas repetidas.

---

## Dados principais

`cards` — lista de dicionários representando tasks a atribuidas a funcionários durante o expediente. Cada dicionário contém as chaves:
- `titulo` (str)
- `custo` (int): custo em horas
- `impacto` (int): impacto positivo estimado

Exemplo de um card:

    {"titulo": "Dashboard de Engajamento", "custo": 4, "impacto": 9}


## Caches / memoização

O módulo define caches globais (dicionários) usados para memoização:

- `_merge_cache` — cache para a função `merge` (chave baseada nos conteúdos das duas listas).
- `_merge_sort_cache` — cache para `merge_sort` (chave: tupla representando a lista).
- `_quick_sort_cache` — cache para `quick_sort` (chave: tupla representando a lista).
- `_gerar_cache` — cache de relatório memoizado por `capacidade_total`.

Esses caches guardam resultados de subproblemas para acelerar chamadas repetidas evitar stack overflow.

---

## `pandas`

- Quais funções do módulo usam/retornam `DataFrame`?

- `cards_to_dataframe()` — pega a lista global `cards` e retorna um `pandas.DataFrame` com colunas `titulo`, `custo`, `impacto`.
- `sort_df_by_impact(df, inplace=False)` — recebe um `DataFrame` e retorna uma cópia ordenada por `impacto` em ordem decrescente (ou ordena in-place se `inplace=True`).


## Funções (explicação passo a passo)

Cada função em detalhe: o que faz, entradas, saídas, comportamento recursivo e notas de implementação.

### quick_sort(lista)

O que faz:
- Ordena uma lista de cards por `impacto` em ordem decrescente usando uma versão recursiva de Quick Sort (com partições) e memoização. Esta é a função de ordenação canônica usada no módulo.

Entradas:
- `lista` (list): lista de cards (dicionários) ou objetos com atributo `impacto`.

Saída:
- Retorna uma nova lista ordenada por `impacto` (decrescente).

Como funciona (passo a passo):
1. Define a função interna `_impacto(item)` que extrai o valor de `impacto` de um dicionário ou de um objeto.
2. Constrói uma chave `key` representando o conteúdo da lista (tupla de triplas ou pares) e verifica `_quick_sort_cache`.
3. Se a lista tem tamanho 0 ou 1, retorna uma cópia (caso base).
4. Escolhe um pivot (`pivot_val`) como o impacto do elemento do meio.
5. Particiona a lista em `left` (itens com impacto > pivot), `middle` (== pivot), `right` (< pivot).
6. Ordena recursivamente `left` e `right` (chamando `quick_sort`), concatena `quick_sort(left) + middle + quick_sort(right)`.
7. Memoiza (`_quick_sort_cache[key] = res[:]`) e retorna.

Notas:
- Aqui retornamos uma nova lista para simplicidade e compatibilidade com memoização.
- A memoização usa uma representação imutável da lista para servir de chave.


### mochila(i, capacidade, memo=None)

O que faz:
- Resolve o problema da mochila (0/1 knapsack) recursivamente: decide, para cada card `i`, se deve incluí-lo ou não para maximizar o impacto total sem ultrapassar a `capacidade` (horas).

Entradas:
- `i` (int): índice do card atual a considerar (inicia em 0).
- `capacidade` (int): capacidade remanescente (horas disponíveis).
- `memo` (dict | None): dicionário para memoização de subproblemas (chave `(i, capacidade)`). Se `None`, a função cria um novo dicionário.

Saída:
- Tupla `(impacto_maximo, lista_selecionados)` onde `impacto_maximo` é a soma máxima de impactos e `lista_selecionados` é a lista de cards escolhidos.

Como funciona (passo a passo):
1. Se `i == len(cards)` ou `capacidade == 0`, retorna `(0, [])` (casos base).
2. Verifica se a chave `(i, capacidade)` está em `memo`; se sim, retorna o valor memoizado.
3. Lê o card atual `atual = cards[i]`.
4. Se `atual['custo'] > capacidade`, não é possível incluir o card: chama recursivamente `mochila(i+1, capacidade, memo)`.
5. Caso contrário, calcula duas alternativas:
   - `sem_card`: resultado de `mochila(i+1, capacidade, memo)` (não incluir o card)
   - `com_card`: resultado de `mochila(i+1, capacidade - atual['custo'], memo)` e soma o `impacto` do `atual` ao valor retornado.
6. Compara `com_card` e `sem_card` por impacto; escolhe a melhor opção e monta a lista de selecionados adequadamente (`lista_com + [atual]` quando inclui).
7. Armazena o resultado em `memo[(i, capacidade)]` e retorna.

### gerar_relatorio(capacidade_total)

O que faz:
- Gera e imprime um relatório de cards selecionados para uma `capacidade_total` dada.
- A formatação da lista de selecionados usa uma função recursiva interna `format_sel`.
- O relatório inteiro é memoizado por `capacidade_total` em `_gerar_cache`.

Entradas:
- `capacidade_total` (int): horas disponíveis.

Saída:
- Imprime o relatório. Também armazena a string do relatório em `_gerar_cache[capacidade_total]`.

Como funciona (passo a passo):
1. Se `capacidade_total` já estiver em `_gerar_cache`, imprime o relatório memoizado e retorna.
2. Chama `mochila(0, capacidade_total, memo={})` para obter `(impacto_total, selecionados)`.
3. Ordena `selecionados` por `impacto` usando `quick_sort(selecionados)`.
4. Monta um cabeçalho (`header`) com informações gerais.
5. Define `format_sel(sel, idx=0)`, uma função recursiva que percorre `sel` e concatena linhas formatadas para cada card.
6. `body = format_sel(selecionados, 0)`, concatena e produz o relatório final.
7. Armazena o relatório em `_gerar_cache[capacidade_total]` e imprime.



### Bloco principal (`if __name__ == "__main__":`)

Comportamento:
- Loop interativo que permite ao usuário adicionar novos cards via input.
- Após sair do loop, o programa ordena `cards` com `quick_sort(cards)` e chama `gerar_relatorio(capacidade_total=8)`.


