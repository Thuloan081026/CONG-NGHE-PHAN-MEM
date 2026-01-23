<?php

session_start();

// Khởi tạo dữ liệu mẫu nếu chưa có
if (!isset($_SESSION['clo_plo_mapping'])) {
    $_SESSION['clo_plo_mapping'] = [
        [
            'clo' => 'CLO1: Understand basic software engineering concepts',
            'plo' => 'PLO1'
        ],
        [
            'clo' => 'CLO2: Apply UML in system design',
            'plo' => 'PLO2'
        ]
    ];
}

// Xử lý submit form
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $clos = $_POST['clo'];
    $plos = $_POST['plo'];

    $_SESSION['clo_plo_mapping'] = [];

    for ($i = 0; $i < count($clos); $i++) {
        $_SESSION['clo_plo_mapping'][] = [
            'clo' => $clos[$i],
            'plo' => $plos[$i]
        ];
    }

    $success = true;
}

$mappingList = $_SESSION['clo_plo_mapping'];
?>

<h2>CLO – PLO Mapping</h2>

<?php if (!empty($success)): ?>
    <p style="color: green;">✔ Mapping đã được lưu thành công</p>
<?php endif; ?>

<form method="post">
    <table border="1" cellpadding="8" cellspacing="0" width="100%">
        <thead>
            <tr>
                <th>#</th>
                <th>Course Learning Outcome (CLO)</th>
                <th>Program Learning Outcome (PLO)</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($mappingList as $index => $item): ?>
                <tr>
                    <td><?= $index + 1 ?></td>
                    <td>
                        <input
                            type="text"
                            name="clo[]"
                            value="<?= htmlspecialchars($item['clo']) ?>"
                            style="width: 100%;"
                            required
                        >
                    </td>
                    <td>
                        <select name="plo[]" required>
                            <option value="">-- Select PLO --</option>
                            <option value="PLO1" <?= $item['plo'] === 'PLO1' ? 'selected' : '' ?>>PLO1</option>
                            <option value="PLO2" <?= $item['plo'] === 'PLO2' ? 'selected' : '' ?>>PLO2</option>
                            <option value="PLO3" <?= $item['plo'] === 'PLO3' ? 'selected' : '' ?>>PLO3</option>
                            <option value="PLO4" <?= $item['plo'] === 'PLO4' ? 'selected' : '' ?>>PLO4</option>
                        </select>
                    </td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>

    <br>
    <button type="submit">💾 Save Mapping</button>
</form>
