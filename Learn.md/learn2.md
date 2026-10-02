# MiniGit — Day 2

## Goal

Today I extended MiniGit so it can:

```text
1. Initialize a repository
2. Create MiniGit internal folders
3. Understand the add command
4. Read file contents
5. Generate a SHA-1 hash
6. Store file contents as an object
7. Add hash + filepath into the index
```

---

# 1. Imports

```python
import sys
from pathlib import Path
import hashlib
```

### `import sys`

```python
import sys
```

Used to access command-line arguments.

Example:

```bash
python minigit.py init
```

Python stores this as:

```text
sys.argv[0] -> "minigit.py"
sys.argv[1] -> "init"
```

Another example:

```bash
python minigit.py add hello.txt
```

becomes:

```text
sys.argv[0] -> "minigit.py"
sys.argv[1] -> "add"
sys.argv[2] -> "hello.txt"
```

---

### `from pathlib import Path`

```python
from pathlib import Path
```

`Path` helps us work with:

```text
files
folders
file paths
```

instead of manually joining strings.

Example:

```python
git_dir = root / ".minigit"
```

means:

```text
current_folder/.minigit
```

---

### `import hashlib`

```python
import hashlib
```

Used to generate hashes.

For MiniGit we currently use:

```python
hashlib.sha1(...)
```

A hash gives the contents of a file an identifier.

---

# 2. Detecting the `init` command

```python
if len(sys.argv) == 2 and sys.argv[1] == "init":
```

This checks:

```text
Did the user type exactly:

python minigit.py init
```

Here:

```text
len(sys.argv) == 2
```

means there are two terminal arguments:

```text
["minigit.py", "init"]
```

And:

```python
sys.argv[1] == "init"
```

checks whether the command is actually `init`.

---

# 3. Getting the Current Directory

```python
root = Path.cwd()
```

`cwd` means:

```text
Current Working Directory
```

Example:

```text
/home/user/project
```

So:

```python
root
```

represents the folder where MiniGit is currently being used.

---

# 4. Checking Whether MiniGit Already Exists

```python
if (root / ".minigit").exists():
```

This builds the path:

```text
current_folder/.minigit
```

Then:

```python
.exists()
```

checks whether that path already exists.

If it exists:

```python
print("Repository already exists")
```

This prevents us from accidentally initializing the same repository again.

---

# 5. Creating `.minigit`

```python
git_dir = root / ".minigit"
```

This creates a `Path` representing:

```text
current_folder/.minigit
```

Then:

```python
git_dir.mkdir()
```

creates the actual folder.

Result:

```text
project/
└── .minigit/
```

---

# 6. Creating the Index

```python
(git_dir / "index").touch()
```

This creates an empty file:

```text
.minigit/index
```

The index represents our **staging area**.

Eventually it stores information such as:

```text
hash filepath
```

Example:

```text
abc123 hello.txt
```

---

# 7. Creating HEAD

```python
(git_dir / "HEAD").write_text("refs/heads/main")
```

This creates:

```text
.minigit/HEAD
```

and puts:

```text
refs/heads/main
```

inside it.

Conceptually:

```text
HEAD
 ↓
refs/heads/main
 ↓
latest commit
```

`HEAD` tells MiniGit which branch is currently active.

Currently:

```text
HEAD
→ main
```

---

# 8. Creating the Object Store

```python
(git_dir / "objects").mkdir()
```

Creates:

```text
.minigit/objects/
```

This folder stores objects.

For now we are storing **file contents** as objects.

Conceptually:

```text
file contents
     ↓
   SHA-1
     ↓
objects/<hash>
```

---

# 9. Creating the Branch Directory

```python
(git_dir / "refs" / "heads").mkdir(parents=True)
```

Creates:

```text
.minigit/
└── refs/
    └── heads/
```

`heads/` will eventually contain branch references.

Example:

```text
refs/heads/main
```

may eventually contain:

```text
abc123...
```

where `abc123...` is the latest commit hash.

---

## Why `parents=True`?

Without it:

```python
.mkdir()
```

would fail if:

```text
refs/
```

does not already exist.

Using:

```python
parents = True
```

means:

```text
create missing parent directories too
```

So both:

```text
refs/
```

and:

```text
refs/heads/
```

can be created together.

---

# 10. Detecting the `add` Command

```python
elif len(sys.argv) == 3 and sys.argv[1] == "add":
```

Checks for a command like:

```bash
python minigit.py add hello.txt
```

Here:

```text
sys.argv[0] = minigit.py
sys.argv[1] = add
sys.argv[2] = hello.txt
```

---

# 11. Getting the File Path

```python
path = Path(sys.argv[2])
```

If the user runs:

```bash
python minigit.py add hello.txt
```

then:

```text
sys.argv[2]
→ hello.txt
```

and:

```python
Path(sys.argv[2])
```

creates a Python path representing that file.

---

