<?php
session_start();
require_once "../src/services/AdminAuthService.php";

if (!AdminAuthService::check()) {
    header("Location: ../src/auth/login.php");
    exit;
}

$page = $_GET['page'] ?? 'dashboard';

switch ($page) {
    case 'users':
        $pageContent = "../src/pages/ManageUsers.php";
        break;
    case 'timeline':
        $pageContent = "../src/pages/ManageTimeline.php";
        break;
    case 'publish':
        $pageContent = "../src/pages/PublishSyllabus.php";
        break;
    default:
        $pageContent = "../src/pages/Dashboard.php";
}

include "../src/components/layout/MainLayout.php";

