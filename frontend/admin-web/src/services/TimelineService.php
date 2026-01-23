<?php
namespace Services;

class TimelineService
{
    private static array $timelines = [];

    public static function getAll(): array
    {
        return self::$timelines;
    }

    public static function create(array $data): void
    {
        self::$timelines[] = [
            'id' => uniqid(),
            'semester' => $data['semester'],
            'academic_year' => $data['academic_year'],
            'start_date' => $data['start_date'],
            'end_date' => $data['end_date'],
            'status' => 'ACTIVE'
        ];
    }

    public static function delete(string $id): void
    {
        self::$timelines = array_filter(
            self::$timelines,
            fn($t) => $t['id'] !== $id
        );
    }
}
