from pathlib import Path

CSV_PATH = Path("app/data/favorites.csv")
DELIMITER = ","


def listar_favoritos(user_id):
    favoritos = set()

    if not CSV_PATH.exists():
        return favoritos

    with open(CSV_PATH, "r", encoding="utf-8") as file:
        linhas = file.readlines()

    # Ignora o cabeçalho
    for linha in linhas[1:]:
        dados = linha.strip().split(DELIMITER)

        if len(dados) != 2:
            continue

        csv_user_id, pokemon_id = dados

        if int(csv_user_id) == user_id:
            favoritos.add(int(pokemon_id))

    return favoritos


def salvar_favorito(user_id, pokemon_id):
    arquivo_existe = CSV_PATH.exists()

    with open(CSV_PATH, "a", encoding="utf-8") as file:
        if not arquivo_existe:
            file.write("user_id,pokemon_id\n")

        file.write(f"{user_id},{pokemon_id}\n")


def remover_favorito(user_id, pokemon_id):
    if not CSV_PATH.exists():
        return

    with open(CSV_PATH, "r", encoding="utf-8") as file:
        linhas = file.readlines()

    novas_linhas = [linhas[0]]  # mantém o cabeçalho

    for linha in linhas[1:]:
        dados = linha.strip().split(DELIMITER)

        if len(dados) != 2:
            continue

        csv_user_id, csv_pokemon_id = dados

        if not (
            int(csv_user_id) == user_id and
            int(csv_pokemon_id) == pokemon_id
        ):
            novas_linhas.append(linha)

    with open(CSV_PATH, "w", encoding="utf-8") as file:
        file.writelines(novas_linhas)