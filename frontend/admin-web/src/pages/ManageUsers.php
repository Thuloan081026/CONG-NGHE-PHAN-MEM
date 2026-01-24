<?php
use Services\UserService;

require_once "../services/UserService.php";

$users = UserService::getAll();
?>

<h1>Manage Users</h1>

<section class="form-section">
    <h2>Add New User</h2>

    <form method="post" action="../app/handlers/CreateUserHandler.php">
        <?php include "../components/form/UserForm.php"; ?>
        <button type="submit">Create User</button>
    </form>
</section>

<section class="table-section">
    <h2>User List</h2>
    <?php
        $data = $users;
        include "../components/table/UserTable.php";
    ?>
</section>


