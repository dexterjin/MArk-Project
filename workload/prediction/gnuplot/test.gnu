# Set the output to a png file
set terminal png size 500,500
# The file we'll write to
set output 'tweet_load_12h.eps'
# The graphic title
set title 'tweet_load'
#plot the graphic


set linetype  1 lc rgb "green" lw 2
set linetype  2 lc rgb "purple" lw 2
set linetype  3 lc rgb "red" lw 2

set datafile separator ","
set timefmt "%m-%d-%H-%M"
set xdata time
set xrange ["01-01-11-00":"01-01-17-00"]
plot "../tweet_load.csv" skip 1 using 1:2 with line ls 1 notitle, "../tweet_load_predict.csv" skip 1 using 1:2 with line ls 2 notitle
