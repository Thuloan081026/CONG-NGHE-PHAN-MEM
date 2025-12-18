<?php
session_start();

require_once "../../services/AdminAuthService.php";
require_once "../../services/TimelineService.php";

// Chỉ admin mới được tạo timeline
if (!AdminAuthService::check()) {
    header("Location: ../../auth/login.php");
    exit;
}

$semester = trim($_POST['semester'] ?? '');

if ($semester === '') {
    echo "Semester name is required";
    exit;
}

// Hiện tại demo: chỉ log ra (sau này thay bằng DB insert)
TimelineService::create($semester);

// Quay về trang quản lý timeline
header("Location: ../../../public/index.php?page=timeline");
exit;
