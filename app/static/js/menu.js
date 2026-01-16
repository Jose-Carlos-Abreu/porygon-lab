document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector(".menu-toggle");
    const menu = document.getElementById("mobile-menu");

    if (!toggle || !menu) return;

    toggle.addEventListener("click", (e) => {
        e.stopPropagation();
        menu.classList.toggle("active");
    });

    menu.addEventListener("click", (e) => {
        e.stopPropagation();
    });

    document.addEventListener("click", () => {
        menu.classList.remove("active");
    });
});
