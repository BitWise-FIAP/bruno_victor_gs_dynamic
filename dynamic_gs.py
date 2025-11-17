# Lista de cards com título, custo (em horas) e impacto positivo estimado após resolução

cards = [
    {"titulo": "Dashboard de Engajamento", "custo": 4, "impacto": 9},
    {"titulo": "Análise de Reuniões", "custo": 5, "impacto": 12},
    {"titulo": "Checklist Inteligente", "custo": 2, "impacto": 5},
    {"titulo": "Gestão de Agenda", "custo": 4, "impacto": 9},
    {"titulo": "Análise de Sentimentos", "custo": 5, "impacto": 11},
    {"titulo": "Relatório de Produtividade", "custo": 3, "impacto": 8},
    {"titulo": "Resumo de Documentos", "custo": 3, "impacto": 7},
    {"titulo": "Gestão de Tarefas", "custo": 2, "impacto": 6},
    {"titulo": "Organizador de Projetos", "custo": 5, "impacto": 12},
    {"titulo": "Análise de Riscos", "custo": 4, "impacto": 10},
    {"titulo": "Integração com API Externa", "custo": 3, "impacto": 7},
    {"titulo": "Automação de Relatórios", "custo": 4, "impacto": 9},
    {"titulo": "Melhoria de Onboarding", "custo": 2, "impacto": 6},
    {"titulo": "Cache Inteligente", "custo": 3, "impacto": 8},
    {"titulo": "Otimização de Busca", "custo": 5, "impacto": 11},
    {"titulo": "Refatoração do Módulo X", "custo": 6, "impacto": 10},
    {"titulo": "Validação de Dados", "custo": 2, "impacto": 5},
    {"titulo": "Painel de Alertas", "custo": 3, "impacto": 8},
    {"titulo": "Teste A/B Básico", "custo": 4, "impacto": 9},
    {"titulo": "Central de Notificações", "custo": 4, "impacto": 10},
    {"titulo": "SDK para Clientes", "custo": 7, "impacto": 13},
    {"titulo": "Melhoria na Segurança", "custo": 5, "impacto": 12},
    {"titulo": "Documentação Técnica", "custo": 2, "impacto": 6},
    {"titulo": "Exportar CSV", "custo": 1, "impacto": 4},
    {"titulo": "Importação em Massa", "custo": 3, "impacto": 7},
    {"titulo": "Monitoramento de Performance", "custo": 4, "impacto": 11},
    {"titulo": "Suporte Multilíngue", "custo": 5, "impacto": 9},
    {"titulo": "Assistente por Chatbot", "custo": 6, "impacto": 12},
    {"titulo": "Painel de KPI Avançado", "custo": 6, "impacto": 14},
]

# Caches para memoização (usados por funções recursivas que recebem
# estruturas não-hashable como listas/dicts).
_quick_sort_cache = {}
_mochila_cache = {}
_gerar_cache = {}


