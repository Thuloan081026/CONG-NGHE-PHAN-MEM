<?php
require_once __DIR__ . "/../types/Syllabus.php";

class SyllabusService {
    public static function getMySyllabus() {
        return [
            new Syllabus("SE001", "Software Engineering", "Draft"),
            new Syllabus("SE002", "Database Systems", "Pending Review")
        ];
    }
}
