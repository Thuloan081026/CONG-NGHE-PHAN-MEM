<?php

require_once __DIR__ . '/../services/SyllabusService.php';

// Xử lý submit form
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = $_POST['title'] ?? '';
    $description = $_POST['description'] ?? '';
    $clos = $_POST['clo'] ?? [];
    $plos = $_POST['plo'] ?? [];
    $weight = $_POST['weight'] ?? '';

    // Lưu syllabus
    SyllabusService::create([
        'title' => $title,
        'description' => $description,
        'created_by' => 'lecturer'
    ]);

    // Lưu CLO – PLO mapping riêng 
    $_SESSION['clo_plo_mapping'] = [];
    for ($i = 0; $i < count($clos); $i++) {
        $_SESSION['clo_plo_mapping'][] = [
            'clo' => $clos[$i],
            'plo' => $plos[$i]
        ];
    }

    header('Location: index.php?page=my-syllabus');
    exit;
}
?>

<h2>Create New Syllabus</h2>

<form method="post">
    <!-- BASIC INFO -->
    <fieldset>
        <legend><strong>Basic Information</strong></legend>

        <label>Subject Name</label><br>
        <input type="text" name="title" required style="width:100%"><br><br>

        <label>Description</label><br>
        <textarea name="description" rows="4" style="width:100%" required></textarea>
    </fieldset>

    <br>

    <!-- CLO - PLO -->
    <fieldset>
        <legend><strong>CLO – PLO Mapping</strong></legend>

        <?php for ($i = 0; $i < 3; $i++): ?>
            <div style="margin-bottom:10px;">
                <input
                    type="text"
                    name="clo[]"
                    placeholder="CLO <?= $i + 1 ?>"
                    style="width:60%;"
                    required
                >

                <select name="plo[]" required>
                    <option value="">-- Select PLO --</option>
                    <option value="PLO1">PLO1</option>
                    <option value="PLO2">PLO2</option>
                    <option value="PLO3">PLO3</option>
                    <option value="PLO4">PLO4</option>
                </select>
            </div>
        <?php endfor; ?>
    </fieldset>

    <br>

    <!-- ASSESSMENT -->
    <fieldset>
        <legend><strong>Assessment Weight</strong></legend>
        <input type="number" name="weight" placeholder="Total weight (%)" min="0" max="100" required>
    </fieldset>

    <br>

    <button type="submit">📘 Create Syllabus</button>
</form>
