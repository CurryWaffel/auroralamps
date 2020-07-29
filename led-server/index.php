<?php
	if(isset($_GET['function'])){
		file_put_contents("befehl.txt", $_GET['function']);
	}
?>
<html>
	<body>
		<form method="get">
			<input type="hidden" name="function" value="01" />
			<button type="submit">colorWipe</button>
		</form>
		<form method="get">
                        <input type="hidden" name="function" value="02" />
                        <button type="submit">theaterChase</button>
                </form>
		<form method="get">
                        <input type="hidden" name="function" value="03" />
                        <button type="submit">rainbow</button>
                </form>
		<form method="get">
                        <input type="hidden" name="function" value="04" />
                        <button type="submit">rainbowCycle</button>
                </form>
		<form method="get">
                        <input type="hidden" name="function" value="05" />
                        <button type="submit">theaterChaseRainbow</button>
                </form>
		<form method="get">
                        <input type="hidden" name="function" value="00" />
                        <button type="submit">Aus</button>
                </form>
		<a href="https://staticfloat.de/" target="_blank">Staticfloat.de</a>
	</body>
</html>

