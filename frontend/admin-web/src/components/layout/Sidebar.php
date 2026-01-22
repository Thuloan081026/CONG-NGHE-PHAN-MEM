<?php

$currentPage = $_GET['page'] ?? 'dashboard';
?>

<aside class="app-sidebar">
    <ul>
        <li class="<?= $currentPage === 'dashboard' ? 'active' : '' ?>">
            <a href="index.php?page=dashboard">Dashboard</a>
        </li>

        <li class="<?= $currentPage === 'manage-users' ? 'active' : '' ?>">
            <a href="index.php?page=manage-users">Manage Users</a>
        </li>

        <li class="<?= $currentPage === 'manage-timeline' ? 'active' : '' ?>">
            <a href="index.php?page=manage-timeline">Manage Timeline</a>
        </li>

        <li class="<?= $currentPage === 'publish-syllabus' ? 'active' : '' ?>">
            <a href="index.php?page=publish-syllabus">Publish Syllabus</a>
        </li>
    </ul>
</aside>


