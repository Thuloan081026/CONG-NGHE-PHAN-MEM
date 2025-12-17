<?php
// services/UserService.php
require_once __DIR__ . "/../types/User.php";

class UserService {

    public static function getUsers() {
        return [
            new User(1, "Nguyễn Văn A", "admin"),
            new User(2, "Trần Thị B", "lecturer"),
            new User(3, "Lê Văn C", "student")
        ];
    }

    public static function createUser($name, $role) {
        // Frontend demo – chưa có DB
        return new User(rand(10, 100), $name, $role);
    }
}
