
app/controller/teams.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.decorators import session_required
from app.models.teams import salvar_novo_time, pegar_time_do_usuario, remover_time, atualizar_time
from app.models.home import listar_tipos, carregar_pokemons

teams_bp = Blueprint('teams', __name__)

MAX_POKEMONS_POR_TIME = 6

def limpar_nome_time(nome_time):
    """
    Remove caracteres que podem quebrar o CSV.
    """
    if not nome_time:
        return ""

    nome_time = nome_time.strip()

    # Retira caracteres que possam quebrar o CSV e o campo pokemons
    nome_time = nome_time.replace(",", "")
    nome_time = nome_time.replace(";", "")
    nome_time = nome_time.replace("\n", "")
    nome_time = nome_time.replace("\r", "")

    return nome_time

def validar_pokemons_selecionados(selecionados, maximo):
    """
    Validar os pokémons recebidos do formulário, removes valores inválidos, duplicados e garantir limite máximo de pokemons.
    """
    if not selecionados:
        return []

    # remove duplicados mantendo ordem
    vistos = set()
    lista_final = []

    for pid in selecionados:
        pid = str(pid).strip()

        # só aceita número
        if not pid.isdigit():
            continue

        # remove repetidos
        if pid in vistos:
            continue

        vistos.add(pid)
        lista_final.append(pid)

        # trava no máximo permitido
        if len(lista_final) >= maximo:
            break

    return lista_final

@teams_bp.route('/teams')
@session_required
def list_teams():
    """
    Lista todos os times do usuário logado.
    """
    usuario_id = session.get('usuario_id') 
    teams = pegar_time_do_usuario(usuario_id) # Carrega os times do usuário no arquivo CSV.
    return render_template(
        'teams.html', 
        teams=teams, 
        logado='usuario_id' in session
    )


@teams_bp.route('/team/<int:team_id>/delete', methods=['POST'])
@session_required
def delete_team(team_id):
    """
    Remove um time do usuário logado com base no ID do time.
    """
    usuario_id = session.get('usuario_id')

    sucesso = remover_time(usuario_id, team_id) # retorna True ou False.

    if sucesso:
        flash('Time removido com sucesso.', 'success')
    else:
        flash('Não foi possível remover o time.', 'error')

    return redirect(url_for('teams.list_teams'))


@teams_bp.route('/team/<int:team_id>/edit', methods=['GET', 'POST'])
@session_required
def edit_team(team_id):
    """
    Edita um time existente.
    """
    usuario_id = session.get('usuario_id')

    # Carrega todos os pokémons e tipos disponíveis no CSV.
    pokemons = carregar_pokemons()
    tipos = listar_tipos()

    teams = pegar_time_do_usuario(usuario_id) # Carrega os times do usuário no arquivo CSV.
    
    team = next((t for t in teams if t['id'] == team_id), None) # Busca o time pelo ID dentro dos times do usuário.

    if not team:
        flash('Time não encontrado.', 'error')
        return redirect(url_for('teams.list_teams'))

    # Verifica se o method é POST, significando que o usuário enviou o formulário.
    if request.method == 'POST':
        nome_time = request.form.get('nome_time')
        selecionados = request.form.getlist('pokemons')

        nome_time = limpar_nome_time(nome_time)
        selecionados = validar_pokemons_selecionados(selecionados, MAX_POKEMONS_POR_TIME)

        # Validações do formulário.
        if not nome_time:
            flash('Informe o nome do time.', 'error')
            return redirect(request.url)

        if len(selecionados) == 0:
            flash('Selecione ao menos um Pokémon.', 'error')
            return redirect(request.url)

        if len(selecionados) > MAX_POKEMONS_POR_TIME:
            flash(f'Um time pode ter no máximo {MAX_POKEMONS_POR_TIME} Pokémons.', 'error')
            return redirect(request.url)
        
        atualizar_time(
            usuario_id=usuario_id,
            team_id=team_id,
            nome_time=nome_time,
            pokemons=selecionados
        )

        flash('Time atualizado com sucesso!', 'success')
        return redirect(url_for('teams.list_teams'))

    # Se o method é GET, exibe a tela com os dados atuais do time.
    return render_template(
        'team_new.html',
        pokemons=pokemons,
        team=team,
        tipos=tipos,
        edit=True,
        logado='usuario_id' in session
    )
    

@teams_bp.route('/team/new', methods=['GET', 'POST'])
@session_required
def new_team():
    """
    Cria um novo time para o usuário logado.
    """
    usuario_id = session.get('usuario_id')

    # Carrega todos os pokémons e tipos disponíveis no CSV.
    pokemons = carregar_pokemons()
    tipos = listar_tipos()

    # Verifica se o method é POST, significando que o usuário enviou o formulário.
    if request.method == 'POST':
        nome_time = request.form.get('nome_time')
        selecionados = request.form.getlist('pokemons')

        nome_time = limpar_nome_time(nome_time)
        selecionados = validar_pokemons_selecionados(selecionados, MAX_POKEMONS_POR_TIME)

        # Validações do formulário.
        if not nome_time:
            flash('Informe o nome do time.', 'error')
            return redirect(url_for('teams.new_team'))

        if len(selecionados) == 0:
            flash('Selecione ao menos um Pokémon.', 'error')
            return redirect(url_for('teams.new_team'))

        if len(selecionados) > MAX_POKEMONS_POR_TIME:
            flash(f'Um time pode ter no máximo {MAX_POKEMONS_POR_TIME} Pokémons.', 'error')
            return redirect(url_for('teams.new_team'))
        
        salvar_novo_time(
            usuario_id=usuario_id,
            nome_time=nome_time,
            pokemons=selecionados
        )

        flash('Time criado com sucesso!', 'success')
        return redirect(url_for('teams.list_teams'))

    # Se o method é GET, exibe o formulário vazio.
    return render_template('team_new.html', pokemons=pokemons, tipos=tipos, logado='usuario_id' in session)