# 12. Finding `.minigit`

```python
root = Path.cwd()
git_dir = root / ".minigit"
```

Again:

```text
root
→ current directory

git_dir
→ current_directory/.minigit
```

---

# 13. Checking Whether the Repository Exists

```python
if not git_dir.exists():
    print("Not a MiniGit repository")
```

Before allowing:

```bash
python minigit.py add hello.txt
```

MiniGit checks whether:

```text
.minigit/
```

exists.

If not:

```text
init was never run
```

so MiniGit refuses to add the file.

---

# 14. Checking Whether the File Exists

```python
elif not path.exists():
    print(f"File {path} does not exist")
```

This checks whether the file requested by the user actually exists.

Example:

```bash
python minigit.py add random.txt
```

If `random.txt` does not exist:

```text
File random.txt does not exist
```

This check must happen before reading the file.

---

# 15. Reading Raw File Bytes

```python
data = path.read_bytes()
```

This reads the exact bytes stored inside the file.

Example:

```text
hello.txt
```

contains:

```text
hello
```

Then conceptually:

```python
data = b"hello"
```

The `b` means:

```text
bytes
```

We use:

```python
read_bytes()
```

instead of:

```python
read_text()
```

because MiniGit should eventually support:

```text
.txt
.cpp
.jpg
.png
.pdf
.exe
```

not only text files.

---

# 16. Generating the SHA-1 Hash

```python
hash_value = hashlib.sha1(data).hexdigest()
```

Two things happen here.

First:

```python
hashlib.sha1(data)
```

generates a SHA-1 hash from the file's bytes.

Then:

```python
.hexdigest()
```

converts the raw hash into readable hexadecimal text.

Example:

```text
"hello"
↓
SHA-1
↓
a hexadecimal hash
```

So:

```python
hash_value
```

might contain something like:

```text
f572d396fae9206628714fb2ce00f72e94f2258f
```

---

# 17. Why We Hash the Contents

We hash:

```text
file contents
```

not just the filename.

Example:

```text
a.txt → "hello"
b.txt → "hello"
```

Both contain exactly the same bytes.

Therefore:

```text
same content
→ same hash
→ same object
```

But:

```text
a.txt → "hello"
b.txt → "bye"
```

means:

```text
different content
→ different hash
→ different objects
```

This is called:

```text
Content Addressing
```

---

# 18. Creating the Object Path

```python
object_path = git_dir / "objects" / hash_value
```

Suppose:

```text
hash_value = abc123
```

Then:

```text
object_path
```

becomes:

```text
.minigit/objects/abc123
```

So the hash becomes the object's filename.

---

# 19. Avoiding Duplicate Objects

```python
if not object_path.exists():
```

This checks whether MiniGit already stored this content.

If the object already exists:

```text
same content
→ same hash
→ object already stored
```

There is no need to save another copy.

---

# 20. Writing the Object

```python
object_path.write_bytes(data)
```

This writes the exact file contents into:

```text
.minigit/objects/<hash>
```

Example:

```text
hello.txt
     ↓
"hello"
     ↓
SHA-1
     ↓
abc123
     ↓
.minigit/objects/abc123
```

Inside that object:

```text
hello
```

This object is conceptually our first simple **blob**.

---

# 21. Finding the Index

```python
index_path = git_dir / "index"
```

Creates a path pointing to:

```text
.minigit/index
```

The index is our staging area.

---

# 22. Opening the Index

```python
with index_path.open("a") as f:
```

The:

```text
"a"
```

means:

```text
append mode
```

So Python does not erase the existing file.

Instead it adds new content at the end.

Example:

Existing:

```text
hash1 a.txt
```

After appending:

```text
hash1 a.txt
hash2 b.txt
```

---

# 23. Writing to the Index

```python
f.write(f"{hash_value} {path}\n")
```

This writes:

```text
hash filepath
```

into the index.

Example:

```text
f572d396fae9206628714fb2ce00f72e94f2258f hello.txt
```

So MiniGit now knows:

```text
hello.txt
   ↓
blob hash
   ↓
object storage
```

Conceptually:

```text
Index

hello.txt
   ↓
f572d396...
   ↓
.minigit/objects/f572d396...
```

---

# 24. Current `add` Flow

Our current `add` implementation works like this:

```text
python minigit.py add hello.txt
              ↓
       get hello.txt path
              ↓
     check .minigit exists
              ↓
      check hello.txt exists
              ↓
        read file bytes
              ↓
       calculate SHA-1
              ↓
        create object path
              ↓
       object already exists?
          /           \
        yes            no
        ↓              ↓
   don't store     store bytes
          \          /
             ↓
         update index
```

---

# 25. Current Repository Structure

After:

```bash
python minigit.py init
```

we get:

```text
project/
│
├── minigit.py
│
└── .minigit/
    ├── HEAD
    ├── index
    ├── objects/
    └── refs/
        └── heads/
```

