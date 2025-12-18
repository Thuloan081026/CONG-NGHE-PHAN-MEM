<?php
require_once __DIR__ . "/../services/SyllabusService.php";

function useMySyllabus() {
    return SyllabusService::getMySyllabus();
}
