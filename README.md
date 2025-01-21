Pull requests updating this README are very welcome!

- With a flake-enabled [nixpkgs](https://nixos.org) install:

```
nix run github:anderslundstedt/check-unicode-coverage/main -- args
```

- Without a flake-enabled nixpkgs install: the Python script
  `check-unicode-coverage.py` ought to run in most Python 3 environments that
  has the [`Python-fontconfig`](https://github.com/vayn/python-fontconfig)
  package providing Python bindings for
  [`FontConfig`](https://www.freedesktop.org/wiki/Software/fontconfig/).
