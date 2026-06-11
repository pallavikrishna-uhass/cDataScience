#!/bin/bash
#!/usr/bin/env -S bash -l
#SBATCH --account=lp_mindwell_pilot
#SBATCH --cluster=mindwell
#SBATCH --time=00:05:00

#SBATCH --output=bloom_%j.out
#SBATCH --error=bloom_%j.err

echo "Starting benchmark..."
date

# Activate conda environment
source /apps/leuven/rocky9/skylake/2021a/software/Miniconda3/4.12.0/etc/profile.d/conda.sh
conda activate bloom_filter

# Move to project directory
cd /data/leuven/388/vsc38896

# Run benchmark
python3 benchmarks/benchmark.py --samples 1000
python3 benchmarks/benchmark.py --samples 10000
python3 benchmarks/benchmark.py --samples 100000

echo "Finished"
date