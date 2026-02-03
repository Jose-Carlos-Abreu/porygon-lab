document.addEventListener("DOMContentLoaded", () => {
    // Elementos principais do filtro (input de busca + select de tipo)
    const searchInput = document.getElementById("search");
    const typeSelect = document.getElementById("filter-type");

    // Todos os cards de pokémon exibidos no grid
    const cards = document.querySelectorAll(".pokemon-card-container");

    // Aplica os filtros no grid de pokémons.
    // - Busca por nome (contém) ou ID (começa com)
    // - Filtra por tipo1/tipo2 usando dataset "types"
    function aplicarFiltro() {
        const textoBusca = searchInput.value.toLowerCase().trim();
        const tipoSelecionado = typeSelect.value.toLowerCase();

        let visiveis = 0;

        cards.forEach(card => {
            // Dados vindos do HTML via dataset
            const nomePokemon = card.dataset.name || "";
            const idPokemon = card.dataset.id;
            const tiposPokemon = card.dataset.types;
            
            // Filtro de texto:
            // - se texto vazio, passa
            // - se nome contém o texto, passa
            // - se id começa com o texto, passa
            const matchTexto =
                !textoBusca ||
                nomePokemon.includes(textoBusca) ||
                idPokemon.startsWith(textoBusca);

            // Filtro de tipo:
            // - se tipo vazio, passa
            // - se os tipos do pokémon contém o tipo selecionado, passa
            const matchTipo =
                !tipoSelecionado || tiposPokemon.includes(tipoSelecionado);

            const deveMostrar = matchTexto && matchTipo;

            // Mostra ou esconde o card conforme o resultado do filtro
            card.style.display = deveMostrar ? "block" : "none";

            if (deveMostrar) {
                totalVisiveis++;
            }
        });

        // Exibe mensagem de "nenhum encontrado" quando necessário
        const emptyState = document.getElementById("empty-state-team");
        if (emptyState) {
            emptyState.style.display = visiveis === 0 ? "block" : "none";
        }
    }

 // Eventos: ao digitar ou mudar o tipo, refaz o filtro
    searchInput.addEventListener("input", aplicarFiltro);
    typeSelect.addEventListener("change", aplicarFiltro);

    // Aplica uma vez ao carregar a página 
    aplicarFiltro();
});