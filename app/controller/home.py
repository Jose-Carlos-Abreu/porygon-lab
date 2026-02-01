from flask import Blueprint, request, render_template, jsonify, redirect, url_for, flash, session
from app.models.home import carregar_pokemons, buscar_pokemon_por_nome, listar_tipos, buscar_pokemons_por_prefixo
from app.models.favorite import listar_favoritos

home_bp = Blueprint("home", __name__)

POKEMONS_POR_PAGINA = 10

@home_bp.route('/')
def home():
    session["pokedex_return_url"] = request.full_path.rstrip("?")
    pokemons = carregar_pokemons()
    tipos = listar_tipos() 

    favoritos = set()
    usuario_id = session.get('usuario_id')
    if usuario_id:
        favoritos = listar_favoritos(usuario_id)

    search = request.args.get('search', '').lower()
    tipo_selecionado = request.args.get('tipo', '').lower()

    if search:
        pokemons = [
            p for p in pokemons
            if search in p['nome'].lower() or search == str(p['id'])
        ]

    if tipo_selecionado:
        pokemons = [
            p for p in pokemons
            if tipo_selecionado in (p['tipo1'], p['tipo2'])
        ]

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
        logado='usuario_id' in session,
        tipo_selecionado=tipo_selecionado,
        search=search
    )

@home_bp.route("/pokemon/<int:pokemon_id>")
def pokemon_detail(pokemon_id):

    pokemons = carregar_pokemons()
    pokemon = next((p for p in pokemons if p["id"] == pokemon_id), None)

    if not pokemon:
        flash(f"Pokémon #{pokemon_id} não foi encontrado!", "error")
        return redirect(url_for("home.home"))

    evolutions = []
    if pokemon.get("evolucoes"):
        for nome in pokemon["evolucoes"].split("|"):
            evo = buscar_pokemon_por_nome(nome)
            if evo:
                evolutions.append(evo)

    favoritos = set()
    usuario_id = session.get('usuario_id')
    if usuario_id:
        favoritos = listar_favoritos(usuario_id)

    return_url = request.args.get("return_url")
    if not return_url:
        return_url = session.get("pokedex_return_url", url_for("home.home"))

    return render_template(
        "pokemon_detail.html",
        pokemon=pokemon,
        evolutions=evolutions,
        favoritos=favoritos,
        return_url=return_url,
        logado='usuario_id' in session
    )

@home_bp.route("/api/pokemons/search")
def api_search_pokemons():
    query = request.args.get("q", "").strip()

    if len(query) < 2:
        return jsonify([])

    return jsonify(buscar_pokemons_por_prefixo(query))
