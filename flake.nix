
{
  description = "PyQt5 MIME changer app";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
      in {
        devShells.default = pkgs.mkShell {
          name = "pyqt5-mimechanger-shell";

          buildInputs = with pkgs; [
            python3
            python3Packages.pyqt5
            # Optional: If you want to run update-desktop-database from the app
            desktop-file-utils
          ];

          shellHook = ''
            echo "Running PyQt5 MIME changer shell"
            echo "You can run the app with: python mime_changer.py"
          '';
        };
      });
}
