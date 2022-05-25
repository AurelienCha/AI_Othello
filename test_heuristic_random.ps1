$Variable = 8
$depth  = "1+", "2+", "3+", "4+", "5+", "6+", "7+"
$prun = "1p", "2p", "3p", "4p", "5p", "6p", "7p"
$min = "1min", "2min", "3min", "4min", "5min", "6min", "7min"
$max = "1max", "2max", "3max", "4max", "5max", "6max", "7max"
$heur = "1h", "2h", "3h", "4h", "5h", "6h", "7h"
$i = 1
Do{
    $j = 0
    Do{
        $j++
        python3 main.py $heur[$i-1] R
        Write-Host "i = $($heur[$i-1])"
    }Until($j -eq 10)
    $i++

}Until($i -eq $Variable)