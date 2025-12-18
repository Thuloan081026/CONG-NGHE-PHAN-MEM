<?php

class AuthGuard {
    public static function adminOnly() {
        if (!isset($_SESSION['admin'])) {
            header("Location: ../auth/login.php");
            exit;
        }
    }
}
