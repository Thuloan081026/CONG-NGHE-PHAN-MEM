<?php
session_start();

require_once __DIR__ . "/../controllers/SyllabusController.php";
require_once __DIR__ . "/../middlewares/LecturerMiddleware.php";

LecturerMiddleware::handle();

if (!isset($_GET['id'])) {
    header("Location: ../../../public/index.php?page=my-syllabus");
    exit;
}

$syllabusId = $_GET['id'];

// Gửi syllabus lên quy trình review
$result = SyllabusController::submit($syllabusId);

if ($result) {
    header("Location: ../../../public/index.php?page=my-syllabus&submitted=1");
} else {
    header("Location: ../../../public/index.php?page=my-syllabus&error=1");
}
exit;
