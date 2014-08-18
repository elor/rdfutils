#!/bin/bash
# 
#PBS -l nodes=1:ppn=2
#PBS -m a
#PBS -j oe

# set up PBS environment (directory and number of cores)
[ -n "$PBS_O_WORKDIR" ] && cd "$PBS_O_WORKDIR"
[ -s "$PBS_NODEFILE" ] && ncpu=`cat $PBS_NODEFILE | wc -l` || ncpu=2

# remove previous rdf directories
find * -type d -name '*rdf' -exec rm -rf {} +

[ -d dumps ] && dumpdir=dumps
[ -d out ] && dumpdir=out
[ -z "$dumpdir" ] && dumpdir=dumps

echo "processing ./$dumpdir/ using $ncpu cores"

process(){
		local dumpfile="$1"
    [ -z "$dumpfile" ] && exit 1
		local rdfdir="`basename "$dumpfile" .xyz`rdf"

		echo "processing $dumpfile"

	  mkdir "$rdfdir" || exit 1
	  cd "$rdfdir" || exit 1
	  xyz2rdf.sh "../$dumpfile"  || exit 1
	  rdfplot.py *.rdf || exit 1
}

for dumpfile in $dumpdir/*.xyz; do
	  process "$dumpfile" &

	  # wait for ALL children, not ANY of them (as `wait` would)
	  while (( `jobs -p | wc -l` >= $ncpu )); do sleep 1; done
done

wait

