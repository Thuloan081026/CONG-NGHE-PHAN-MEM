<?php

?>
<header class="app-header">
    <div class="logo">
        <h2>SMD Admin</h2>
    </div>

    <div class="user-info">
        <span>
            Xin chào,
            <strong><?= $_SESSION['admin']['name'] ?? 'Admin' ?></strong>
        </span>
        <a href="../auth/logout.php" class="logout-btn">Logout</a>
    </div>
</header>
