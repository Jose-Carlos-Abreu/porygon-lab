document.addEventListener("DOMContentLoaded", () => {
    const deleteForms = document.querySelectorAll(".delete-team-form");

    deleteForms.forEach(form => {
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            showDeleteTeamModal(form);
        });
    });
});

function showDeleteTeamModal(form) {
    const overlay = document.createElement('div');
    overlay.className = 'confirm-overlay';

    const modal = document.createElement('div');
    modal.className = 'confirm-modal';

    modal.innerHTML = `
        <div class="confirm-icon">🗑️</div>
        <h3>Excluir Time?</h3>
        <p>Essa ação não pode ser desfeita. Deseja realmente excluir este time?</p>
        <div class="confirm-actions">
            <button id="btn-cancel-team" class="btn-cancel">Cancelar</button>
            <button id="btn-confirm-team" class="btn-confirm" style="background-color: #dc3545;">Sim, excluir</button>
        </div>
    `;

    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    requestAnimationFrame(() => {
        overlay.classList.add('visible');
        modal.classList.add('visible');
    });

    document.getElementById('btn-cancel-team').onclick = () => {
        closeModal(overlay);
    };

    document.getElementById('btn-confirm-team').onclick = () => {
        form.submit();
        closeModal(overlay);
    };
}

function closeModal(overlay) {
    overlay.classList.remove('visible');
    setTimeout(() => {
        overlay.remove();
    }, 300);
}