<?php

class User {
    public string $username;
    public string $role;

    public function __construct($username, $role) {
        $this->username = $username;
        $this->role = $role;
    }
}
