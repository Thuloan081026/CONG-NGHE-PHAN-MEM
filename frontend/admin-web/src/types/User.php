<?php
// types/User.php
// Mô tả cấu trúc dữ liệu User

class User {
    public int $id;
    public string $name;
    public string $email;
    public string $role;

    public function __construct($id, $name, $email, $role) {
        $this->id = $id;
        $this->name = $name;
        $this->email = $email;
        $this->role = $role;
    }
}
