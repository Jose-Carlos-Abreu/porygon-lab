document.addEventListener("DOMContentLoaded", () => {
    const inputBusca = document.querySelector("#search");
    const containerSugestoes = document.getElementById("suggestions-container");

    if (!inputBusca || !containerSugestoes) {
        return;
    }

    const MIN_CARACTERES_PARA_BUSCAR = 2;

    // Esconde e limpa as sugestões da tela.
    function limparSugestoes() {
        containerSugestoes.innerHTML = "";
        containerSugestoes.style.display = "none";
    }

    // Monta o HTML de um item de sugestão e adiciona o evento de clique.
    function criarItemSugestao(pokemon) {
        const item = document.createElement("div");
        item.classList.add("suggestion-item");

        item.innerHTML = `
            <img src="/static/images/pokemons/${pokemon.id}.png" alt="${pokemon.nome}">
            <span>#${pokemon.id} - ${pokemon.nome}</span>
        `;

        // permite que o usuario clik e seja direcionado para a pagina de detalhes do pokemon
        item.addEventListener("click", () => {
            window.location.href = `/pokedex/pokemon/${pokemon.id}`;
        });

        return item;
    }

    // Apresenta lista de sugestões dentro do container.
    function mostrarSugestoes(lista) {
        containerSugestoes.innerHTML = "";

        if (!Array.isArray(lista) || lista.length === 0) {
            containerSugestoes.style.display = "none";
            return;
        }

        lista.forEach((pokemon) => {
            const item = criarItemSugestao(pokemon);
            containerSugestoes.appendChild(item);
        });

        containerSugestoes.style.display = "block";
    }

    // Busca sugestões no backend usando o endpoint de autocomplete.
    async function buscarSugestoes(query) {
        const url = `/pokedex/api/pokemons/search?q=${encodeURIComponent(query)}`;

        const response = await fetch(url);
        return response.json();
    }

    // É acionado quando o usuário digita no input.
    inputBusca.addEventListener("input", async () => {
        const query = inputBusca.value.trim();

        if (query.length < MIN_CARACTERES_PARA_BUSCAR) {
            limparSugestoes();
            return;
        }

        try {
            const sugestoes = await buscarSugestoes(query);
            mostrarSugestoes(sugestoes);
        } catch (error) {
            console.error("Erro ao buscar sugestões:", error);
            limparSugestoes();
        }
    });

    // Quando clicar fora do input e do container fecha as sugestões
    document.addEventListener("click", (event) => {
        const clicouNoInput = event.target === inputBusca;
        const clicouDentroDoContainer = containerSugestoes.contains(event.target);

        if (!clicouNoInput && !clicouDentroDoContainer) {
            limparSugestoes();
        }
    });
});