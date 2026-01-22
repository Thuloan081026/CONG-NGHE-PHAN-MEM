<?php
namespace Services;

class SyllabusService
{
    private static array $syllabi = [
        [
            'id' => 1,
            'course_code' => 'SWE201',
            'course_name' => 'Software Engineering',
            'status' => 'Draft',
            'lecturer' => 'Lecturer A'
        ]
    ];

    // Lecturer: xem syllabus của mình
    public static function getByLecturer(string $lecturer): array
    {
        return array_filter(self::$syllabi, function ($s) use ($lecturer) {
            return $s['lecturer'] === $lecturer;
        });
    }

    // Admin: xem tất cả syllabus
    public static function getAll(): array
    {
        return self::$syllabi;
    }

    // Tạo syllabus mới
    public static function create(array $data): void
    {
        $data['id'] = count(self::$syllabi) + 1;
        $data['status'] = 'Draft';
        self::$syllabi[] = $data;
    }

    // Publish syllabus
    public static function publish(int $id): void
    {
        foreach (self::$syllabi as &$s) {
            if ($s['id'] === $id) {
                $s['status'] = 'Published';
            }
        }
    }
}


