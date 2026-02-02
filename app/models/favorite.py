from pathlib import Path

CSV_PATH = Path("app/data/favorites.csv")
DELIMITER = ","


def ler_arquivo():
    """
    Lê o arquivo CSV de favoritos e retorna todas as linhas.
    """
    if not CSV_PATH.exists():
        return []

    with open(CSV_PATH, "r", encoding="utf-8") as file:
        linhas = file.readlines() # retorna uma lista ['linha1\n', 'linha2\n', 'linha3']

    return linhas


def converter_linha_em_dict(header, linha):
    """
    Converte uma linha do CSV em dict baseado no header, caso faltar alguma coluna na linha, ela vira string vazia.
    """
    valores = linha.strip().split(DELIMITER)

    dados = {}
    for i, coluna in enumerate(header):
        dados[coluna] = valores[i] if i < len(valores) else ""

    return dados

def listar_favoritos(user_id):
    """
    Retorna um set() com os IDs dos pokémons favoritados por um usuário.
    """
    favoritos = set()
    linhas = ler_arquivo()

    if not linhas:
        return favoritos

    header = linhas[0].strip().split(DELIMITER)

    for linha in linhas[1:]:
        row = converter_linha_em_dict(header, linha)
        
        # Garante que a linha tenha as colunas necessárias.
        if not row.get("user_id") or not row.get("pokemon_id"):
            continue

        # Filtra apenas favoritos do usuário informado.
        if int(row["user_id"]) == user_id:
            favoritos.add(int(row["pokemon_id"]))

    return favoritos


def salvar_favorito(user_id, pokemon_id):
    """
    Salva um favorito no CSV.
    """
    arquivo_existe = CSV_PATH.exists()
  
    with open(CSV_PATH, "a", encoding="utf-8") as file:
        # Se o arquivo não existir, cria o arquivo e adiciona o cabeçalho.
        if not arquivo_existe:
            file.write("user_id,pokemon_id\n")

        file.write(f"{user_id},{pokemon_id}\n")


def remover_favorito(user_id, pokemon_id):
    """
    Remove um favorito do CSV.
    """
    linhas = ler_arquivo()

    if not linhas:
        return

    header = linhas[0]
    colunas = header.strip().split(DELIMITER)

    novas_linhas = [header]

    for linha in linhas[1:]:
        row = converter_linha_em_dict(colunas, linha)

        if not row.get("user_id") or not row.get("pokemon_id"):
            continue

        # Mantém as linhas que não são o favorito a ser removido, verificando id do usuario e id do pokemon.
        if not (int(row["user_id"]) == user_id and int(row["pokemon_id"]) == pokemon_id):
            novas_linhas.append(linha)

    with open(CSV_PATH, "w", encoding="utf-8") as file:
        file.writelines(novas_linhas)