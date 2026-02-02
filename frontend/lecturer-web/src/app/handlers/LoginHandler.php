<?php
session_start();

require_once __DIR__ . "/../../services/LecturerAuthService.php";

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header("Location: ../../auth/login.php");
    exit;
}

$email    = $_POST['email'] ?? '';
$password = $_POST['password'] ?? '';

$lecturer = LecturerAuthService::login($email, $password);

if ($lecturer) {
    $_SESSION['lecturer'] = $lecturer;
    header("Location: ../../../public/index.php");
} else {
    header("Location: ../../auth/login.php?error=1");
}
exit;
