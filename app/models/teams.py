from app.models.home import carregar_pokemons
import os

CSV_PATH = os.path.join('app', 'data', 'teams.csv')
DELIMITER = ','


def ler_arquivo():
    if not os.path.exists(CSV_PATH):
        return []

    with open(CSV_PATH, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    return linhas[1:]


def escrever_arquivo(linhas):
    with open(CSV_PATH, 'w', encoding='utf-8') as file:
        file.write('usuario_id,nome_time,pokemons\n')
        for linha in linhas:
            file.write(linha)


def pegar_time_do_usuario(user_id):
    teams = []
    linhas = ler_arquivo()

    pokemons_all = carregar_pokemons()
    id_to_pokemon = {str(p['id']): p for p in pokemons_all}

    for index, linha in enumerate(linhas):
        dados = linha.strip().split(DELIMITER)

        if len(dados) != 3:
            continue

        usuario_id, nome_time, pokemons_str = dados

        if usuario_id != str(user_id):
            continue

        pokemon_list = []
        for pid in pokemons_str.split(';'):
            if pid in id_to_pokemon:
                pokemon_list.append(id_to_pokemon[pid])

        teams.append({
            'id': index,
            'nome': nome_time or 'Time sem nome',
            'pokemons': pokemon_list,
            'total': len(pokemon_list)
        })

    return teams


def atualizar_time(usuario_id, team_id, nome_time, pokemons):
    linhas = ler_arquivo()

    if team_id < 0 or team_id >= len(linhas):
        return False

    dados = linhas[team_id].strip().split(DELIMITER)

    if len(dados) != 3:
        return False

    csv_usuario_id, _, _ = dados

    if csv_usuario_id != str(usuario_id):
        return False

    nova_linha = f"{usuario_id},{nome_time},{';'.join(pokemons)}\n"
    linhas[team_id] = nova_linha

    escrever_arquivo(linhas)
    return True


def remover_time(usuario_id, team_id):
    linhas = ler_arquivo()

    if team_id < 0 or team_id >= len(linhas):
        return False

    dados = linhas[team_id].strip().split(DELIMITER)

    if len(dados) != 3:
        return False

    csv_usuario_id, _, _ = dados

    if csv_usuario_id != str(usuario_id):
        return False

    linhas.pop(team_id)
    escrever_arquivo(linhas)
    return True


def salvar_novo_time(usuario_id, nome_time, pokemons):
    arquivo_existe = os.path.exists(CSV_PATH)

    with open(CSV_PATH, 'a', encoding='utf-8') as file:
        if not arquivo_existe:
            file.write('usuario_id,nome_time,pokemons\n')

        linha = f"{usuario_id},{nome_time},{';'.join(pokemons)}\n"
        file.write(linha)