def quick_sort(lista):
    """Quick sort recursivo e memoizado por 'impacto' (decrescente).

    Como os itens são dicts, construímos uma chave baseada no
    conteúdo para memoização. Retorna uma nova lista ordenada.
    """
    def _impacto(item):
        if isinstance(item, dict):
            return item.get("impacto", 0)
        return getattr(item, "impacto", 0)

    # chave representando o conteúdo da lista
    key = tuple((x.get("impacto", 0), x.get("titulo", ""), x.get("custo", 0))
                if isinstance(x, dict) else (getattr(x, "impacto", 0),)
                for x in lista)
    if key in _quick_sort_cache:
        return _quick_sort_cache[key][:]

    if len(lista) <= 1:
        res = lista[:]
    else:
        pivot_val = _impacto(lista[len(lista) // 2])
        left = [x for x in lista if _impacto(x) > pivot_val]
        middle = [x for x in lista if _impacto(x) == pivot_val]
        right = [x for x in lista if _impacto(x) < pivot_val]

        res = quick_sort(left) + middle + quick_sort(right)

    _quick_sort_cache[key] = res[:]  # armazena cópia
    return res


# --- Utilitários para DataFrame ---
try:
    import pandas as pd
except Exception:
    pd = None


def cards_to_dataframe():
    """Converte a lista global `cards` em um `pandas.DataFrame`.

    Retorna o DataFrame com colunas exatamente: 'titulo','custo','impacto'.
    """
    if pd is None:
        raise ImportError("pandas não está instalado. Instale com 'pip install pandas'.")
    return pd.DataFrame(cards)


def sort_df_by_impact(df, inplace=False):
    """Retorna um DataFrame ordenado por 'impacto' (decrescente).

    - Se `inplace=True` tenta ordenar no lugar quando possível.
    - `df` deve conter a coluna 'impacto'.
    """
    if pd is None:
        raise ImportError("pandas não está instalado. Instale com 'pip install pandas'.")
    if not isinstance(df, pd.DataFrame):
        raise TypeError("`df` deve ser um pandas.DataFrame")
    if 'impacto' not in df.columns:
        raise ValueError("DataFrame precisa conter a coluna 'impacto'")

    if inplace:
        df.sort_values(by='impacto', ascending=False, inplace=True)
        return df
    return df.sort_values(by='impacto', ascending=False).reset_index(drop=True)


def mochila(i, capacidade, memo=None):
    """Problema da mochila (recursivo) com memoização.

    Usa um dicionário `memo` passado (ou criado) para armazenar subproblemas
    por chave (i, capacidade).
    """
    if memo is None:
        memo = {}

    if i == len(cards) or capacidade == 0:
        return 0, []

    chave = (i, capacidade)
    if chave in memo:
        return memo[chave]

    atual = cards[i]
    if atual["custo"] > capacidade:
        resultado = mochila(i + 1, capacidade, memo)
    else:
        sem_card, lista_sem = mochila(i + 1, capacidade, memo)
        com_card, lista_com = mochila(i + 1, capacidade - atual["custo"], memo)
        com_card += atual["impacto"]

        if com_card > sem_card:
            resultado = (com_card, lista_com + [atual])
        else:
            resultado = (sem_card, lista_sem)

    memo[chave] = resultado
    return resultado


def gerar_relatorio(capacidade_total):
    """Gera e imprime relatório. A formatação da lista de selecionados é feita
    por uma função recursiva; o resultado final é memoizado por
    `capacidade_total` para evitar recomputação do texto do relatório.
    """
    if capacidade_total in _gerar_cache:
        print(_gerar_cache[capacidade_total])
        return

    impacto_total, selecionados = mochila(0, capacidade_total, memo={})
    selecionados = quick_sort(selecionados)

    header = (
        f"\n📊 Relatório de Cards Selecionados\n"
        f"Capacidade disponível: {capacidade_total} horas\n"
        f"Impacto total alcançado: {impacto_total}\n\n"
        "Cards escolhidos:\n"
    )

    def format_sel(sel, idx=0):
        # função recursiva que formata cada item da lista
        if idx >= len(sel):
            return ""
        c = sel[idx]
        linha = f"- {c['titulo']} (Custo: {c['custo']}h, Impacto: {c['impacto']})\n"
        return linha + format_sel(sel, idx + 1)

    body = format_sel(selecionados, 0)
    relatório = header + body
    _gerar_cache[capacidade_total] = relatório
    print(relatório)


if __name__ == "__main__":
    # Apresenta todos os cards atuais ordenados por impacto (decrescente)
    try:
        if pd is not None:
            df = cards_to_dataframe()
            df_sorted = sort_df_by_impact(df)
            print("\n📋 Cards atuais (ordenados por impacto):")
            try:
                # imprime sem os índices para ficar mais limpo
                print(df_sorted.to_string(index=False))
            except Exception:
                # fallback simples
                print(df_sorted)
        else:
            # sem pandas: usa quick_sort para apresentar
            print("\n📋 Cards atuais (ordenados por impacto):")
            for c in quick_sort(cards):
                print(f"- {c['titulo']} (Custo: {c['custo']}h, Impacto: {c['impacto']})")
    except Exception as e:
        print(f"Não foi possível exibir os cards ordenados: {e}")

    op = 1
    while op != 0:
        match op:
            case 0:
                print("Encerrando o programa.")
            case 1:
                print("\nAdicionando um novo card.")
                titulo = input("Digite o título do card: ")
                custo = int(input("Digite o custo (em horas) do card: "))
                impacto = int(input("Digite o impacto positivo estimado do card: "))
                cards.append({"titulo": titulo, "custo": custo, "impacto": impacto})
        op = int(input("\nEncerrar o programa (0), adicionar card (1): "))
        cards.append({"titulo": f"Card {len(cards)+1}", "custo": op, "impacto": op * 2})
    # Ordena cards por impacto decrescente antes de gerar relatório
    cards = quick_sort(cards)
    gerar_relatorio(capacidade_total=8)


