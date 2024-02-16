{
  description = "A console-based SLURM job monitoring tool";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, nixpkgs }: {
    packages.x86_64-linux.slurmtoppy = nixpkgs.legacyPackages.x86_64-linux.python3Packages.buildPythonApplication {
      pname = "slurmtoppy";
      version = "0.1.5";  
      src = self;
    };

    defaultPackage.x86_64-linux = self.packages.x86_64-linux.slurmtoppy;

    apps.x86_64-linux.slurmtop = {
      type = "app";
      program = "${self.packages.x86_64-linux.slurmtoppy}/bin/slurmtop";
    };
    
    defaultApp.x86_64-linux = self.apps.x86_64-linux.slurmtop;
  };
}
