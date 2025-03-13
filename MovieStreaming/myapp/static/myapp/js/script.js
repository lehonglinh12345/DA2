
document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector(".sidebar");
    const overlay = document.querySelector(".sidebar-overlay");
    const sidebarToggle = document.querySelector(".sidebar-toggle");
    const closeBtn = document.querySelector(".close-btn");

    function closeSidebar() {
        sidebar.classList.remove("active");
        overlay.classList.remove("active");
    }

    // Khi bấm nút mở sidebar
    sidebarToggle.addEventListener("click", function () {
        sidebar.classList.add("active");
        overlay.classList.add("active");
    });

    // Khi bấm nút đóng sidebar
    closeBtn.addEventListener("click", closeSidebar);

    // Khi bấm vào overlay (bên ngoài sidebar) thì đóng sidebar
    overlay.addEventListener("click", closeSidebar);
});
