# slurmtoppy
A console-based [SLURM](https://slurm.schedmd.com) job monitoring tool.

What `htop` is for `ps`, `slurmtoppy` is for `squeue`.

## Installation
### pip
```bash
pip install slurmtoppy
```
There are no dependencies, except of standard SLURM commands.

## Running
After installation:
```bash
slurmtop
```

Using nix, without installation:
```
nix run github:ischurov/slurmtoppy
```

## Screenshot
<img width="704" alt="Screenshot of slurmtop command" src="https://github.com/ischurov/slurmtoppy/assets/2717321/b9c691bb-a78a-4ddb-9fe9-a2b341a84e02">

## Features
- Show list of running jobs (a.k.a. `watch squeue`).
- Cancel the selected job (no job_id input needed!)
- View output of the selected job with `tail` or `less`
- SSH to a node where the selected job runs (provided it's a one-node job)