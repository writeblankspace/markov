# run nix-shell to use
let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    pkgs.sqlite
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.discordpy
      python-pkgs.python-dotenv
    ]))
  ];
}
