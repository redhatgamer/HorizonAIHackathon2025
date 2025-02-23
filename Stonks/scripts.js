document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.querySelector(".sidebar-content");
    const body = document.body;

    if (sidebar) {
        const observer = new MutationObserver(() => {
            if (sidebar.style.display !== "none") {
                body.classList.add("sidebar-open");
            } else {
                body.classList.remove("sidebar-open");
            }
        });

        observer.observe(sidebar, { attributes: true, attributeFilter: ["style"] });
    }
});