<?php
  if(isset($_GET['function'])){
      file_put_contents("befehl.txt", "01\n".$_GET['function']."\n[114,0,171]\n");
  }
?>
