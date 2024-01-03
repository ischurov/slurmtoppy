# slurmtoppy
A console-based [SLURM](https://slurm.schedmd.com) job monitoring tool.

What `htop` is for `ps`, `slurmtoppy` is for `squeue`.

## Installation
### pip
```bash
pip install slurmtoppy
```
There are no dependencies, except of standard SLURM commands.

### nix
```nix
buildPythonPackage rec {
    pname = "slurmtoppy";
    version = "0.1.0";
    src = fetchPypi {
        inherit pname version;
        sha256 = "sha256-IcI/tlH9p5hdOkohZcMTl/eGhvHCrg9LlPkCRzlT/Dg=";
    };
    doCheck = false;
}
```

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
- Cancel selected job (no job_id input needed!)
- View output of selected job with `tail` or `less` (provided that output file in the current working directory)
