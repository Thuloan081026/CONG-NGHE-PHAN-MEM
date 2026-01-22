<?php
session_start();

require_once "../src/services/LecturerAuthService.php";

// Chưa đăng nhập → về login
if (!LecturerAuthService::check()) {
    header("Location: ../src/auth/login.php");
    exit;
}

// Router đơn giản
$page = $_GET['page'] ?? 'dashboard';

switch ($page) {
    case 'my-syllabus':
        $pageContent = "../src/pages/MySyllabus.php";
        break;

    case 'review':
        $pageContent = "../src/pages/ReviewSyllabus.php";
        break;

    default:
        $pageContent = "../src/pages/Dashboard.php";
        break;
}

// Load layout
include "../src/components/layout/MainLayout.php";

