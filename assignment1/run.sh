for i in `seq 1000 100 2000`;
do
    echo Running $i
    time python3 $1 $i
done
