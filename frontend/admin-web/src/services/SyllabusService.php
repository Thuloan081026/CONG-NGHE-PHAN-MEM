<?php
// services/SyllabusService.php

class SyllabusService {

    public static function getAll() {
        return [
            [
                "code" => "SE001",
                "name" => "Software Engineering",
                "year" => "2024"
            ],
            [
                "code" => "SE002",
                "name" => "Database Systems",
                "year" => "2024"
            ]
        ];
    }

    public static function compare($oldYear, $newYear) {
        return "So sánh syllabus $oldYear và $newYear (demo)";
    }
}
