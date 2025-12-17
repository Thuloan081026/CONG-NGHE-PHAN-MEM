<?php
$page = $_GET['page'] ?? 'dashboard';

switch ($page) {
    case 'my-syllabus':
        $pageContent = __DIR__ . "/pages/MySyllabus.php";
        break;
    case 'create-syllabus':
        $pageContent = __DIR__ . "/pages/CreateSyllabus.php";
        break;
    default:
        $pageContent = __DIR__ . "/pages/Dashboard.php";
}

include "../components/layout/MainLayout.php";
