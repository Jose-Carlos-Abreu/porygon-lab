document.addEventListener("DOMContentLoaded", () => {

    /* --- PARTE 1: FAVORITAR NA HOME (Mantive igual) --- */
    const stars = document.querySelectorAll(".favorite-star");

    stars.forEach(star => {
        star.addEventListener("click", async (e) => {
            e.preventDefault();
            e.stopPropagation();

            const pokemonId = star.dataset.pokemonId;

            try {
                const response = await fetch(`/favorite/toggle/${pokemonId}`, {
                    method: "POST",
                    headers: { "X-Requested-With": "XMLHttpRequest" }
                });

                const data = await response.json();

                if (data.status === "added") {
                    star.classList.add("active");
                }
                if (data.status === "removed") {
                    star.classList.remove("active");
                }
            } catch (error) {
                console.error("Erro ao favoritar:", error);
            }
        });
    });


    /* --- PARTE 2: REMOVER COM CONFIRMAÇÃO --- */
    const removeButtons = document.querySelectorAll(".remove-favorite-x");

    removeButtons.forEach(button => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();

            const pokemonId = button.dataset.pokemonId;
            
            // Chama a função que cria o modal bonito
            showConfirmationModal(pokemonId);
        });
    });
});

/* Função que cria o Modal de Confirmação na tela */
function showConfirmationModal(pokemonId) {
    // 1. Cria o fundo escuro (Overlay)
    const overlay = document.createElement('div');
    overlay.className = 'confirm-overlay';
    
    // 2. Cria o Card de Confirmação
    const modal = document.createElement('div');
    modal.className = 'confirm-modal';
    
    modal.innerHTML = `
        <div class="confirm-icon">⚠️</div>
        <h3>Tem certeza?</h3>
        <p>Deseja realmente remover este Pokémon dos seus favoritos?</p>
        <div class="confirm-actions">
            <button id="btn-cancel" class="btn-cancel">Cancelar</button>
            <button id="btn-confirm" class="btn-confirm">Sim, remover</button>
        </div>
    `;

    // 3. Adiciona na tela
    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    // 4. Animação de entrada
    requestAnimationFrame(() => {
        overlay.classList.add('visible');
        modal.classList.add('visible');
    });

    // 5. Ação do botão CANCELAR
    document.getElementById('btn-cancel').onclick = () => {
        closeModal(overlay);
    };

    // 6. Ação do botão CONFIRMAR
    document.getElementById('btn-confirm').onclick = async () => {
        await removeFavorite(pokemonId); // Chama a função real de remover
        closeModal(overlay);
    };
}

/* Função para fechar o modal */
function closeModal(overlay) {
    overlay.classList.remove('visible');
    setTimeout(() => {
        overlay.remove();
    }, 300); // Espera a animação acabar
}

/* Função Lógica de Remover (a que você já tinha) */
async function removeFavorite(pokemonId) {
    const card = document.getElementById(`card-${pokemonId}`);
    const grid = document.getElementById("favorites-grid");
    const header = document.getElementById("favorites-header");

    try {
        const response = await fetch(`/favorite/toggle/${pokemonId}`, {
            method: "POST",
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });

        const data = await response.json();

        if (data.status === "removed" && card) {
            // Efeito visual de saída do card
            card.style.transform = "scale(0.8)";
            card.style.opacity = "0";
            
            setTimeout(() => {
                card.remove();
                checkIfEmpty(grid, header);
            }, 300);
        }
    } catch (error) {
        console.error("Erro ao remover favorito:", error);
    }
}

/* Verifica se ficou vazio e mostra msg */
function checkIfEmpty(grid, header) {
    if (grid && grid.children.length === 0) {
        grid.remove();
        if (header) header.remove();

        const emptyState = document.createElement("div");
        emptyState.className = "empty-state";
        emptyState.innerHTML = `
            <div class="empty-icon"></div>
            <img src="/static/images/ui/icon_favoritos.png" alt="favoritos" class="empty-icon">
            <h2>Nenhum Pokémon favorito</h2>
            <p>
                Você ainda não favoritou nenhum Pokémon.<br>
                Explore a Pokédex e marque seus favoritos!
            </p>

            <a href="/" class="btn-back">
                ← Voltar para Pokédex
            </a>
        `;
        document.querySelector("main").appendChild(emptyState);
    }
}