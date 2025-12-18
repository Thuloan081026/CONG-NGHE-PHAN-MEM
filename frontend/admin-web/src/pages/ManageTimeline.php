<?php
use Services\TimelineService;

require_once "../services/TimelineService.php";

$timelines = TimelineService::getAll();
?>

<h1>Manage Timeline</h1>

<section class="form-section">
    <h2>Create New Semester Timeline</h2>

    <form method="post" action="../app/handlers/CreateTimelineHandler.php">
        <?php include "../components/form/TimelineForm.php"; ?>
        <button type="submit">Create Timeline</button>
    </form>
</section>

<section class="table-section">
    <h2>Timeline List</h2>

    <?php
        $data = $timelines;
        include "../components/table/TimelineTable.php";
    ?>
</section>
