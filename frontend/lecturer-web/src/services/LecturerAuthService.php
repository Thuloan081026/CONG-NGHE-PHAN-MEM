<?php

class LecturerAuthService
{
    public static function login($email, $password)
    {
        if ($email === 'lecturer@fpt.edu.vn' && $password === '123456') {
            $_SESSION['lecturer'] = [
                'email' => $email,
                'role' => 'LECTURER'
            ];
            return true;
        }
        return false;
    }

    public static function check()
    {
        return isset($_SESSION['lecturer']);
    }
}
