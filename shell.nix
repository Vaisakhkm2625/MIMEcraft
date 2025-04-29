
with import <nixpkgs> { };

mkShell {
  name = "pyqt6-shell";

  buildInputs = [
    python3
    python3Packages.pyqt6
  ];

  shellHook = ''
    echo "Environment ready. Run with:"
    echo "  python mime_changer.py"
  '';
}
