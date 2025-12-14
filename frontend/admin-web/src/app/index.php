<?php
$page = $_GET['page'] ?? 'dashboard';

switch ($page) {
    case 'users':
        $pageContent = __DIR__ . "/pages/UserPage.php";
        break;
    case 'syllabus':
        $pageContent = __DIR__ . "/pages/SyllabusPage.php";
        break;
    default:
        $pageContent = __DIR__ . "/pages/Dashboard.php";
}

include "../components/layout/MainLayout.php";
