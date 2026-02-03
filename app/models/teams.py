from app.models.home import carregar_pokemons
from pathlib import Path

CSV_PATH = Path('app/data/teams.csv')
DELIMITER = ','


def ler_arquivo():
    """
    Lê o arquivo CSV de times e retorna todas as linhas.
    """
    if not CSV_PATH.exists():
        return []

    with open(CSV_PATH, 'r', encoding='utf-8') as file:
        linhas = file.readlines() # retorna uma lista ['linha1\n', 'linha2\n', 'linha3'].

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


def escrever_arquivo(linhas):
    """
    Sobrescreve o arquivo CSV com os dados informados.
    """
    with open(CSV_PATH, 'w', encoding='utf-8') as file:
        file.write('usuario_id,nome_time,pokemons\n')

        for linha in linhas:
            file.write(linha)


def pegar_time_do_usuario(user_id):
    """
    Retorna todos os times cadastrados por um usuário específico.
    """
    teams = []
    linhas = ler_arquivo()

    if not linhas:
        return teams

    header = linhas[0].strip().split(DELIMITER)

    pokemons_all = carregar_pokemons() # Carrega todos os pokémons disponíveis no CSV.
    id_to_pokemon = {str(p['id']): p for p in pokemons_all}


    for index, linha in enumerate(linhas[1:]):
        row = converter_linha_em_dict(header, linha)

        usuario_id_csv = row.get("usuario_id", "")
        nome_time = row.get("nome_time", "")
        pokemons_str = row.get("pokemons", "")

        # Só retorna times do usuário logado.
        if usuario_id_csv != str(user_id):
            continue
        
        # Monta a lista de pokémons do time.
        pokemon_list = []
        for pid in pokemons_str.split(';'):
            if pid in id_to_pokemon:
                pokemon_list.append(id_to_pokemon[pid])

        teams.append({
            'id': index, # index é relativo aos times criados pelo usuário.
            'nome': nome_time or 'Time sem nome',
            'pokemons': pokemon_list,
            'total': len(pokemon_list)
        })

    return teams


def atualizar_time(usuario_id, team_id, nome_time, pokemons):
    """
    Atualiza um time existente do usuário.
    """
    linhas = ler_arquivo()
    
    if not linhas:
        return False

    index_real = team_id + 1 # corrige o index, por causa do cabeçalho.
    
    # Verifica o índice no arquivo
    if index_real < 1 or index_real >= len(linhas):
        return False

    header = linhas[0].strip().split(DELIMITER)
    row = converter_linha_em_dict(header, linhas[index_real])

    # Verifica se o time pertence ao usuário logado
    if row.get("usuario_id") != str(usuario_id):
        return False

    # Atualiza o time com os novos dados
    nova_linha = f"{usuario_id},{nome_time},{';'.join(pokemons[:6])}\n"
    linhas[index_real] = nova_linha

    escrever_arquivo(linhas[1:]) # Regrava apenas as linhas de dados
    return True


def remover_time(usuario_id, team_id):
    """
    Remove um time do usuário pelo ID.
    """
    linhas = ler_arquivo()

    index_real = team_id + 1 # corrige o index, por causa do cabeçalho.

    # Verifica o índice no arquivo
    if index_real < 1 or index_real >= len(linhas):
        return False
    
    header = linhas[0].strip().split(DELIMITER)
    row = converter_linha_em_dict(header, linhas[index_real])

    # Verifica se o time pertence ao usuário logado
    if row.get("usuario_id") != str(usuario_id):
        return False

    linhas.pop(index_real) # Remove a linha do time
    escrever_arquivo(linhas[1:]) # Regrava apenas as linhas de dados
    return True


def salvar_novo_time(usuario_id, nome_time, pokemons):
    """
    Salva um novo time no CSV.
    """
    arquivo_existe = CSV_PATH.exists()

    with open(CSV_PATH, 'a', encoding='utf-8') as file:
        if not arquivo_existe:
            # Se o arquivo não existir, cria o arquivo e adiciona o cabeçalho.
            file.write('usuario_id,nome_time,pokemons\n')

        linha = f"{usuario_id},{nome_time},{';'.join(pokemons[:6])}\n"
        file.write(linha)