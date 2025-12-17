<?php
require_once __DIR__ . "/../../hooks/useSyllabus.php";
$syllabusList = useMySyllabus();
?>

<table border="1">
    <tr>
        <th>Mã</th>
        <th>Tên</th>
        <th>Trạng thái</th>
    </tr>

    <?php foreach ($syllabusList as $s): ?>
    <tr>
        <td><?= $s->code ?></td>
        <td><?= $s->name ?></td>
        <td><?= $s->status ?></td>
    </tr>
    <?php endforeach; ?>
</table>
