<?php
session_start();

// Nếu đã đăng nhập rồi thì không cho vào lại trang login
if (isset($_SESSION['lecturer'])) {
    header("Location: ../../public/index.php");
    exit;
}
?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Lecturer Login - SMD</title>
    <link rel="stylesheet" href="../styles/lecturer.css">
</head>
<body>

<h2>Lecturer Login</h2>

<?php if (isset($_GET['error'])): ?>
    <p style="color:red;">Email hoặc mật khẩu không đúng</p>
<?php endif; ?>

<form method="POST" action="../app/handlers/LoginHandler.php">
    <label>Email</label><br>
    <input type="email" name="email" required><br><br>

    <label>Password</label><br>
    <input type="password" name="password" required><br><br>

    <button type="submit">Login</button>
</form>

</body>
</html>

