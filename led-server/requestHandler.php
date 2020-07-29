<?php
  if(isset($_GET['function'])){
    file_put_contents("befehl.txt", $_GET['function']);
  }
?>
