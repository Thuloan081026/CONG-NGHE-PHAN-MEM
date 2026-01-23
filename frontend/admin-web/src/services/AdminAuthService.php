<?php
namespace Services;

class AdminAuthService
{
    public static function login(string $email, string $password): bool
    {
        // Demo account
        if ($email === 'admin@smd.edu.vn' && $password === '123456') {
            $_SESSION['admin'] = [
                'email' => $email,
                'role' => 'admin'
            ];
            return true;
        }
        return false;
    }

    public static function check(): bool
    {
        return isset($_SESSION['admin']);
    }

    public static function logout(): void
    {
        unset($_SESSION['admin']);
    }
}

