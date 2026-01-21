document.addEventListener("DOMContentLoaded", () => {
    const checkboxes = document.querySelectorAll('input[name="pokemons"]');
    const counter = document.getElementById("selection-counter");
    const warning = document.getElementById("limit-warning");

    function atualizarContador() {
        const total = document.querySelectorAll(
            'input[name="pokemons"]:checked'
        ).length;

        counter.querySelector("strong").textContent = total;
        return total;
    }

    function mostrarAviso() {
        warning.style.display = "block";

        clearTimeout(warning._timeout);
        warning._timeout = setTimeout(() => {
            warning.style.display = "none";
        }, 2500);
    }

    checkboxes.forEach(cb => {
        cb.addEventListener("change", () => {
            const card = cb.closest(".pokemon-card-container")
                           .querySelector(".pokemon-card");

            const totalSelecionados = atualizarContador();

            if (totalSelecionados > 6) {
                cb.checked = false;
                atualizarContador();
                mostrarAviso();
                return;
            }

            card.classList.toggle("selected", cb.checked);
        });
    });

    atualizarContador();
});