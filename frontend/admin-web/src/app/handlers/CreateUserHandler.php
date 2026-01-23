<?php
session_start();

require_once "../../services/AdminAuthService.php";
require_once "../../services/UserService.php";

// Chỉ Admin mới được tạo user
if (!AdminAuthService::check()) {
    header("Location: ../../auth/login.php");
    exit;
}

$name  = trim($_POST['name'] ?? '');
$email = trim($_POST['email'] ?? '');
$role  = trim($_POST['role'] ?? '');

if ($name === '' || $email === '' || $role === '') {
    echo "All fields are required";
    exit;
}

// Demo: gọi service (sau này thay bằng insert DB)
UserService::create([
    'name'  => $name,
    'email' => $email,
    'role'  => $role
]);

// Quay lại trang quản lý user
header("Location: ../../../public/index.php?page=users");
exit;
