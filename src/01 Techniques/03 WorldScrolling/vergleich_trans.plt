reset
set terminal wxt
set key left
set xlabel "Frames per second"
set ylabel "Tick (Bezier geglättet)"

# robust gegen fremde Session-Einstellungen:
set datafile separator whitespace   # unsere bird.txt ist durch Leerzeichen getrennt
unset logscale                      # falls vorher logscale x aktiv war
set autoscale                       # sicherstellen, dass Autoscale an ist
#set xrange [1:600]                  # explizit: erste Spalte geht von 1..600
#set yrange [1:600]
#set format x "%g "
#set terminal pdfcairo color solid

#set title "Performance mit und ohne Vorbereitung"
#set output "PerformaceTransformation.pdf"
plot "trans.txt" using 1:2 with lines ls 1 lw 2 linecolor "sea-green" smooth bezier  title "Elementtransformation",\
     "trans.txt" using 1:3 with lines ls 1 lw 2 linecolor "red" smooth bezier  title "Welttransformation"

pause mouse

set output


