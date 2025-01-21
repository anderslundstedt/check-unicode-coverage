# flake based on
# https://github.com/NixOS/templates/blob/ad0e221dda33c4b564fad976281130ce34a20cb9/bash-hello/flake.nix
{
  description = "CLI tool to check fonts' Unicode coverage";

  inputs.nixpkgs.url = "nixpkgs/nixpkgs-unstable";

  outputs = inputs@{self, nixpkgs}: (
    let
      # to work with older version of flakes
      lastModifiedDate =
        self.lastModifiedDate or self.lastModified or "19700101";

      # generate a user-friendly version number.
      version = builtins.substring 0 8 lastModifiedDate;

      # confirmed to work on the following systems
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      # helper function to generate an attrset
      # '{ x86_64-linux = f "x86_64-linux"; ... }'.
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;

      get-nixpkgs-for-system = system:
        (import inputs.nixpkgs {inherit system;});

      get-python-env-for-system = system: (
        (get-nixpkgs-for-system system).python3.withPackages (
          python-packages: [
            python-packages.python-fontconfig
          ]
        )
      );
    in {
      devShell = forAllSystems(system:
        (get-nixpkgs-for-system system).mkShell {
          buildInputs = [
            (get-python-env-for-system system)
          ];
        }
      );

      defaultPackage = forAllSystems(system:
        let
          nixpkgs    = get-nixpkgs-for-system    system;
          python-env = get-python-env-for-system system;
        in (
          nixpkgs.stdenv.mkDerivation {
            name = "check-unicode-coverage-${version}";

            buildInputs = [nixpkgs.makeWrapper];

            unpackPhase = "true";

            installPhase = ''
              mkdir -p $out/bin
              cp ${./check-unicode-coverage.py} $out/check-unicode-coverage
              cp ${./characters.txt} $out/characters.txt
              makeWrapper $out/check-unicode-coverage $out/bin/check-unicode-coverage --set PATH ${nixpkgs.lib.makeBinPath [python-env]}
            '';
          }
        )
      );
    }
  );
}
