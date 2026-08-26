{
  description = "CLI tool to check fonts' Unicode coverage";

  inputs.pins.url                 = "github:anderslundstedt/nix-pins";
  inputs.flake-utils.follows      = "pins/flake-utils";
  inputs.nixpkgs-unstable.follows = "pins/nixpkgs-unstable";

  outputs = inputs@{self,...}:
    let
      # to work with older version of flakes
      lastModifiedDate =
        self.lastModifiedDate or self.lastModified or "19700101";

      # generate a user-friendly version number.
      version = builtins.substring 0 8 lastModifiedDate;

      # confirmed to work on the following systems
      systems-linux    = ["x86_64-linux"  "aarch64-linux"];
      systems-darwin   = ["aarch64-darwin"];
      supportedSystems = systems-linux ++ systems-darwin;
    in
      inputs.flake-utils.lib.eachSystem supportedSystems (system:
        let
          nixpkgs-24-11    =
            inputs.pins.nixpkgs-24-11.${system}.legacyPackages.${system};
          nixpkgs-stable   =
            inputs.pins.nixpkgs-stable.${system}.legacyPackages.${system};
          nixpkgs-unstable =
            inputs.nixpkgs-unstable.legacyPackages.${system};
          python-env    = is-dev-shell: (
            nixpkgs-24-11.python312.withPackages (python-packages:
              builtins.filter(x: x != 0) [
                (if is-dev-shell then python-packages.ipython else 0)
                python-packages.python-fontconfig
              ]
            )
          );
        in {
          devShells.default = nixpkgs-stable.mkShell {
            buildInputs = [
              (python-env true)
              nixpkgs-unstable.pyright
              nixpkgs-unstable.gh
              nixpkgs-unstable.gh-markdown-preview
            ];
          };
          packages.default = nixpkgs-stable.stdenv.mkDerivation {
            name = "check-unicode-coverage-${version}";

            inherit version;

            buildInputs = [nixpkgs-stable.makeWrapper];

            unpackPhase = "true";

            installPhase = ''
              mkdir -p $out/bin
              cp ${./check-unicode-coverage.py} $out/check-unicode-coverage
              cp ${./font_query.py}             $out/font_query.py
              cp ${./characters.txt}            $out/characters.txt
              makeWrapper $out/check-unicode-coverage $out/bin/check-unicode-coverage --set PATH ${
                nixpkgs-stable.lib.makeBinPath [(python-env false)]
              }
            '';
          };
        }
      );
}
