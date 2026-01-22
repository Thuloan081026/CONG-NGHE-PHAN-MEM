<?php $users = UserService::all(); ?>
<table>
<tr><th>Name</th><th>Email</th><th>Role</th></tr>
<?php foreach ($users as $u): ?>
<tr>
    <td><?= $u['name'] ?></td>
    <td><?= $u['email'] ?></td>
    <td><?= $u['role'] ?></td>
</tr>
<?php endforeach; ?>
</table>
