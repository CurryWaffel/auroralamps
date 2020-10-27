<?php
  if (isset($_POST['cmd'])) {
    file_put_contents("befehl.txt", $_POST['cmd']);
    file_put_contents("change.txt", json_encode(array("change"=>1)));
  }

  if (isset($_POST['setting'])) {
    file_put_contents("setting.txt", $_POST['setting']);
    file_put_contents("setting_change.txt", json_encode(array("change"=>1)));
  }
?>
