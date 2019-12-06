# bowser_slurm_tutorial

`bowser` has 20 CPU nodes and 3 GPU nodes at the moment. To schedule jobs we use a job scheduler [slurm](https://slurm.schedmd.com/documentation.html).

1. To submit a job:

       sbatch -N<number of nodes you require> -n<number of tasks> --wrap="<your command>"
      
   eg:
   
       sbatch -N1 -n1 --wrap="python hello_world.py -h"
      
      This will give you a job ID.
      
2. To check queue containing all the jobs:

       squeue
      
3. To query all the jobs by a user:

       squeue -u <username>
      
4. To cancel a job:

       scancel <job_id>
      
    eg:
    
       scancel 7331112


5. To check available resources:

       sinfo
      
6. To submit a GPU job:

       sbatch -N <number of nodes you require> -n <number of tasks> --partition=gpu --gres=gpu:<No. of GPUs required> --wrap="<your command>"
      
   eg:
   
       sbatch -N1 -n1 --partition=gpu --gres=gpu:1 --wrap="nvidia-smi"


Bonus: You can run jupyter-notebooks as well. Replace `PPPP` in the following command with a 4 digit number of your choice:
  
      sbatch -N1 -n1 --wrap="jupyter notebook --no-browser --port=PPPP"
      
  Use `squeue` to check which node your job was scheduled to, say it was `node01`. The slurm-<job_id>.out file will have the output and the link which can then use to login. To forward the port to your local system:
  
      ssh -L PPPP:localhost:PPPP <username>@bowser.phys.wvu.edu ssh -L PPPP:localhost:PPPP <username>@node01
      
   eg:
    
      ssh -L 8080:localhost:8080 dagarwal@bowser.phys.wvu.edu ssh -L 8080:localhost:8080 dagarwal@gpu01
