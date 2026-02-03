document.addEventListener("DOMContentLoaded", () => {
    // Botão responsável por limpar a busca quando nenhum Pokémon é encontrado
    const btnClear = document.getElementById("btn-clear-team-search");

    // Campo de busca por nome ou número do Pokémon
    const searchInput = document.getElementById("search");

    // Select de filtro por tipo (tipo1/tipo2)
    const typeSelect = document.getElementById("filter-type");

    if (!btnClear || !searchInput || !typeSelect) return;

    function limparBuscaEFiltro() {
        searchInput.value = "";
        typeSelect.value = "";

        // Dispara o evento para que o filter.js reaplique o filtro automaticamente
        searchInput.dispatchEvent(new Event("input"));
    }

    // Evento do botão "Limpar busca"
    btnClearSearch.addEventListener("click", limparBuscaEFiltro);
});