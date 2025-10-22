# flake.nix

{
  description = "piss";

  outputs =
    { self, nixpkgs, ... }:
    {
      devShell.x86_64-linux =
        let
          pkgs = import nixpkgs { system = "x86_64-linux"; };

          pythonEnv = pkgs.python313.withPackages (
            ps: with ps; [
              pip
            ]
          );
        in
        pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.nixfmt-rfc-style
            pkgs.cmake
            pkgs.ninja
            pkgs.pkg-config
            pkgs.gcc
          ];

          shellHook = ''
            echo "hiiieee !!!"

            python3 -m venv .venv
            source .venv/bin/activate
            pip install --upgrade pip scikit-build-core setuptools wheel

            echo install with: \"pip install --no-build-isolation .\"
          '';
        };
    };
}
