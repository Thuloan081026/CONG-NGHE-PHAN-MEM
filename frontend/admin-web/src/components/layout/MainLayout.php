<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Admin Web - SMD</title>

    <!-- CSS chung -->
    <link rel="stylesheet" href="/admin-web/public/styles/main.css">
</head>

<body>

    <!-- HEADER -->
    <?php include __DIR__ . "/Header.php"; ?>

    <div class="layout-container">

        <!-- SIDEBAR -->
        <?php include __DIR__ . "/Sidebar.php"; ?>

        <!-- NỘI DUNG CHÍNH -->
        <div class="main-content">
            <?php
                // Đây là nơi load trang con (Dashboard, User, ...)
                if (isset($pageContent)) {
                    include $pageContent;
                } else {
                    echo "<h3>Không có nội dung</h3>";
                }
            ?>
        </div>

    </div>

    <!-- FOOTER -->
    <?php include __DIR__ . "/Footer.php"; ?>

</body>
</html>