<?php
require_once "../context/FlashMessage.php";

function useFlash() {
    return FlashMessage::get();
}
