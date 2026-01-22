<?php

class Validator {
    public static function required($value) {
        return !empty(trim($value));
    }
}
