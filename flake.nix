{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/release-23.11";
    nixpkgs-unstable.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, nixpkgs-unstable, flake-utils }:
    flake-utils.lib.eachDefaultSystem(system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        unstable = nixpkgs-unstable.legacyPackages.${system};
      in
      with pkgs; {
        devShells.default = mkShell {
          name = "dev-environment";
          buildInputs = [
            bash
            python311
            unstable.isort
            unstable.mypy
            unstable.poetry
            unstable.ruff
          ] ++ (
            if ("$INSIDE_DOCKER" != "true") then [
              unstable.pre-commit
              entr
              flyctl
              httpie
              jq
              lazygit
              ripgrep
              silver-searcher
              tmux
              tree
              yazi
            ] else [
            ]
          );
          shellHook = ''
            if [[ $INSIDE_DOCKER != "true" ]]; then
              export POETRY_VIRTUALENVS_IN_PROJECT="true"
            fi
            unset PYTHONPATH
            poetry env use ${python311.executable}
        
            export PATH="$(poetry env info -p)/bin:$PATH"
          '';
        };
      }
    );
}
