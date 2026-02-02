from pathlib import Path

CSV_PATH = Path("app/data/pokemons.csv")
DELIMITER = ","


def ler_arquivo():
    """
    Lê o arquivo CSV de pokemons e retorna todas as linhas.
    """
    if not CSV_PATH.exists():
        return []
    
    with open(CSV_PATH, "r", encoding="utf-8") as file:
        linhas = file.readlines() 

    return linhas # retorna uma lista ['linha1\n', 'linha2\n', 'linha3'].


def converter_linha_em_dict(header, linha):
    """
    Converte uma linha do CSV em dict baseado no header, caso faltar alguma coluna na linha, ela vira string vazia.
    """
    valores = linha.strip().split(DELIMITER)

    dados = {}
    for i, coluna in enumerate(header):
        dados[coluna] = valores[i] if i < len(valores) else ""
        
    return dados


def carregar_pokemons():
    """
    Carrega todos os pokémons do CSV e retorna em formato de lista de dicionários.
    """
    pokemons = []
    linhas = ler_arquivo()

    if not linhas:
        return pokemons

    header = linhas[0].strip().split(DELIMITER)

    for linha in linhas[1:]:
        row = converter_linha_em_dict(header, linha)

        pokemons.append({
            "id": int(row["id"]),
            "nome": row["nome"],
            "tipo1": row.get("tipo1", ""),
            "tipo2": row.get("tipo2", ""),
            "imagem": row.get("imagem", ""),
            "altura": row.get("altura", ""),
            "peso": row.get("peso", ""),
            "categoria": row.get("categoria", ""),
            "habilidades": row.get("habilidades", ""),
            "evolucoes": row.get("evolucoes", ""),
            "fraquezas": row.get("fraquezas", "")
        })

    return pokemons


def listar_tipos():
    """
    Lista todos os tipos existentes no CSV (tipo1 e tipo2), sem repetição utilizando set().
    """
    tipos = set()
    linhas = ler_arquivo()

    if not linhas:
        return []

    header = linhas[0].strip().split(DELIMITER)

    for linha in linhas[1:]:
        row = converter_linha_em_dict(header, linha)

        if row.get("tipo1"):
            tipos.add(row["tipo1"].lower())
        if row.get("tipo2"):
            tipos.add(row["tipo2"].lower())

    return sorted(tipos)


def buscar_pokemon_por_nome(nome):
    """
    Busca um pokémon pelo nome exato no CSV, usado para apresentar cards de evoluções do pokemon.
    """
    nome = nome.strip().lower()
    linhas = ler_arquivo()

    if not linhas:
        return None

    header = linhas[0].strip().split(DELIMITER)

    for linha in linhas[1:]:
        row = converter_linha_em_dict(header, linha)

        if row["nome"].lower() == nome:
            return {
                "id": int(row["id"]),
                "nome": row["nome"],
                "imagem": f"/static/images/pokemons/{row['imagem']}"
            }

    return None


def buscar_pokemons_por_prefixo(texto, limite):
    """
    Busca pokémons cujo nome começa com o texto informado, usado no autocomplete de busca.
    """
    texto = texto.strip().lower()
    resultados = []

    if not texto:
        return resultados

    linhas = ler_arquivo()
    header = linhas[0].strip().split(DELIMITER)

    for linha in linhas[1:]:
        row = converter_linha_em_dict(header, linha)

        # O startswith() retorna True se a string começar com o valor especificado, caso contrário, retorna False.

        if row["nome"].lower().startswith(texto):
            resultados.append({
                "id": int(row["id"]),
                "nome": row["nome"]
            })

        if len(resultados) >= limite:
            break

    return resultados