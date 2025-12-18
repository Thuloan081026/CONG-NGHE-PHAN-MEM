<?php
// lib/helpers.php

function redirect($url) {
    header("Location: $url");
    exit();
}

function isActive($page, $currentPage) {
    return $page === $currentPage ? 'active' : '';
}
