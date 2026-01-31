from pathlib import Path

CSV_PATH = Path("app/data/pokemons.csv")
DELIMITER = ","

def _ler_linhas():
    if not CSV_PATH.exists():
        return []

    with open(CSV_PATH, "r", encoding="utf-8") as file:
        return file.readlines()


def _parse_linha(header, linha):
    valores = linha.strip().split(DELIMITER)
    return dict(zip(header, valores))


def carregar_pokemons():
    pokemons = []
    linhas = _ler_linhas()

    if not linhas:
        return pokemons

    header = linhas[0].strip().split(DELIMITER)

    for linha in linhas[1:]:
        row = _parse_linha(header, linha)

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
    tipos = set()
    linhas = _ler_linhas()

    if not linhas:
        return []

    header = linhas[0].strip().split(DELIMITER)

    for linha in linhas[1:]:
        row = _parse_linha(header, linha)

        if row.get("tipo1"):
            tipos.add(row["tipo1"].lower())
        if row.get("tipo2"):
            tipos.add(row["tipo2"].lower())

    return sorted(tipos)


def buscar_pokemon_por_nome(nome):
    nome = nome.strip().lower()
    linhas = _ler_linhas()

    if not linhas:
        return None

    header = linhas[0].strip().split(DELIMITER)

    for linha in linhas[1:]:
        row = _parse_linha(header, linha)

        if row["nome"].lower() == nome:
            return {
                "id": int(row["id"]),
                "nome": row["nome"],
                "imagem": f"/static/images/pokemons/{row['imagem']}"
            }

    return None


def buscar_pokemons_por_prefixo(texto, limite=8):
    texto = texto.strip().lower()
    resultados = []

    if not texto:
        return resultados

    linhas = _ler_linhas()
    header = linhas[0].strip().split(DELIMITER)

    for linha in linhas[1:]:
        row = _parse_linha(header, linha)

        if row["nome"].lower().startswith(texto):
            resultados.append({
                "id": int(row["id"]),
                "nome": row["nome"]
            })

        if len(resultados) >= limite:
            break

    return resultados