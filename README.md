# bowser_slurm_tutorial

`bowser` has 20 CPU nodes and 5 GPU nodes at the moment. To schedule jobs we use a job scheduler [slurm](https://slurm.schedmd.com/documentation.html).

**NOTE**: We also have a data transfer node `remote.phys.wvu.edu` which can be used for high speed transfers.

- To submit a job, use [bowser-slurm.herokuapp.com](https://bowser-slurm.herokuapp.com) to generate the slurm script.
      
- To check queue containing all the jobs:

       squeue
      
- To query all the jobs by a user:

       squeue -u <username>
      
- To cancel a job:

       scancel <job_id>
      
    eg:
    
       scancel 7331112


- To check available resources:

       sinfo
      
- To run a `jupyter-notebook` on one of the nodes, run [jupyter_bowser_cpu.sh](https://github.com/devanshkv/bowser_slurm_tutorial/blob/master/jupyter_bowser_cpu.sh) (or [jupyter_bowser_gpu.sh](https://github.com/devanshkv/bowser_slurm_tutorial/blob/master/jupyter_bowser_gpu.sh) for a gpu job). This will create `jupyter-notebook-<job_id>.log`. `cat jupyter-notebook-<job_id>.log` file and it will give you the ssh tunnel command for MacOS or linux terminal along with the port and the token.
