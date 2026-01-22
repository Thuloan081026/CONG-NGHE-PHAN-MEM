<?php

class Syllabus {
    public string $title;
    public string $lecturer;
    public string $status;

    public function __construct($title, $lecturer, $status = 'draft') {
        $this->title = $title;
        $this->lecturer = $lecturer;
        $this->status = $status;
    }
}
