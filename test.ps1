$Variable = 2
$depth  = "1+", "2+", "3+", "4+", "5+", "6+", "7+"
$prun = "1p", "2p", "3p", "4p", "5p", "6p", "7p"
$min = "1min", "2min", "3min", "4min", "5min", "6min", "7min"
$max = "1max", "2max", "3max", "4max", "5max", "6max", "7max"
$i = 0
Do{

    $i++
    py main.py $prun[$i] $i+1
    Write-Host "i = $($prun[$i])"
    Write-Host "i = $($i+1)"

}Until($i -eq $Variable)