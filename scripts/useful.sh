# executes gphocs safely
nohup ./scripts/run_simulation.sh experiments/simM2.00/full/ &> ./experiments/simM2.00/full/nohup.out& 
nohup G-PhoCS-1-2-3 folder/control-file.ctl &> folder/nohup.out& 

#recursively deletes all files named '*.out' in current subdirectory
find . -name '*.out' -delete 

# kill all the gphocs
pkill -f G-PhoCS-1-2-3

# kill matching grep 'my_pattern'
for KILLPID in `ps ax | grep '0_1\|0_2\|0_4' | awk ' { print $1;}'`; do 
  kill -9 $KILLPID;
done