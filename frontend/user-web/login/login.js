function handleLogin() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value;
    const error = document.getElementById("error");

    // Reset lỗi
    error.innerText = "";

    // 1️⃣ Kiểm tra rỗng
    if (email === "" || password === "" || role === "") {
        error.innerText = "Vui lòng nhập đầy đủ thông tin.";
        return false;
    }

    //  Kiểm tra email hợp lệ
    const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    if (!emailRegex.test(email)) {
        error.innerText = "Email không hợp lệ.";
        return false;
    }

    // 3️⃣ Kiểm tra độ dài mật khẩu
    if (password.length < 6) {
        error.innerText = "Mật khẩu phải có ít nhất 6 ký tự.";
        return false;
    }

    // 4️⃣ Điều hướng theo role
    if (role === "student") {
        window.location.href = "/student/dashboard.html";
    } else if (role === "lecture") {
        window.location.href = "/lecture/dashboard.html";
    } else if (role === "reviewer") {
        window.location.href = "/reviewer/dashboard.html";
    }

    return false;
}
