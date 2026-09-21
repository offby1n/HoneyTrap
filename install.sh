#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/offby1n/HoneyTrap.git"
APP="honeytrap"
SCRIPT="honeytrap"
SRC_DIR="$HOME/.local/share/honeytrap"
BIN_DIR="$HOME/.local/bin"

# Work out where the source is.
# - Run from a cloned repo (honeytrap sits next to us): install from here.
# - Piped from curl (no local file): clone the repo, or pull if already cloned.
if [ -f "$SCRIPT" ]; then
    SRC="$(pwd)/$SCRIPT"
elif command -v git >/dev/null 2>&1; then
    if [ -d "$SRC_DIR/.git" ]; then
        echo "updating existing clone in $SRC_DIR"
        git -C "$SRC_DIR" pull --quiet
    else
        echo "cloning $REPO"
        git clone --quiet "$REPO" "$SRC_DIR"
    fi
    SRC="$SRC_DIR/$SCRIPT"
else
    echo "error: git not found and no honeytrap script in this folder"
    echo "either install git, or run this from the cloned repo"
    exit 1
fi

# Make it executable and link it as the bare command 'honeytrap'.
chmod +x "$SRC"
mkdir -p "$BIN_DIR"
ln -sf "$SRC" "$BIN_DIR/$APP"

# Warn if the bin dir isn't on PATH (so the command won't be found).
case ":$PATH:" in
    *":$BIN_DIR:"*) : ;;
    *) echo "NOTE: $BIN_DIR is not on your PATH — add it to your shell profile" ;;
esac

echo "installed: run '$APP -h'   (needs sudo to write /var/log/honeytrap.log)"
