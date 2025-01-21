SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -O globstar -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.PHONY: build update-flake clean

build:
	nix build

update-flake:
	nix flake update

clean:
	rm -rf .direnv
	rm -rf ./result
