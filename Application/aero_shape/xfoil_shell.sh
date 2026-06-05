m=`date|awk '{print $2}'`
d=`date|awk '{print $3}'`
t=`date|awk '{print $4}'`
s=`date|awk '{print $5}'`

#1. ./xfoil_shell.sh  NACA_0012_180.dat 1e6 this_polar_name.txt 5
#2. xfoil<$this_run
#./xfoil_shell.sh NACA_0012_180.dat 1e6 NACA_0012_180.txt 6
rm -f ./outputs/this_polar/*.*
rm -f *.png
this_run=this.run
this_log=aoa$4.log
echo $1 $2 $3 $4>$this_log
echo load $1>$this_run # foil name
echo oper>>$this_run  
echo  visc>>$this_run 
echo $2>>$this_run #Re number 1e6
echo pacc>>$this_run # export polar file
echo ./outputs/this_polar/$3>>$this_run # file name to plot later
echo ./log/$t$d$m$s.dump>>$this_run
echo a $4>>$this_run 
echo HARD>>$this_run
xfoil<$this_run
sleeo 2
./ps2png plot.ps
#now plot is on 1.png to show



