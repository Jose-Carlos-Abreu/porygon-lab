document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search");

    if (!searchInput) return;

    searchInput.addEventListener("input", (event) => {
        const valorDigitado = event.target.value;
        console.log("Digitando:", valorDigitado);
    });
});