<?php

class AdminContext {
    public static function user() {
        return $_SESSION['admin'] ?? null;
    }
}
