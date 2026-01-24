<?php
session_start();

require_once __DIR__ . "/../controllers/SyllabusController.php";
require_once __DIR__ . "/../middlewares/LecturerMiddleware.php";

// Kiểm tra quyền Lecturer
LecturerMiddleware::handle();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header("Location: ../../../public/index.php?page=create-syllabus");
    exit;
}

// Lấy dữ liệu từ form
$data = [
    'subject_code'   => $_POST['subject_code'] ?? '',
    'subject_name'   => $_POST['subject_name'] ?? '',
    'description'    => $_POST['description'] ?? '',
    'clo'            => $_POST['clo'] ?? '',
    'plo'            => $_POST['plo'] ?? '',
    'lecturer_email' => $_SESSION['lecturer']['email']
];

// Gọi controller xử lý nghiệp vụ
$result = SyllabusController::create($data);

if ($result) {
    header("Location: ../../../public/index.php?page=my-syllabus&success=1");
} else {
    header("Location: ../../../public/index.php?page=create-syllabus&error=1");
}
exit;
