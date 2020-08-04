<?php
  if(isset($_GET['function'])){
      file_put_contents("befehl.txt", "01\n".$_GET['function']."\n".$_GET['args'][0]."\n");
  }
?>
