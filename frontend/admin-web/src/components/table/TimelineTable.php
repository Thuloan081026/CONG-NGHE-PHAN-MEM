<?php $list = TimelineService::all(); ?>
<table>
<tr><th>Semester</th></tr>
<?php foreach ($list as $t): ?>
<tr><td><?= $t ?></td></tr>
<?php endforeach; ?>
</table>
