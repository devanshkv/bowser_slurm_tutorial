# Your Heimdall Fetch FRBs

Here are the instructions to run Heimdall + FETCH with your to find FRBs.
Bowser has an account named `fetch` where we have installed everything.

First login and activate `your_fetch` environment using

```
conda activate your_fetch
```

## Heimdall
Assuming you have filterbank files. If you have PSRFITS files, use [`your_heimdall.py`](https://thepetabyteproject.github.io/your/bin/your_heimdall/) instead.

Here is the help from `heimdall`:
```
Usage: heimdall [options]
    -k  key                  use PSRDADA hexidecimal key
    -f  filename             process specified SIGPROC filterbank file
    -vVgG                    increase verbosity level
    -yield_cpu               yield CPU during GPU operations
    -gpu_id ID               run on specified GPU
    -nsamps_gulp num         number of samples to be read at a time [262144]
    -baseline_length num     number of seconds over which to smooth the baseline [2]
    -beam ##                 over-ride beam number
    -output_dir path         create all output files in specified path
    -dm min max              min and max DM
    -dm_tol num              SNR loss tolerance between each DM trial [1.25]
    -coincidencer host:port  connect to the coincidencer on the specified host and port
    -zap_chans start end     zap all channels between start and end channels inclusive
    -max_giant_rate nevents  limit the maximum number of individual detections per minute to nevents
    -dm_pulse_width num      expected intrinsic width of the pulse signal in microseconds
    -dm_nbits num            number of bits per sample in dedispersed time series [32]
    -no_scrunching           don't use an adaptive time scrunching during dedispersion
    -scrunching_tol num      smear tolerance factor for time scrunching [1.15]
    -rfi_tol num             RFI exicision threshold limits [5]
    -rfi_no_narrow           disable narrow band RFI excision
    -rfi_no_broad            disable 0-DM RFI excision
    -boxcar_max num          maximum boxcar width in samples [4096]
    -fswap                   swap channel ordering for negative DM - SIGPROC 2,4 or 8 bit only
    -min_tscrunch_width num  vary between high quality (large value) and high performance (low value)
```

So a sample command for
- a filterbank with the name `name.fil`
- dm between 10 and 10,000 pc/cc
- max pulse width of 512 samples
```
heimdall -f name.fil -dm 10 10000 -boxcar_max 512 
```
To run using slurm
```
sbatch -n1 -N1 --partition=gpu --nodelist=notebook --gres=gpu:1 --wrap="heimdall -f name.fil -dm 10 10000 -boxcar_max 512"
```

If you know bad channels to flag (let's say flag channels between 10 and 30), just add `-zap_chans 10 30` to the above command. This will create `.cand` files.
The columns of the `.cand` files are:
- Detection SNR
- candidate Sample Number (for highest frequency channel)
- Candidate Time (s)
- Boxcar Filter Number (e.g. 3 equates to 2^3 or 8 samples)
- Dispersion Measure Trial Number
- Dispersion Measure (in pc cm^-3)
- Members (the number of individual boxcar/DM trials that were clustered into this event)
- First sample that the candidate spans
- Last sample that the candidate spans

The next step is to run `candcsvmaker.py` to convert these `.cand` files to a format which [`your`](https://github.com/thepetabyteproject/your) can read.
Here is the help:
```
usage: candcsvmaker.py [-h] [-v] [-o FOUT] -f FIN [FIN ...] -c HEIM_CANDS
                       [HEIM_CANDS ...] [-k CHANNEL_MASK_PATH] [-s SNR_TH]
                       [-dl DM_MIN_TH] [-du DM_MAX_TH] [-g CLUSTERSIZE_TH]

Your Heimdall candidate csv maker

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Be verbose (default: False)
  -o FOUT, --fout FOUT  Output file directory for candidate csv file (default:
                        None)
  -f FIN [FIN ...], --fin FIN [FIN ...]
                        Input files, can be *fits or *fil or *sf (default:
                        None)
  -c HEIM_CANDS [HEIM_CANDS ...], --heim_cands HEIM_CANDS [HEIM_CANDS ...]
                        Heimdall cand files (default: None)
  -k CHANNEL_MASK_PATH, --channel_mask_path CHANNEL_MASK_PATH
                        Path of channel flags mask (default: None)
  -s SNR_TH, --snr_th SNR_TH
                        SNR Threshold (default: 6)
  -dl DM_MIN_TH, --dm_min_th DM_MIN_TH
                        Minimum DM allowed (default: 10)
  -du DM_MAX_TH, --dm_max_th DM_MAX_TH
                        Maximum DM allowed (default: 5000)
  -g CLUSTERSIZE_TH, --clustersize_th CLUSTERSIZE_TH
                        Minimum cluster size allowed (default: 2)
```
And to run it along with the above Heimdall command, the example would go as:
```
candcsvmaker.py -f name.fil -c 2*cand
```
This will create a file name `name.csv`.

## your
The next step is making candidates; this is where [`your`](https://github.com/thepetabyteproject/your) comes in. Now we will make the candidates using the above-generated csv file to make candidates. The command is called `your_candmaker.py`.

```
usage: your_candmaker.py [-h] [-v] [-fs FREQUENCY_SIZE]
                         [-g GPU_ID [GPU_ID ...]] [-ts TIME_SIZE] -c
                         CAND_PARAM_FILE [-n NPROC] [-o FOUT] [-opt]
                         [--no_log_file]

Your candmaker! Make h5 candidates from the candidate csv files

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Be verbose (default: False)
  -fs FREQUENCY_SIZE, --frequency_size FREQUENCY_SIZE
                        Frequency size after rebinning (default: 256)
  -g GPU_ID [GPU_ID ...], --gpu_id GPU_ID [GPU_ID ...]
                        GPU ID (use -1 for CPU). To use multiple GPUs (say
                        with id 2 and 3 use -g 2 3 (default: [-1])
  -ts TIME_SIZE, --time_size TIME_SIZE
                        Time length after rebinning (default: 256)
  -c CAND_PARAM_FILE, --cand_param_file CAND_PARAM_FILE
                        csv file with candidate parameters (default: None)
  -n NPROC, --nproc NPROC
                        number of processors to use in parallel (default: 2)
                        (default: 2)
  -o FOUT, --fout FOUT  Output file directory for candidate h5 (default: .)
  -opt, --opt_dm        Optimise DM (default: False)
  --no_log_file         Do not write a log file (default: False)
```
So to make candidates from the above file, it's better to do the following:
- Create a directory called `cands` to save candidate files in.
- Make several candidates in parallel to speed up the process.
- Lets say we decide to make 5 candidates in parallel
- Use GPUs if possible.
```
your_candmaker.py -c name.csv -o cands/ -n 5
```
To use a GPU with GPU ID 2, add `-g 2` to the above command.
The corresponding slurm command for using a GPU would be
```
sbatch -n5 -N1 --partition=gpu --nodelist=notebook --gres=gpu:1 --wrap="your_candmaker.py -c name.csv -o cands/ -n 5 -g 0"
```


Once the above is complete, we can run FETCH to see which ones are real.

#  FETCH
We would run `predict.py` who's help is below:
```
usage: predict.py [-h] [-v] [-g GPU_ID] [-n NPROC] -c DATA_DIR [-b BATCH_SIZE]
                  -m MODEL [-p PROBABILITY]

Fast Extragalactic Transient Candidate Hunter (FETCH)

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Be verbose (default: False)
  -g GPU_ID, --gpu_id GPU_ID
                        GPU ID (use -1 for CPU) (default: 0)
  -n NPROC, --nproc NPROC
                        Number of processors for training (default: 4)
  -c DATA_DIR, --data_dir DATA_DIR
                        Directory with candidate h5s. (default: None)
  -b BATCH_SIZE, --batch_size BATCH_SIZE
                        Batch size for training data (default: 8)
  -m MODEL, --model MODEL
                        Index of the model to train (default: None)
  -p PROBABILITY, --probability PROBABILITY
                        Detection threshold (default: 0.5)
```
To run it with all the cands in `cands/` folder, the command would look like,
```
predict.py -m a -c cands/
```
and the corresponding slurm command would be
```
sbatch -n1 -N1 --partition=gpu --nodelist=notebook --gres=gpu:1 --wrap="predict.py -m a -c cands/"
```
This would produce a file named `results_a.csv` with candidate name, probability of it being an FRB, and label (1=FRB, 0=RFI).

You can also plot the postively labelled candidates using `your_h5plotter.py`. The help is as follows:
```
usage: your_h5plotter.py [-h] [-v] [-f FILES [FILES ...]] [-c RESULTS_CSV]
                         [--publish] [--no_detrend_ft] [--no_save]
                         [-o OUT_DIR] [-mad [MAD_FILTER]] [-n NPROC]
                         [--no_progress] [--no_log_file]

Plot candidate h5 files

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Be verbose (default: False)
  -f FILES [FILES ...], --files FILES [FILES ...]
                        h5 files to be plotted (default: None)
  -c RESULTS_CSV, --results_csv RESULTS_CSV
                        Plot positives in results.csv (default: None)
  --publish             Make publication-quality plots (default: False)
  --no_detrend_ft       Detrend the frequency-time plot (default: True)
  --no_save             Do not save the plot (default: True)
  -o OUT_DIR, --out_dir OUT_DIR
                        Directory to save pngs (default: h5 dir) (default:
                        None)
  -mad [MAD_FILTER], --mad_filter [MAD_FILTER]
                        Median Absolute Deviation spectal clipper, default 3
                        sigma (default: False)
  -n NPROC, --nproc NPROC
                        Number of processors to use in parallel (default: 4)
                        (default: 4)
  --no_progress         Do not show the tqdm bar (default: False)
  --no_log_file         Do not write a log file (default: False)
  ```
  To plot the using the results file, the command would be
  ```
  your_h5plotter.py -c results_a.csv
  ```
  This will generate png files that can be viewed easily.
  
## Citations 
In the end add the following citations:

### Your
```
@article{Aggarwal2020,
  doi = {10.21105/joss.02750},
  url = {https://doi.org/10.21105/joss.02750},
  year = {2020},
  month = nov,
  publisher = {The Open Journal},
  volume = {5},
  number = {55},
  pages = {2750},
  author = {Kshitij Aggarwal and Devansh Agarwal and Joseph Kania and William Fiore and Reshma Thomas and Scott Ransom and Paul Demorest and Robert Wharton and Sarah Burke-Spolaor and Duncan Lorimer and Maura Mclaughlin and Nathaniel Garver-Daniels},
  title = {Your: Your Unified Reader},
  journal = {Journal of Open Source Software}
}
```
### Heimdall
```
@article{Barsdell2012_Dedisp,
  doi = {10.1111/j.1365-2966.2012.20622.x},
  url = {https://doi.org/10.1111/j.1365-2966.2012.20622.x},
  year = {2012},
  month = mar,
  publisher = {Oxford University Press ({OUP})},
  volume = {422},
  number = {1},
  pages = {379--392},
  author = {B. R. Barsdell and M. Bailes and D. G. Barnes and C. J. Fluke},
  title = {Accelerating incoherent dedispersion},
  journal = {Monthly Notices of the Royal Astronomical Society}
}
@phdthesis{Barsdell2012_Heimdall,
       author = {{Barsdell}, B.~R.},
        title = "{Advanced architectures for astrophysical supercomputing}",
       school = {Swinburne University of Technology},
         year = 2012,
        month = jan,
       adsurl = {https://ui.adsabs.harvard.edu/abs/2012PhDT.......418B},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```
### FETCH
```
@article{Agarwal2020,
  doi = {10.1093/mnras/staa1856},
  url = {https://doi.org/10.1093/mnras/staa1856},
  year = {2020},
  month = jun,
  publisher = {Oxford University Press ({OUP})},
  volume = {497},
  number = {2},
  pages = {1661--1674},
  author = {Devansh Agarwal and Kshitij Aggarwal and Sarah Burke-Spolaor and Duncan R Lorimer and Nathaniel Garver-Daniels},
  title = {{FETCH}: A deep-learning based classifier for fast transient classification},
  journal = {Monthly Notices of the Royal Astronomical Society}
}
```
