document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search");
    const typeSelect = document.getElementById("filter-type");
    const cards = document.querySelectorAll(".pokemon-card-container");

    function aplicarFiltro() {
        const texto = searchInput.value.toLowerCase().trim();
        const tipo = typeSelect.value.toLowerCase();

        let visiveis = 0;

        cards.forEach(card => {
            const nome = card.dataset.name;
            const id = card.dataset.id;
            const tipos = card.dataset.types;

            const matchTexto =
                !texto ||
                nome.includes(texto) ||
                id.startsWith(texto);

            const matchTipo =
                !tipo || tipos.includes(tipo);

            const mostrar = matchTexto && matchTipo;

            card.style.display = mostrar ? "block" : "none";

            if (mostrar) visiveis++;
        });

        const emptyState = document.getElementById("empty-state-team");
        if (emptyState) {
            emptyState.style.display = visiveis === 0 ? "block" : "none";
        }
    }

    searchInput.addEventListener("input", aplicarFiltro);
    typeSelect.addEventListener("change", aplicarFiltro);

    aplicarFiltro();
});