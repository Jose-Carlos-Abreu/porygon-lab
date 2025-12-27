document.addEventListener("DOMContentLoaded", () => {
    const input = document.querySelector('#search');
    const container = document.getElementById("suggestions-container");

    if (!input || !container) return;

    input.addEventListener("input", async () => {
        const query = input.value.trim();

        if (query.length < 2) {
            container.innerHTML = "";
            container.style.display = "none";
            return;
        }

        try {
            const response = await fetch(`/pokedex/api/pokemons/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();

            container.innerHTML = "";

            if (!Array.isArray(data) || data.length === 0) {
                container.style.display = "none";
                return;
            }

            data.forEach(pokemon => {
                const item = document.createElement("div");
                item.classList.add("suggestion-item");

                item.innerHTML = `
                    <img src="/static/images/pokemons/${pokemon.id}.png" alt="${pokemon.nome}">
                    <span>#${pokemon.id} - ${pokemon.nome}</span>
                `;

                item.addEventListener("click", () => {
                    window.location.href = `/pokedex/pokemon/${pokemon.id}`;
                });

                container.appendChild(item);
            });

            container.style.display = "block";

        } catch (error) {
            console.error("Erro ao buscar sugestões:", error);
        }
    });

    document.addEventListener("click", (e) => {
        if (!container.contains(e.target) && e.target !== input) {
            container.style.display = "none";
        }
    });
});
