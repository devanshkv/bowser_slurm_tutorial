# bowser_slurm_tutorial

`bowser` has 20 CPU nodes and 3 GPU nodes at the moment. To schedule jobs we use a job scheduler [slurm](https://slurm.schedmd.com/documentation.html).

1. To submit a job:

      `sbatch -N<number of nodes you require> -n<number of tasks> --wrap="<your command>"`
      
   eg:
   
      `sbatch -N1 -n1 --wrap="python hello_world.py -h"`
      
      This will give you a job ID.
      
2. To check queue containing all the jobs:

      `squeue`
      
3. To query all the jobs by a user:

      `squeue -u <username>`
      
4. To cancel a job:

      `scancel <job_id>`
      
    eg:
    
      `scancel 7331112`


5. To check available resources:

      `sinfo`
      
6. To submit a GPU job:

      `sbatch -N <number of nodes you require> -n <number of tasks> --partition=gpu --gres=gpu:<No. of GPUs required> --wrap="<your command>"`
      
   eg:
   
      `sbatch -N1 -n1 --partition=gpu --gres=gpu:1 --wrap="nvidia-smi"`
