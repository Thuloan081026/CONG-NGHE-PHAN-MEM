<?php

class SyllabusService
{
    private static function startSession()
    {
        if (session_status() === PHP_SESSION_NONE) {
            session_start();
        }

        if (!isset($_SESSION['syllabuses'])) {
            $_SESSION['syllabuses'] = [];
        }
    }

    // =========================
    // CREATE
    // =========================
    public static function create($data)
    {
        self::startSession();

        $syllabus = [
            'id' => uniqid('syllabus_'),
            'title' => $data['title'] ?? '',
            'description' => $data['description'] ?? '',
            'created_by' => $data['created_by'] ?? 'lecturer',
            'status' => 'draft',
            'created_at' => date('Y-m-d H:i:s')
        ];

        $_SESSION['syllabuses'][] = $syllabus;

        return $syllabus;
    }

    // =========================
    // READ ALL
    // =========================
    public static function all()
    {
        self::startSession();
        return $_SESSION['syllabuses'];
    }

    // =========================
    // READ BY ID
    // =========================
    public static function find($id)
    {
        self::startSession();

        foreach ($_SESSION['syllabuses'] as $syllabus) {
            if ($syllabus['id'] === $id) {
                return $syllabus;
            }
        }
        return null;
    }

    // =========================
    // UPDATE
    // =========================
    public static function update($id, $data)
    {
        self::startSession();

        foreach ($_SESSION['syllabuses'] as $index => $syllabus) {
            if ($syllabus['id'] === $id) {
                $_SESSION['syllabuses'][$index]['title'] =
                    $data['title'] ?? $syllabus['title'];

                $_SESSION['syllabuses'][$index]['description'] =
                    $data['description'] ?? $syllabus['description'];

                $_SESSION['syllabuses'][$index]['status'] =
                    $data['status'] ?? $syllabus['status'];

                return $_SESSION['syllabuses'][$index];
            }
        }
        return false;
    }

    // =========================
    // DELETE
    // =========================
    public static function delete($id)
    {
        self::startSession();

        foreach ($_SESSION['syllabuses'] as $index => $syllabus) {
            if ($syllabus['id'] === $id) {
                array_splice($_SESSION['syllabuses'], $index, 1);
                return true;
            }
        }
        return false;
    }
}
