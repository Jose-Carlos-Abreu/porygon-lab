from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.teams import salvar_novo_time, pegar_time_do_usuario, remover_time, atualizar_time
from app.models.home import listar_tipos, carregar_pokemons

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/teams')
@login_required
def list_teams():
    teams = pegar_time_do_usuario(current_user.id)
    return render_template('teams.html', teams=teams)

@teams_bp.route('/team/<int:team_id>/delete', methods=['POST'])
@login_required
def delete_team(team_id):
    sucesso = remover_time(current_user.id, team_id)

    if sucesso:
        flash('Time removido com sucesso.', 'success')
    else:
        flash('Não foi possível remover o time.', 'error')

    return redirect(url_for('teams.list_teams'))

@teams_bp.route('/team/<int:team_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):
    pokemons = carregar_pokemons()
    tipos = listar_tipos()
    teams = pegar_time_do_usuario(current_user.id)

    team = next((t for t in teams if t['id'] == team_id), None)
    if not team:
        flash('Time não encontrado.', 'error')
        return redirect(url_for('teams.list_teams'))

    if request.method == 'POST':
        nome_time = request.form.get('nome_time')
        selecionados = request.form.getlist('pokemons')

        if not nome_time:
            flash('Informe o nome do time.', 'error')
            return redirect(request.url)

        if len(selecionados) == 0:
            flash('Selecione ao menos um Pokémon.', 'error')
            return redirect(request.url)

        if len(selecionados) > 6:
            flash('Um time pode ter no máximo 6 Pokémons.', 'error')
            return redirect(request.url)

        atualizar_time(
            usuario_id=current_user.id,
            team_id=team_id,
            nome_time=nome_time,
            pokemons=selecionados
        )

        flash('Time atualizado com sucesso!', 'success')
        return redirect(url_for('teams.list_teams'))

    return render_template(
        'team_new.html',
        pokemons=pokemons,
        team=team,
        tipos=tipos,
        edit=True
    )
    
@teams_bp.route('/team/new', methods=['GET', 'POST'])
@login_required
def new_team():
    pokemons = carregar_pokemons()
    tipos = listar_tipos()

    if request.method == 'POST':
        nome_time = request.form.get('nome_time')
        selecionados = request.form.getlist('pokemons')

        if not nome_time:
            flash('Informe o nome do time.', 'error')
            return redirect(url_for('teams.new_team'))

        if len(selecionados) == 0:
            flash('Selecione ao menos um Pokémon.', 'error')
            return redirect(url_for('teams.new_team'))

        if len(selecionados) > 6:
            flash('Um time pode ter no máximo 6 Pokémons.', 'error')
            return redirect(url_for('teams.new_team'))

        salvar_novo_time(
            usuario_id=current_user.id,
            nome_time=nome_time,
            pokemons=selecionados
        )

        flash('Time criado com sucesso!', 'success')
        return redirect(url_for('teams.list_teams'))

    return render_template('team_new.html', pokemons=pokemons, tipos=tipos)