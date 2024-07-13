#!/bin/bash
#SBATCH -J hpcc-snellius
#SBATCH --nodes=1                   # number of nodes needed
#SBATCH --exclusive
#SBATCH -p rome                     # ensure rome compute node
#SBATCH -t 5:00:00
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=c.d.kooistra@student.vu.nl

#Loading modules
module load 2022
module load foss/2022a
module load HPCC/1.5.0-foss-2022a

timestamp=$(date +"%y%m%d_%H%M%S")
output_dir="$TMPDIR"/output_dir_$timestamp

mkdir -p $output_dir

cp _hpccinf.txt "$output_dir/hpccinf.txt"

cd $output_dir

mpirun -np 16 hpcc

cp -r $output_dir $HOME

rm -rf $output_dir