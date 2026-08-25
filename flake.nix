# flake based on
# https://github.com/NixOS/templates/blob/ad0e221dda33c4b564fad976281130ce34a20cb9/bash-hello/flake.nix
{
  description = "CLI tool to check fonts' Unicode coverage";

  inputs.pins.url = "github:anderslundstedt/nix-pins";

  inputs.nixpkgs-unstable.follows = "pins/nixpkgs-unstable";

  outputs = inputs@{self,...}: (
    let
      # to work with older version of flakes
      lastModifiedDate =
        self.lastModifiedDate or self.lastModified or "19700101";

      # generate a user-friendly version number.
      version = builtins.substring 0 8 lastModifiedDate;

      # confirmed to work on the following systems
      systems-linux    = ["x86_64-linux"  "aarch64-linux"];
      systems-darwin   = ["x86_64-darwin" "aarch64-darwin"];
      supportedSystems = systems-linux ++ systems-darwin;

      # helper function to generate an attrset
      # '{ x86_64-linux = f "x86_64-linux"; ... }'.
      forAllSystems = inputs.nixpkgs-unstable.lib.genAttrs supportedSystems;

      get-pkgs-for-system = system:
        inputs.pins.nixpkgs-24-11.${system}.legacyPackages.${system};

      get-python-env-for-system = pkgs: system: is-dev-shell: (
        pkgs.python312.withPackages (
          python-packages: builtins.filter(x: x != 0) [
            (if is-dev-shell then python-packages.ipython else 0)
            python-packages.python-fontconfig
          ]
        )
      );
    in {
      devShell = forAllSystems(system:
        let
          pkgs-24-11    = get-pkgs-for-system system;
          python-env    = get-python-env-for-system pkgs-24-11 system true;
          pkgs-unstable = inputs.nixpkgs-unstable.legacyPackages.${system};
        in (
          pkgs-unstable.mkShell {
            buildInputs = [
              python-env
              pkgs-unstable.pyright
              pkgs-unstable.gh
              pkgs-unstable.gh-markdown-preview
            ];
          }
        )
      );

      defaultPackage = forAllSystems(system:
        let
          pkgs-24-11    = get-pkgs-for-system system;
          python-env    = get-python-env-for-system pkgs-24-11 system false;
          pkgs-unstable = inputs.nixpkgs-unstable.legacyPackages.${system};
        in (
          pkgs-unstable.stdenv.mkDerivation {
            name = "check-unicode-coverage-${version}";

            buildInputs = [pkgs-unstable.makeWrapper];

            unpackPhase = "true";

            installPhase = ''
              mkdir -p $out/bin
              cp ${./check-unicode-coverage.py} $out/check-unicode-coverage
              cp ${./font_query.py}             $out/font_query.py
              cp ${./characters.txt}            $out/characters.txt
              makeWrapper $out/check-unicode-coverage $out/bin/check-unicode-coverage --set PATH ${inputs.nixpkgs-unstable.lib.makeBinPath [python-env]}
            '';
          }
        )
      );
    }
  );
}
