Pull requests updating this README are very welcome!

- With a flake-enabled¹ install of the [Nix package manager](https://nixos.org):

  ```
  nix run github:anderslundstedt/check-unicode-coverage/main -- args
  ```

  Example run:

  ```
  $ nix run github:anderslundstedt/check-unicode-coverage/main -- -h
  usage: check-unicode-coverage [-h] [--characters CHARACTERS] [--print-found] [--ignore-missing] font [font ...]
  
  check fonts' Unicode coverage
  
  positional arguments:
    font                  path to font
  
  options:
    -h, --help            show this help message and exit
    --characters CHARACTERS
                          path to input text file (default: /nix/store/l7cqp88jc4wh12fjyqcvpss1fn3mckrk-check-unicode-
                          coverage-20250121/characters.txt)
    --print-found         print found characters (default: False)
    --ignore-missing      do not print missing characters (default: False)
  ```

- Without a flake-enabled nixpkgs install: the Python script
  `check-unicode-coverage.py` ought to run in most Python 3.12 environments that
  has the [`Python-fontconfig`](https://github.com/vayn/python-fontconfig)
  package providing Python bindings for
  [`FontConfig`](https://www.freedesktop.org/wiki/Software/fontconfig/).


¹ This one should work-out-of-the box:

<https://github.com/DeterminateSystems/nix-installer>
