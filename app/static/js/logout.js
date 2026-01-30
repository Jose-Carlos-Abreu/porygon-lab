document.addEventListener("DOMContentLoaded", () => {
    // Seleciona o botão de sair pelo CSS class que vimos no base.html
    const logoutBtn = document.querySelector(".btn-logout");

    // Só roda o código se o botão existir na página (para evitar erros na tela de login)
    if (logoutBtn) {
        logoutBtn.addEventListener("click", (e) => {
            e.preventDefault(); // Pausa o redirecionamento
            const logoutUrl = logoutBtn.href; // Guarda o link real (/logout)
            showLogoutModal(logoutUrl); // Chama o modal
        });
    }
});

function showLogoutModal(logoutUrl) {
    // Cria o fundo escuro
    const overlay = document.createElement('div');
    overlay.className = 'confirm-overlay';

    // Cria a caixinha branca
    const modal = document.createElement('div');
    modal.className = 'confirm-modal';

    // Preenche com o HTML do aviso de sair
    modal.innerHTML = `
        <div class="confirm-icon">🚪</div>
        <h3>Sair da conta?</h3>
        <p>Você será desconectado da Pokédex. Deseja continuar?</p>
        <div class="confirm-actions">
            <button id="btn-cancel-logout" class="btn-cancel">Cancelar</button>
            <button id="btn-confirm-logout" class="btn-confirm" style="background-color: #666;">Sair</button>
        </div>
    `;

    // Coloca na tela
    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    // Animação de entrada
    requestAnimationFrame(() => {
        overlay.classList.add('visible');
        modal.classList.add('visible');
    });

    // Botão Cancelar: fecha tudo
    document.getElementById('btn-cancel-logout').onclick = () => {
        closeModal(overlay);
    };

    // Botão Sair: redireciona para a URL original de logout
    document.getElementById('btn-confirm-logout').onclick = () => {
        window.location.href = logoutUrl;
    };
}

function closeModal(overlay) {
    overlay.classList.remove('visible');
    setTimeout(() => {
        overlay.remove();
    }, 300);
}