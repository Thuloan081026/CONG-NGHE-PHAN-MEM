<?php
session_start();
require_once "../../services/AdminAuthService.php";

AdminAuthService::logout();
header("Location: ../../auth/login.php");
