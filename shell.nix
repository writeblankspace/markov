# run either:
# $ nix-shell
# $ echo "use nix" > .envrc && direnv allow
let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    pkgs.sqlite
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.discordpy
      python-pkgs.python-dotenv
      python-pkgs.numpy
    ]))
  ];
}
