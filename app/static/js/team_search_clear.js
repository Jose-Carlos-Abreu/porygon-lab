document.addEventListener("DOMContentLoaded", () => {
    const btnClear = document.getElementById("btn-clear-team-search");
    const searchInput = document.getElementById("search");
    const typeSelect = document.getElementById("filter-type");

    if (!btnClear || !searchInput || !typeSelect) return;

    btnClear.addEventListener("click", () => {
        searchInput.value = "";
        typeSelect.value = "";
        searchInput.dispatchEvent(new Event("input"));
    });
});