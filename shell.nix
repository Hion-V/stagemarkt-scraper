# shell.nix
{ pkgs ? import <nixpkgs> {} }:
let
  my-python-packages = ps: with ps; [
    beautifulsoup4
    pandas
    requests
    html5lib
    dataclasses-json
    # other python packages
  ];
  my-python = pkgs.python3.withPackages my-python-packages;
in my-python.env