After:

```bash
python minigit.py add hello.txt
```

we may get:

```text
.minigit/
│
├── HEAD
│
├── index
│
├── objects/
│   └── f572d396...
│
└── refs/
    └── heads/
```

---

# 26. What Each Internal Part Means

```text
.minigit/
```

MiniGit's internal repository.

---

```text
HEAD
```

Points to the currently active branch.

Currently:

```text
refs/heads/main
```

---

```text
index
```

Represents the staging area.

Currently stores:

```text
hash filepath
```

---

```text
objects/
```

Stores file contents using their hash as the filename.

---

```text
refs/heads/
```

Will eventually store branch pointers.

---

# 27. Important Concepts Learned

Today I learned:

```text
Command-line arguments
Path objects
Current Working Directory
Checking file existence
Creating directories
Creating files
Reading raw bytes
SHA-1 hashing
Hexadecimal hashes
Content-addressed storage
Blob objects
Object deduplication
Staging/index concept
Append mode
HEAD
Branch references
```

---

# 28. Important Rules to Remember

### Rule 1

```text
same content
→ same SHA-1 hash
```

### Rule 2

```text
different content
→ different hash
```

### Rule 3

```text
hash
→ identifies an object
```

### Rule 4

```text
objects/<hash>
→ stores file contents
```

### Rule 5

```text
index
→ remembers which file corresponds to which hash
```

### Rule 6

```text
HEAD
→ tells us our current branch
```

---

# 29. Current Complete Code

```python
import sys
from pathlib import Path
import hashlib

# sys.argv holds words supplied in the terminal
# python minigit.py init
# -> ["minigit.py", "init"]

if len(sys.argv) == 2 and sys.argv[1] == "init":
    # Get the directory where MiniGit is being run
    root = Path.cwd()

    # Check if this folder is already a MiniGit repository
    if (root / ".minigit").exists():
        print("Repository already exists")

    else:
        # Create the path to the MiniGit internal directory
        git_dir = root / ".minigit"

        # Create .minigit/
        git_dir.mkdir()

        # Create an empty staging/index file
        (git_dir / "index").touch()

        # HEAD points to our current branch: main
        (git_dir / "HEAD").write_text("refs/heads/main")

        # Create object storage
        (git_dir / "objects").mkdir()

        # Create branch-reference folders
        # parents=True creates refs/ if it does not exist
        (git_dir / "refs" / "heads").mkdir(parents=True)


elif len(sys.argv) == 3 and sys.argv[1] == "add":
    # Get the filename supplied after "add"
    path = Path(sys.argv[2])

    # Get current working directory
    root = Path.cwd()

    # Path to MiniGit's internal repository
    git_dir = root / ".minigit"

    # add should only work inside a MiniGit repository
    if not git_dir.exists():
        print("Not a MiniGit repository")

    # Make sure the requested file actually exists
    elif not path.exists():
        print(f"File {path} does not exist")

    else:
        # Read exact raw bytes of the file
        data = path.read_bytes()

        # Calculate SHA-1 and convert it to readable hexadecimal
        hash_value = hashlib.sha1(data).hexdigest()

        # Use the hash as the object's filename
        object_path = git_dir / "objects" / hash_value

        # Store the object only if it hasn't already been stored
        if not object_path.exists():
            object_path.write_bytes(data)

        # Path to our staging/index file
        index_path = git_dir / "index"

        # Open index in append mode
        with index_path.open("a") as f:
            # Store:
            # <blob hash> <filepath>
            f.write(f"{hash_value} {path}\n")


else:
    # Command did not match init or add
    print("Invalid command")
```

---

# 30. Day 2 Progress

```text
[✓] Implement MiniGit init

[✓] Create .minigit directory

[✓] Create objects/

[✓] Create refs/heads/

[✓] Create HEAD

[✓] Point HEAD to main

[✓] Create index

[✓] Detect add command

[✓] Check repository exists

[✓] Check file exists

[✓] Read file bytes

[✓] Generate SHA-1 hash

[✓] Store blob object

[✓] Avoid duplicate blob storage

[✓] Add hash + path into index

[ ] Prevent duplicate index entries

[ ] Update an existing staged file

[ ] Build commit objects

[ ] Connect branch to commit

[ ] Implement log
```

---

# Day 3 Starting Point

Our current index uses append mode:

```python
index_path.open("a")
```

Therefore doing:

```bash
python minigit.py add hello.txt
python minigit.py add hello.txt
python minigit.py add hello.txt
```

can create:

```text
hash1 hello.txt
hash1 hello.txt
hash1 hello.txt
```

This is not what we want.

On Day 3 we will learn how to make the index behave like:

```text
filepath → latest staged hash
```

instead of blindly adding duplicate entries.

That will teach us:

```text
reading structured files
parsing existing index entries
updating mappings
rewriting files
staging modified versions
```
