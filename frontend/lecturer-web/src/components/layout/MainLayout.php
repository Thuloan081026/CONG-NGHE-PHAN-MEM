<?php

?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Lecturer Dashboard - SMD</title>
    <link rel="stylesheet" href="../src/styles/lecturer.css">
</head>
<body>

<?php include __DIR__ . "/Header.php"; ?>

<div class="container">
    <?php include __DIR__ . "/Sidebar.php"; ?>

    <main class="content">
        <?php
        if (isset($pageContent) && file_exists($pageContent)) {
            include $pageContent;
        } else {
            echo "<p>Page not found</p>";
        }
        ?>
    </main>
</div>

</body>
</html>
