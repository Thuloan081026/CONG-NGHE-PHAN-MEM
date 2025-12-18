<?php
// context/AuthContext.php
session_start();

class AuthContext {

    public static function login($user) {
        $_SESSION['user'] = $user;
    }

    public static function logout() {
        unset($_SESSION['user']);
    }

    public static function user() {
        return $_SESSION['user'] ?? null;
    }

    public static function isLoggedIn() {
        return isset($_SESSION['user']);
    }
}
