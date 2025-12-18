<?php

class FlashMessage {
    public static function set($msg) {
        $_SESSION['flash'] = $msg;
    }

    public static function get() {
        if (!isset($_SESSION['flash'])) return null;
        $msg = $_SESSION['flash'];
        unset($_SESSION['flash']);
        return $msg;
    }
}
