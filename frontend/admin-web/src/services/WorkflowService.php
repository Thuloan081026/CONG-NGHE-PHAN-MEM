<?php
// services/WorkflowService.php

class WorkflowService {

    public static function getStatusList() {
        return [
            "Draft",
            "Pending Review",
            "Pending Approval",
            "Approved",
            "Published"
        ];
    }

    public static function submit($syllabusId) {
        return "Syllabus $syllabusId đã gửi duyệt";
    }
}
