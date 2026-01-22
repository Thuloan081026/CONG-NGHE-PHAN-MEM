<?php
namespace Services;

class UserService
{
    // Fake data (demo)
    private static array $users = [
        [
            'id' => 1,
            'name' => 'Admin',
            'email' => 'admin@smd.edu.vn',
            'role' => 'admin'
        ],
        [
            'id' => 2,
            'name' => 'Lecturer A',
            'email' => 'lecturer@smd.edu.vn',
            'role' => 'lecturer'
        ]
    ];

    // Lấy toàn bộ user
    public static function getAll(): array
    {
        return self::$users;
    }

    // Tạo user mới
    public static function create(array $data): void
    {
        $data['id'] = count(self::$users) + 1;
        self::$users[] = $data;
    }

    // Tìm user theo id
    public static function findById(int $id): ?array
    {
        foreach (self::$users as $user) {
            if ($user['id'] === $id) {
                return $user;
            }
        }
        return null;
    }
}
