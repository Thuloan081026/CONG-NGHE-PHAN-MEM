<?php
class Syllabus {
    public $code;
    public $name;
    public $status;

    public function __construct($code, $name, $status) {
        $this->code = $code;
        $this->name = $name;
        $this->status = $status;
    }
}
