{
  description = "A very basic flake";

  inputs.nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  inputs.treefmt-nix.url = "github:numtide/treefmt-nix";

  inputs.uv2nix.url = "github:pyproject-nix/uv2nix";
  inputs.uv2nix.inputs.pyproject-nix.follows = "pyproject-nix";
  inputs.uv2nix.inputs.nixpkgs.follows = "nixpkgs";

  inputs.pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
  inputs.pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";

  inputs.pyproject-build-systems.url = "github:pyproject-nix/build-system-pkgs";
  inputs.pyproject-build-systems.inputs.pyproject-nix.follows = "pyproject-nix";
  inputs.pyproject-build-systems.inputs.uv2nix.follows = "uv2nix";
  inputs.pyproject-build-systems.inputs.nixpkgs.follows = "nixpkgs";

  outputs =
    inputs:
    let
      pkgs = inputs.nixpkgs.legacyPackages.x86_64-linux;

      lib = pkgs.lib;

      treefmtEval = inputs.treefmt-nix.lib.evalModule pkgs {
        programs.nixfmt.enable = true;
        programs.ruff-format.enable = true;
      };

      workspace = inputs.uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };

      overlay = workspace.mkPyprojectOverlay {
        sourcePreference = "wheel";
      };

      editableOverlay = workspace.mkEditablePyprojectOverlay {
        root = "$REPO_ROOT";
      };

      pythonSets =
        (pkgs.callPackage inputs.pyproject-nix.build.packages {
          python = pkgs.python3;
        }).overrideScope
          (
            lib.composeManyExtensions [
              inputs.pyproject-build-systems.overlays.wheel
              overlay
            ]
          );

      pythonSet = pythonSets.overrideScope editableOverlay;

      virtualenv = pythonSet.mkVirtualEnv "hello-world-dev-env" workspace.deps.all;

    in
    {

      formatter.x86_64-linux = treefmtEval.config.build.wrapper;

      devShells.x86_64-linux.default = pkgs.mkShellNoCC {
        packages = [
          pkgs.nixd
          pkgs.uv
          virtualenv
        ];
        env.UV_NO_SYNC = "1";
        env.UV_PYTHON = pythonSet.python.interpreter;
        env.UV_PYTHON_DOWNLOADS = "never";
        shellHook = ''
          unset PYTHONPATH
          export REPO_ROOT=$(git rev-parse --show-toplevel)
        '';
      };

    };
}
