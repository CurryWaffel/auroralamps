<?php
  if(isset($_GET['function'])){
      $argumentstring = "";

      foreach ($_GET['args'] as $arg) {
        $argumentstring .= $arg . "\n";
      }
      file_put_contents("befehl.txt", "01\n".$_GET['function']."\n".$argumentstring);
  }
?>
