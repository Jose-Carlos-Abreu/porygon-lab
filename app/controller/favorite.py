from flask import Blueprint, jsonify, render_template, session
from app.models.favorite import salvar_favorito, remover_favorito, listar_favoritos
from app.models.home import carregar_pokemons
from app.decorators import session_required

favorite_bp = Blueprint("favorite", __name__)

@favorite_bp.route("/toggle/<int:pokemon_id>", methods=["POST"])
@session_required
def toggle(pokemon_id):
    """
    Alterna o estado de favorito de um Pokémon para o usuário logado. Retorna um JSON com o status da ação realizada.
    """
    usuario_id = session.get('usuario_id')
    favoritos_ids = listar_favoritos(usuario_id) # lista com IDs dos pokémons favoritados do usuário.

    # A função jsonify() converte dicionários em JSON, e enviar dados estruturados como resposta HTTP. 

    # Se já estiver favoritado, remove
    if pokemon_id in favoritos_ids:
        remover_favorito(usuario_id, pokemon_id)
        return jsonify({
            "status": "removed",
            "pokemon_id": pokemon_id
        })
    
    # Senão, adiciona aos favoritos
    else:
        salvar_favorito(usuario_id, pokemon_id)
        return jsonify({
            "status": "added",
            "pokemon_id": pokemon_id
        })

@favorite_bp.route("/favorites")
@session_required
def favorites():
    """
    Página que lista todos os Pokémons favoritados pelo usuário logado.
    """
    usuario_id = session.get('usuario_id')
    favoritos_ids = listar_favoritos(usuario_id) # lista com IDs dos pokémons favoritados do usuário.
    pokemons = carregar_pokemons() # Carrega todos os pokémons disponíveis no CSV.

    # Filtra apenas os pokémons favoritados
    favoritos = [
        p for p in pokemons
        if p["id"] in favoritos_ids
    ]

    return render_template(
        "favorites.html",
        pokemons=favoritos,
        logado='usuario_id' in session
    )