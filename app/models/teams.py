from app.models.home import carregar_pokemons
import csv
import os

CSV_PATH = os.path.join('app', 'data', 'teams.csv')

def pegar_time_do_usuario(user_id):
    teams = []
    pokemons_all = carregar_pokemons()
    id_to_pokemon = {str(p['id']): p for p in pokemons_all}

    if not os.path.exists(CSV_PATH):
        return teams

    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))

        for index, row in enumerate(reader):
            if row.get('usuario_id') == str(user_id):
                poks = row.get('pokemons', '')
                pokemon_list = []

                for pid in poks.split(';'):
                    if pid and pid in id_to_pokemon:
                        pokemon_list.append(id_to_pokemon[pid])

                teams.append({
                    'id': index,
                    'nome': row.get('nome_time', 'Time sem nome'),
                    'pokemons': pokemon_list,
                    'total': len(pokemon_list)
                })

    return teams

def atualizar_time(usuario_id, team_id, nome_time, pokemons):
    if not os.path.exists(CSV_PATH):
        return False

    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    if team_id < 0 or team_id >= len(rows):
        return False

    if rows[team_id].get('usuario_id') != str(usuario_id):
        return False

    rows[team_id]['nome_time'] = nome_time
    rows[team_id]['pokemons'] = ';'.join(pokemons)

    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['usuario_id', 'nome_time', 'pokemons']
        )
        writer.writeheader()
        writer.writerows(rows)

    return True

def remover_time(usuario_id, team_id):
    if not os.path.exists(CSV_PATH):
        return False

    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    if team_id < 0 or team_id >= len(rows):
        return False

    if rows[team_id].get('usuario_id') != str(usuario_id):
        return False

    rows.pop(team_id)

    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['usuario_id', 'nome_time', 'pokemons']
        )
        writer.writeheader()
        writer.writerows(rows)

    return True

def salvar_novo_time(usuario_id, nome_time, pokemons):
    file_exists = os.path.exists(CSV_PATH)

    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['usuario_id', 'nome_time', 'pokemons']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'usuario_id': str(usuario_id),
            'nome_time': nome_time,
            'pokemons': ';'.join(pokemons)
        })

