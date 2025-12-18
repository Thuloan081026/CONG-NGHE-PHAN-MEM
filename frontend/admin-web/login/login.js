function validateAdmin() {
    const user = document.getElementById("adminUser").value.trim();
    const pass = document.getElementById("adminPass").value;
    const error = document.getElementById("adminError");

    error.innerText = "";

    if (user !== "admin" || pass !== "123456") {
        error.innerText = "Sai tài khoản hoặc mật khẩu admin";
        return false;
    }

    window.location.href = "/admin/dashboard.html";
    return false;
}
