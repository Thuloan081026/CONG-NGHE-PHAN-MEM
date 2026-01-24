<?php
require_once "../context/AdminContext.php";

function useAuth() {
    return AdminContext::user();
}
