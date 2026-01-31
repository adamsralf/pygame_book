reset
set terminal wxt
set key left
set xlabel "Frames per Second"
set ylabel "Deviation from the Expected Height of 315 px"
#set format x "%g "
set terminal pdfcairo color solid

set title "Position Error (Median)"
set output "error_invers.pdf"
set xrange [10:600]
#set yrange [0.0:0.04]
plot "result_05f.txt" using 1:(315 - $13) with lines ls 1 lw 2 linecolor "sea-green" title "deltatime = 1/fps",\
     "result_05g.txt" using 1:(315 - $13) with lines ls 1 lw 2 linecolor "red" title "deltatime = clock.tick()"

#pause mouse

set output "error_float.pdf"
set title "Position Error (Median) with Int and Float"
plot "result_05g.txt" using 1:(315 - $13) with lines ls 1 lw 2 linecolor "sea-green" title "Version 1: rect.top",\
     "result_05h.txt" using 1:(315 - $13) with lines ls 1 lw 2 linecolor "red" title "Version 2: FRect"

#pause mouse

set output "error_function.pdf"
set xrange [10:600]
set title "Position Error (Median) with Different Time Functions"
plot "result_05h.txt" using 1:(315 - $13) with lines ls 1 lw 2 linecolor "sea-green" title "clock.tick()",\
     "result_05i.txt" using 1:(315 - $13) with lines ls 1 lw 2 linecolor "red" title "time.time()"


set output

#pause mouse
