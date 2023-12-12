{
  description = "A Nix flake for slurmtoppy";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, nixpkgs }: {
    packages.x86_64-linux.slurmtoppy = nixpkgs.legacyPackages.x86_64-linux.python3Packages.buildPythonPackage {
      pname = "slurmtoppy";
      version = "0.1.0";  
      src = self;
      # propagatedBuildInputs = with nixpkgs.legacyPackages.x86_64-linux.python3Packages; [ 
      # ]
    };

    defaultPackage.x86_64-linux = self.packages.x86_64-linux.slurmtoppy;
  };
}
