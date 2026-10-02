import sys
from pathlib import Path
import hashlib
# sys.argv holds words supplied in the terminal
# pyhton minigit.py init
# -> ["minigit.py", "init"]

if len(sys.argv) == 2 and sys.argv[1] == "init":
    root = Path.cwd()  # current dir
    if (root / ".minigit").exists():
        print("Repository already exists")
    else:
        git_dir = root / ".minigit"  # joins path components
        git_dir.mkdir()  # creates the directory
        (git_dir / "index").touch()  # creates the file (empty)
        (git_dir / "HEAD").write_text(
            "refs/heads/main"
        )  # head stores the path of the currently active branch
        (git_dir / "objects").mkdir()  # creates the directory
        (git_dir / "refs" / "heads").mkdir(parents=True)
        # parents=true create missing parent folders too
elif len(sys.argv) == 3 and sys.argv[1] == "add":
    path = Path(sys.argv[2])
    root = Path.cwd()
    git_dir = root / ".minigit"
    if not git_dir.exists():
        print("Not a MiniGit repository")
    elif not path.exists():
        print(f"File {path} does not exist")
    else:
        data = path.read_bytes()
        hash_value = hashlib.sha1(data).hexdigest()
        object_path = git_dir / "objects" / hash_value
        if not object_path.exists():
            object_path.write_bytes(data)
        index_path = git_dir / "index"
        # load existing index entries into a dixtionary
        staged_files = {}
        for line in index_path.read_text().splitlines():
            if not line.strip():
                continue
            stored_hash, stored_path = line.split(maxsplit=1)
            staged_files[stored_path] = stored_hash
        # add the new file to the staging area
        staged_files[str(path)] = hash_value
        # write the updated index back to disk
        with index_path.open("w") as f:
            for p, h in staged_files.items():
                f.write(f"{h} {p}\n")
else:
    print("Invalid command")
