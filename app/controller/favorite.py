from flask import Blueprint, redirect, url_for, flash, request, jsonify, render_template, session
from app.models.favorite import salvar_favorito, remover_favorito, listar_favoritos
from app.models.home import carregar_pokemons
from app.decorators import session_required

favorite_bp = Blueprint("favorite", __name__)

@favorite_bp.route("/toggle/<int:pokemon_id>", methods=["POST"])
@session_required
def toggle(pokemon_id):
    usuario_id = session.get('usuario_id')
    favoritos = listar_favoritos(usuario_id)

    if pokemon_id in favoritos:
        remover_favorito(usuario_id, pokemon_id)
        return jsonify({
            "status": "removed",
            "pokemon_id": pokemon_id
        })
    else:
        salvar_favorito(usuario_id, pokemon_id)
        return jsonify({
            "status": "added",
            "pokemon_id": pokemon_id
        })

@favorite_bp.route("/favorites")
@session_required
def favorites():
    usuario_id = session.get('usuario_id')
    favoritos_ids = listar_favoritos(usuario_id)

    pokemons = carregar_pokemons()

    favoritos = [
        p for p in pokemons
        if p["id"] in favoritos_ids
    ]

    return render_template(
        "favorites.html",
        pokemons=favoritos,
        logado='usuario_id' in session
    )