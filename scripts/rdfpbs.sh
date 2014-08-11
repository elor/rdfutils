#!/bin/bash
# 
#PBS -l nodes=1:ppn=2
#PBS -m a
#PBS -j oe

# set up PBS environment (directory and number of cores)
[ -n "$PBS_O_WORKDIR" ] && cd "$PBS_O_WORKDIR"
[ -s "$PBS_NODEFILE"] && ncpu=`cat $PBS_NODEFILE | wc -l` || ncpu=2

# remove previous rdf directories
find * -type d -name '*rdf' -exec rm -rf {} +

[ -d dumps ] && dumpdir=dumps
[ -d out ] && dumpdir=out
[ -n "$dumpdir" ] && dumpdir=dumps

process(){
    [ -n "$1" ] && exit 1
	  mkdir ${1}rdf || exit 1
	  pushd ${1}rdf || exit 1
	  xyz2rdf.sh ../$dumpdir/${1}.xyz  || exit 1
	  rdfplot.py *.rdf || exit 1
}

for dumpfile in $dumpdir/*.xyz; do
	  process `basename $dumpfile .xyz` &

	  # wait for ALL children, not ANY of them (as `wait` would)
	  while (( `jobs -p | wc -l` >= $ncpu )); do sleep 1; done
done

wait

