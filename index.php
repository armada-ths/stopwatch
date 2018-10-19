<?php
include('config.php')

function zeropad($input)
{
	return (strlen($input) === 1 ? '0' : '') . $input;
}

function niceDuration($input)
{
	$input = round($input);
	
	$minutes = floor($input / 60);
	
	$seconds = $input % 60;
	
	if ($minutes == 0) { return zeropad(0) . ':' . zeropad($seconds); }
	else { return zeropad($minutes) . ':' . zeropad($seconds); }
}

$mysqli = new mysqli($DB_HOST, $DB_USERNAME, $DB_PASSWORD);
$mysqli->select_db($DB_DATABASE) or die($mysqli->error);
$mysqli->set_charset('utf8') or die($mysqli->error);

if (isset($_POST['type']))
{
	if ($_POST['type'] === 'latest')
	{
		$sql = $mysqli->query("SELECT `teams`.`name`, `times`.`duration` FROM `times`, `teams`, `tags` WHERE `times`.`tag_id` = `tags`.`id` AND `tags`.`team_id` = `teams`.`id` ORDER BY `times`.`id` DESC") or die($mysqli->error);
		
		echo '<h2>LATEST</h2>';
		
		echo '<table>';
		
		if ($sql->num_rows === 0)
		{
			echo '<tr><td colspan="2" style="text-align: center;">There are no results to display.</td></tr>';
		}
		
		else
		{
			$i = 1;
			
			while ($data = $sql->fetch_assoc())
			{
				echo '<tr>';
				echo '<td></td>';
				echo '<td style="width: 60%; padding-top: 20px;">' . $data['name'] . '</td>';
				echo '<td style="padding-top: 20px;">' . niceDuration($data['duration']) . '</td>';
				echo '</tr>';
				
				$i++;
			}
		}
		
		echo '</table>';
	}
	
	else if ($_POST['type'] === 'highscore')
	{
		$sql = $mysqli->query("SELECT `teams`.`name`, `times`.`duration` FROM `times`, `teams`, `tags` WHERE `times`.`tag_id` = `tags`.`id` AND `tags`.`team_id` = `teams`.`id` ORDER BY `times`.`duration` ASC") or die($mysqli->error);
		
		echo '<h2>HIGH SCORE</h2>';
		
		echo '<table>';
		
		if ($sql->num_rows === 0)
		{
			echo '<tr><td colspan="3" style="text-align: center;">There are no results to display.</td></tr>';
		}
		
		else
		{
			$i = 1;
			
			while ($data = $sql->fetch_assoc())
			{
				echo '<tr>';
				echo '<td style="width: 20%;"><span>' . $i . '</span></td>';
				echo '<td style="width: 60%; padding-top: 20px;">' . $data['name'] . '</td>';
				echo '<td style="padding-top: 20px;">' . niceDuration($data['duration']) . '</td>';
				echo '</tr>';
				
				$i++;
			}
		}
		
		echo '</table>';
	}
	
	
	exit;
}

?>
<!doctype html>

<html lang="en">
	<head>
		<title>Stopwatch</title>
		<style type="text/css">
			html, body
			{
				<?php if (!isset($_GET['p'])) { ?>
				overflow: hidden;
				font-size: 60pt;
				<?php } ?>
				color: #fefefe;
				font-family: 'Ubuntu';
				background-color: #2c2c2c;
			}
			
			#background
			{
				background-image: url('/assets/running.png');
				background-repeat: no-repeat;
				background-position: center center;
				background-size: cover;
				position: fixed;
				top: 0;
				right: 0;
				bottom: 0;
				left: 0;
				opacity: 0.1;
				filter: blur(30px);
			}
			
			#highscore
			{
				top: 0;
				left: 50px;
				bottom: 0;
				position: fixed;
				width: calc(50% - 50px);
				padding-right: 5%;
				box-sizing: border-box;
			}
			
			#latest
			{
				top: 0;
				right: 50px;
				bottom: 0;
				position: fixed;
				width: calc(50% - 50px);
				padding-left: 5%;
				box-sizing: border-box;
				border-left: 5px solid rgba(100, 100, 100, 0.4);
			}
			
			h2
			{
				text-align: center;
				margin: 0;
				padding: 0;
			}
			
			table
			{
				width: 100%;
			}
			
			table tr th
			{
				text-align: left;
			}
			
			table tr th:last-of-type, table tr td:last-of-type
			{
				text-align: right;
			}
			
			table tr td
			{
				font-size: 50pt;
				vertical-align: top;
			}
			
			table tr td:first-of-type
			{
				text-align: center;
				color: #cccccc;
				padding: 10px;
			}
			
			table tr td:first-of-type span
			{
				display: block;
				padding: 15px;
				background: rgba(100, 100, 100, 0.4);
				margin-right: 20px;
			}
		</style>
		<script src="/assets/jquery-3.3.1.min.js"></script>
		<script>
			$(function()
			{
				f('highscore');
				f('latest');
				
				setInterval(f, 1000, 'highscore');
				setInterval(f, 1000, 'latest');
			});
			
			
			var f = function(type)
			{
				$.post('/', { type: type }, function(data)
				{
					$('#' + type).html(data);
				});
			};
		</script>
	</head>
	
	<body>
		<div id="background"></div>
		
		<div id="highscore"></div>
		<div id="latest"></div>
	</body>
</html>
