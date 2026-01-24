<?php
session_start();
require_once "../../services/AdminAuthService.php";

$email = $_POST['email'] ?? '';
$password = $_POST['password'] ?? '';

if (AdminAuthService::login($email, $password)) {
    header("Location: ../../../public/index.php");
} else {
    echo "Login failed";
}
