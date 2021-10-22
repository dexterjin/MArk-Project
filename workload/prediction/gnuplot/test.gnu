# Set the output to a png file
set terminal png size 500,500
# The file we'll write to
set output 'tweet_load_jan_20m_50min_10min_5min.eps'
# The graphic title
set title 'tweet_load'
#plot the graphic


set linetype  1 lc rgb "green" lw 2
set linetype  2 lc rgb "purple" lw 2
set linetype  3 lc rgb "red" lw 2
set linetype  4 lc rgb "blue" lw 2

set datafile separator ","
set timefmt "%m-%d-%H-%M"
set xdata time
set xrange ["01-01-10-50":"01-01-11-10"]
plot "../tweet_load.csv" skip 1 using 1:2 with line ls 1 notitle, "../tweet_load_predict_50min.csv" skip 1 using 1:2 with line ls 2 notitle, "../tweet_load_predict_10min.csv" skip 1 using 1:2 with line ls 3 notitle, "../tweet_load_predict_5min.csv" skip 1 using 1:2 with line ls 4 notitle
