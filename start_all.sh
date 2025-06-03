#!/usr/bin/env bash

# -------------------------------------------------------
# Change to the script’s own directory
# -------------------------------------------------------
cd "$(dirname "$0")"

# -------------------------------------------------------
# Loop over each Python file beginning with "vfs_",
# skip "vfs_main.py", and wait 5 seconds between launches
# -------------------------------------------------------
for f in vfs_*.py; do
  if [[ "$f" == "vfs_main.py" ]]; then
    echo "Skipping $f"
    continue
  fi

  echo "Launching $f …"

  # GNOME Terminal
  if command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- bash -c "python \"$f\"; echo; read -p 'Press ENTER to close…'; exit"

  # xterm
  elif command -v xterm &> /dev/null; then
    xterm -hold -e "python \"$f\"" &

  # Fallback: run in background
  else
    echo "No supported terminal emulator found – running $f in background."
    python "$f" &
  fi

  # Wait 50 seconds before next launch
  sleep 50
done