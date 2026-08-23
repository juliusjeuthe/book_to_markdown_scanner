#!/usr/bin/env bash
# Launch git gui from WSL. Usage: ./run_git_gui_wsl.sh [repo_path]
REPO_PATH="${1:-$(pwd)}"
cd "$REPO_PATH" || exit 1

# Try running git gui in WSL (requires DISPLAY/X server configured)
if command -v git >/dev/null 2>&1; then
  if git gui &>/dev/null & then
    exit 0
  fi
fi

# Fallback: try launching Git for Windows' git-gui.exe via mounted path
WIN_PATHS=(
  "/mnt/c/Program Files/Git/cmd/git-gui.exe"
  "/mnt/c/Program Files/Git/mingw64/bin/git-gui.exe"
  "/mnt/c/Program Files (x86)/Git/cmd/git-gui.exe"
)
for p in "${WIN_PATHS[@]}"; do
  if [ -x "$p" ]; then
    "$p" &
    exit 0
  fi
done

echo "Could not launch git gui. Install git-gui in WSL or Git for Windows, or configure an X server for WSL." >&2
exit 1
