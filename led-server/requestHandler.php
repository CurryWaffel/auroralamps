<?php
  if(isset($_GET['function'][0])){
    $funcstring = "01\n";
    $i = 0;
    foreach ($_GET['function'] as $func) {
      $argumentstring = "---\n".$func."\n";

      foreach ($_GET['args'][$i] as $arg) {
        $argumentstring .= $arg . "\n";
      }

      $funcstring .= $argumentstring;
      $i++;
    }

    file_put_contents("befehl.txt", $funcstring);
  } else if (isset($_POST['function'][0])) {

    $funcstring = "01\n";
    foreach ($_POST['function'] as $func) {
      $parts = explode(";", $func);
      $funcstring .= "---\n".$parts[0]."\n";
      for ($i = 1; $i < sizeof($parts); $i++) {
        $funcstring .= $parts[$i] . "\n";
      }
    }

    file_put_contents("befehl.txt", $funcstring);
  }

  if (isset($_POST['brightness'][0])) {
    $funcstring = "01\n";
    foreach ($_POST['brightness'] as $func) {
      $parts = explode(";", $func);
      $funcstring .= "---\n".$parts[0]."\n";
      for ($i = 1; $i < sizeof($parts); $i++) {
        $funcstring .= $parts[$i] . "\n";
      }
    }

    file_put_contents("brightness.txt", $funcstring);
  }
?>
