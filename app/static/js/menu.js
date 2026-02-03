document.addEventListener("DOMContentLoaded", () => {
    const botaoMenu  = document.querySelector(".menu-toggle"); // Botão que para abrir e fechar o menu para mobile
    const menuMobile  = document.getElementById("mobile-menu");

    // Se não existir nada disso na página, não executa o script
    if (!botaoMenu || !menuMobile) {
        return;
    }
    
    // Abre ou fecha o menu mobile adicionando ou removendo a classe "active".
    function alternarMenu() {
        menuMobile.classList.toggle("active");
    }

    // Fecha o menu mobile removendo a classe "active".
    function fecharMenu() {
        menuMobile.classList.remove("active");
    }

    // Quando clicar no botão ".menu-toggle" abre ou fecha o menu
    botaoMenu.addEventListener("click", (event) => {
        event.stopPropagation();
        alternarMenu();
    });

    // Isso é pra não fechar o menu
    menuMobile.addEventListener("click", (event) => {
        event.stopPropagation();
    });

    // Quando clicar fora do menu fecha o menu
    document.addEventListener("click", () => {
        fecharMenu();
    });
});
