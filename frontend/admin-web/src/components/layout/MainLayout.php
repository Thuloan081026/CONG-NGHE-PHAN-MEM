<?php


if (!isset($pageContent)) {
    die('Page content not defined');
}
?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>SMD Admin System</title>
    <link rel="stylesheet" href="../styles/admin.css">
</head>
<body>

<?php include __DIR__ . '/Header.php'; ?>

<div class="app-container">
    <?php include __DIR__ . '/Sidebar.php'; ?>

    <main class="app-content">
        <?php include $pageContent; ?>
    </main>
</div>

<?php include __DIR__ . '/Footer.php'; ?>

</body>
</html>


