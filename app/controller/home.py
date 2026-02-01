from flask import Blueprint, request, render_template, jsonify, redirect, url_for, flash, session
from flask_login import current_user
from app.models.home import carregar_pokemons, buscar_pokemon_por_nome, listar_tipos, buscar_pokemons_por_prefixo
from app.models.favorite import listar_favoritos

home_bp = Blueprint("home", __name__)

POKEMONS_POR_PAGINA = 10 # Quantidade de pokémons exibidos por página na Pokédex.

@home_bp.route('/')
def home():
    """
    Página principal da Pokédex.
    """


    session["pokedex_return_url"] = request.full_path.rstrip("?") # Guarda a URL atual para que o usuário consiga voltar para a mesma página depois (com paginação, busca e filtro aplicado).

    # Carrega todos os pokémons e tipos disponíveis no CSV.
    pokemons = carregar_pokemons()
    tipos = listar_tipos() 

    # Carrega favoritos do usuário que está logado (se houver).
    favoritos = set()
    if current_user.is_authenticated:
        favoritos = listar_favoritos(current_user.id)

    # Captura filtros do usuário (via query string).
    search = request.args.get('search', '').lower()
    tipo_selecionado = request.args.get('tipo', '').lower()

    # Filtro por nome ou número.
    if search:
        pokemons = [
            p for p in pokemons
            if search in p['nome'].lower() or search == str(p['id'])
        ]

    # Filtro por tipo (tipo1 ou tipo2).
    if tipo_selecionado:
        pokemons = [
            p for p in pokemons
            if tipo_selecionado in (p['tipo1'], p['tipo2'])
        ]

    # Paginação.
    page = request.args.get('page', 1, type=int)
    inicio_index = (page - 1) * POKEMONS_POR_PAGINA
    fim_index = inicio_index + POKEMONS_POR_PAGINA
    total_paginas = (len(pokemons) - 1) // POKEMONS_POR_PAGINA + 1

    return render_template(
        "home.html",
        pokemons=pokemons[inicio_index:fim_index],
        tipos=tipos,
        favoritos=favoritos,
        page=page,
        total_paginas=total_paginas,
        logado=current_user.is_authenticated,
        tipo_selecionado=tipo_selecionado,
        search=search
    )

@home_bp.route("/pokemon/<int:pokemon_id>")
def pokemon_detail(pokemon_id):
    """
    Página de detalhes de um Pokémon.
    """
    pokemons = carregar_pokemons()
    pokemon = next((p for p in pokemons if p["id"] == pokemon_id), None) # Busca o Pokémon pelo ID recebido na URL.

    if not pokemon:
        flash(f"Pokémon #{pokemon_id} não foi encontrado!", "error")
        return redirect(url_for("home.home"))

    # Monta lista de evoluções.
    evolutions = []
    if pokemon.get("evolucoes"):
        for nome in pokemon["evolucoes"].split("|"):
            evo = buscar_pokemon_por_nome(nome)
            if evo:
                evolutions.append(evo)

    # Carrega favoritos do usuário que está logado (se houver).
    favoritos = set()
    if current_user.is_authenticated:
        favoritos = listar_favoritos(current_user.id)

    # URL de retorno para a Pokédex. Prioriza o parâmetro return_url, se não existir usa session como retorno.
    return_url = request.args.get("return_url")
    if not return_url:
        return_url = session.get("pokedex_return_url", url_for("home.home"))

    return render_template(
        "pokemon_detail.html",
        pokemon=pokemon,
        evolutions=evolutions,
        favoritos=favoritos,
        return_url=return_url
    )

@home_bp.route("/api/pokemons/search")
def api_search_pokemons():
    """
    Endpoint de autocomplete (busca rápida).
    """
    query = request.args.get("q", "").strip()

    # Evita retornar muitos resultados quando o usuário digitou pouco
    if len(query) < 2:
        return jsonify([])

    return jsonify(buscar_pokemons_por_prefixo(query))
