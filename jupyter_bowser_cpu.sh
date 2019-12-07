#!/bin/bash
#SBATCH --partition batch
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 1
#SBATCH --mem-per-cpu 8G
#SBATCH --time 1-0:00:00
#SBATCH --job-name jupyter-notebook
#SBATCH --output jupyter-notebook-%J.log

# get tunneling info
XDG_RUNTIME_DIR=""
port=$(shuf -i8000-9999 -n1)
node=$(hostname -s)
user=$(whoami)
cluster=$(hostname -f | awk -F"." '{print $1}')

# print tunneling instructions jupyter-log
echo -e "
MacOS or linux terminal command to create your ssh tunnel
ssh -L ${port}:localhost:${port} ${user}@bowser.phys.wvu.edu ssh -L ${port}:localhost:${port} ${user}@${cluster}


Use a Browser on your local machine to go to:
localhost:${port}  (prefix w/ https:// if using password)
"

#put your conda env here
# source activate notebook_env
jupyter-notebook --no-browser --port=${port}
