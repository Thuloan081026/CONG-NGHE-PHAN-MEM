<?php
namespace Services;

class WorkflowService
{
    private static array $workflow = [
        [
            'syllabus_id' => 1,
            'step' => 'Review',
            'status' => 'Pending'
        ]
    ];

    // Lấy trạng thái workflow
    public static function getStatus(int $syllabusId): ?array
    {
        foreach (self::$workflow as $w) {
            if ($w['syllabus_id'] === $syllabusId) {
                return $w;
            }
        }
        return null;
    }

    // Cập nhật trạng thái workflow
    public static function updateStatus(int $syllabusId, string $step, string $status): void
    {
        self::$workflow[] = [
            'syllabus_id' => $syllabusId,
            'step' => $step,
            'status' => $status
        ];
    }
}

