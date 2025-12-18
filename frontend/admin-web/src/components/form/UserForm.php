<form method="post" action="../app/handlers/CreateUserHandler.php">
    <input type="text" name="name" placeholder="Full Name" required>
    <input type="email" name="email" placeholder="Email" required>
    <select name="role">
        <option value="Lecturer">Lecturer</option>
        <option value="Student">Student</option>
    </select>
    <button type="submit">Create User</button>
</form>
