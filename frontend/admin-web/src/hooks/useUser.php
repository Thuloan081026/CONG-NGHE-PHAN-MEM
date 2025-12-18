<?php
require_once __DIR__ . "/../services/UserService.php";

function useUsers() {
    return UserService::getAllUsers();
}

function useUser($id) {
    return UserService::getUserById($id);
}
