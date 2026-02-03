document.addEventListener("DOMContentLoaded", () => {
    const LIMITE_POKEMONS = 6; // Limite máximo de Pokémons permitidos no time

    const checkboxes = document.querySelectorAll('input[name="pokemons"]');  // Todos os checkboxes dos Pokémons no formulário

    // Elementos de visuais (contador e aviso)
    const counter = document.getElementById("selection-counter");
    const warning = document.getElementById("limit-warning");

    // Se não existir nada disso na página, não executa o script
    if (!checkboxes.length || !counter || !warning) {
        return;
    }

    // Timeout usado para esconder o aviso automaticamente
    let warningTimeout = null;

    // Atualiza o contador "Selecionados: X/6" o X é a qauntidade de checkboxes marcados.
    function atualizarContadorSelecionados() {
        const totalSelecionados = document.querySelectorAll(
            'input[name="pokemons"]:checked'
        ).length;

        const strong = counter.querySelector("strong");
        if (strong) {
            strong.textContent = totalSelecionados;
        }

        return totalSelecionados;
    }

    // Mostra o aviso de limite excedido e esconde após alguns segundos.
    function mostrarAvisoLimite() {
        warning.style.display = "block";

        // Evita acumular vários timeouts
        if (warningTimeout) {
            clearTimeout(warningTimeout);
        }

        warningTimeout = setTimeout(() => {
            warning.style.display = "none";
        }, 2500);
    }

    // Ativa ou desativa o visual do card baseado no estado do checkbox, usa a classe CSS "selected".
    function atualizarVisualDoCard(checkbox) {
        const container = checkbox.closest(".pokemon-card-container");
        if (!container) return;

        const card = container.querySelector(".pokemon-card");
        if (!card) return;

        card.classList.toggle("selected", checkbox.checked);
    }

    // Adiciona evento de change em cada checkbox
    checkboxes.forEach((checkbox) => {
        checkbox.addEventListener("change", () => {
            const totalSelecionados = atualizarContadorSelecionados();

            // Se passar do limite, desfaz a seleção e mostra aviso
            if (totalSelecionados > LIMITE_POKEMONS) {
                checkbox.checked = false;
                atualizarContadorSelecionados();
                mostrarAvisoLimite();
                return;
            }

            // Atualiza o visual do card normalmente
            atualizarVisualDoCard(checkbox);
        });
    });

    // Inicializa o contador ao abrir a página (principalmente no modo edição)
    atualizarContadorSelecionados();
});
