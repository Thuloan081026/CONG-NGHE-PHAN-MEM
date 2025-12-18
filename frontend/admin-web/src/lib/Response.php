<?php

class Response {
    public static function redirect($url) {
        header("Location: $url");
        exit;
    }
}
