# slurmtoppy
A console-based [SLURM](https://slurm.schedmd.com) job monitoring tool.

What `top` is for `ps / kill`, `slurtoppy` is for `squeue / scancel`.

## Installation
```bash
pip install slurmtoppy
```
There are no dependencies, except of standard SLURM commands.

## Running
```bash
slurmtop
```

## Features
- Show list of running jobs (a.k.a. `watch squeue`).
- Cancel selected job (no job_id input needed!)
- View output of selected job with `tail` or `less` (provided that output file in the current working directory)