<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Lecturer Web</title>
    <link rel="stylesheet" href="/lecturer-web/public/styles/main.css">
</head>
<body>

<?php include __DIR__ . "/Header.php"; ?>

<div class="layout">
    <?php include __DIR__ . "/Sidebar.php"; ?>

    <div class="main-content">
        <?php include $pageContent; ?>
    </div>
</div>

<?php include __DIR__ . "/Footer.php"; ?>

</body>
</html>
