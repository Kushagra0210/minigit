import sys
from pathlib import Path

# sys.argv holds words supplied in the terminal
# pyhton minigit.py init
# -> ["minigit.py", "init"]
if len(sys.argv) != 2 or sys.argv[1] != "init":
    print("Usage: python minigit.py init")
else:
    # existing initialisation logic goes here
    root = Path.cwd()  # current dir
    if (root / ".minigit").exists():
        print("Repository already exists")
    else:
        git_dir = root / ".minigit"  # joins path components
        git_dir.mkdir()  # creates the directory
        (git_dir / "index").touch()  # creates the file (empty)
        (git_dir / "HEAD").write_text("NO COMMIT YET")  # writes text to a file
        (git_dir / "objects").mkdir()  # creates the directory
