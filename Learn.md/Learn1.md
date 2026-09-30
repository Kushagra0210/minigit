# MiniGit Learning Log — Day 1

**Date:** 30 September 2026

## Goal

Today I started learning how Git works internally by building a simplified version called **MiniGit**.

The goal is not just to use Git commands.

The goal is to understand:

- what Git stores
- how Git detects changes
- how commits are represented
- why hashes are important
- how branches and history work internally

---

# 1. What problem does Git solve?

Suppose I have a file:

```text
main.cpp
```

Today it contains:

```cpp
cout << "Hello";
```

Tomorrow I change it to:

```cpp
cout << "Hello World";
```

A version control system should help me answer:

```text
What changed?
Who changed it?
When was it changed?
Can I go back to the old version?
Can multiple people work on different versions?
```

Git solves these problems using a system based heavily on:

```text
files
+
snapshots
+
hashes
+
objects
+
commit history
```
---
# 2. Three important Git areas
## Working Directory
This is where I normally edit my files.
Example:
```text
project/
│
├── main.cpp
├── README.md
└── app.py
```
These are normal files on my computer.
If I edit:
```text
main.cpp
```
I am changing the **working directory**.
---
## Staging Area
The staging area contains the changes I want to include in the next commit.
Example command:
```bash
git add main.cpp
# git      -> run the Git program
# add      -> tell Git to prepare/stage something
# main.cpp -> the file I want in the next commit
```
Conceptually:
```text
Working Directory
       |
       | git add
       v
   Staging Area
```
Important idea:
```text
Working Directory != Staging Area
```
Just because I changed a file does NOT automatically mean it will be part of the next commit.
---
## Repository
The repository contains Git's stored history.
Normally Git stores its internal data inside:
```text
.git/
```
Example:
```text
my-project/
│
├── main.cpp
├── README.md
│
└── .git/
```
The `.git` directory contains Git's internal information.
Conceptually:
```text
Working Directory
       |
       | git add
       v
   Staging Area
       |
       | git commit
       v
    Repository
```
---
# 3. Our MiniGit architecture
Our simplified Git may look like:
```text
Working Directory
       |
       | mygit add
       v
   Staging Area
       |
       | mygit commit
       v
   Object Store
       |
       v
    Commit
       |
       v
   Commit History
```
Eventually we want commands such as:
```bash
mygit init
# mygit -> our own Git-like program
# init  -> initialize a new MiniGit repository
```
```bash
mygit add file.txt
# add file.txt to our staging area
```
```bash
mygit status
# show which files are changed/staged/untracked
```
```bash
mygit commit -m "first commit"
# commit -> save a snapshot
# -m     -> message option
# "first commit" -> human-readable commit message
```
```bash
mygit log
# display previous commits
```
```bash
mygit branch feature
# create a branch called "feature"
```
```bash
mygit checkout feature
# move to the branch called "feature"
```
---
# 4. Why Git uses hashes
Suppose a file contains:
```text
hello
```
Git can calculate a hash from its contents.
Conceptually:
```text
"hello"
   |
   | hash function
   v
abcdef123456...
```
The hash acts like an identifier for that content.
Important idea:
```text
same content
    ->
same hash
```
If the content changes:

```text
hello
```
becomes:
```text
hello!
```
then the hash changes too.
Conceptually:
```text
hello   -> hash A
hello!  -> hash B
```
So hashes help detect whether content changed.
---
# 5. Content Addressing
Git uses a concept called **content-addressed storage**.
Instead of saying:
```text
store this object using filename "file1"
```
we can store it using the hash of its contents.
Conceptually:
```text
content
   |
   v
hash(content)
   |
   v
object identifier
```
Example:
```text
"Hello Git"
      |
      v
SHA hash
      |
      v
ab12cd34...
```
Then the object can be stored using that hash.
---
# 6. Object Store
Git stores internal objects.
Our MiniGit may eventually have something like:
```text
.mygit/
│
└── objects/
```
Conceptually:
```text
file contents
     |
     v
   hash
     |
     v
.mygit/objects/<hash>
```
This means the file content itself becomes an object.
---
# 7. Blob
A **blob** represents file contents.
Blob basically means:
```text
Binary Large Object
```
For learning purposes, think:
```text
Blob = contents of a file
```
Example:
```text
hello.txt
Hello World
```
MiniGit could create:

```text
Blob
--------------------------------
content: "Hello World"
hash: abc123...
--------------------------------
```

Important:
A blob mainly stores the contents.
It does not need to care that the original filename was:
```text
hello.txt
```
The filename can be stored somewhere else.
---

# 8. Tree

A **tree** represents directory structure.

Suppose the project is:

```text
project/
├── main.cpp
└── README.md
```

Git conceptually needs something that says:

```text
main.cpp  -> Blob A
README.md -> Blob B
```

That structure is represented using a **tree**.

Conceptually:

```text
Tree
│
├── main.cpp  -> blob abc123
└── README.md -> blob xyz789
```

So:

```text
Blob = file contents

Tree = filenames + structure + references to blobs
```

---

# 9. Commit

A commit represents a saved project snapshot.

Conceptually:

```text
Commit
│
├── tree
├── parent commit
├── author
├── timestamp
└── message
```

Example:

```text
Commit
--------------------------------
tree: abc123
parent: def456
message: "Added login system"
--------------------------------
```

Important:

The commit does not need to directly contain every file.

Instead, it can point to a tree.

```text
Commit
   |
   v
Tree
   |
   +-------> Blob
   |
   +-------> Blob
```

---

# 10. Parent Commit

Commits can point to previous commits.

Example:

```text
Commit C
   |
   v
Commit B
   |
   v
Commit A
```

This creates history.

Example:

```text
A <- B <- C
```

Where:

```text
A = first commit

B = second commit

C = latest commit
```

The latest commit points backward toward its parent.

---

# 11. Commit history is a graph

A simple linear history looks like:

```text
A <- B <- C <- D
```

But Git can have branches.

Example:

```text
        C
       /
A <- B
       \
        D
```

This is why Git history can be thought of as a graph.

More specifically, commits form a:

```text
Directed Acyclic Graph
```

Common abbreviation:

```text
DAG
```

---

# 12. Branch

A branch is easier to understand if I think of it as:

```text
a name pointing to a commit
```

Example:

```text
A <- B <- C
          ^
          |
        main
```

Here:

```text
main
```

points to commit:

```text
C
```

If a new commit D is created:

```text
A <- B <- C <- D
               ^
               |
             main
```

The branch pointer moves forward.

---

# 13. HEAD

Git also needs to know:

```text
Which branch am I currently using?
```

That is related to:

```text
HEAD
```

Conceptually:

```text
HEAD
 |
 v
main
 |
 v
Commit D
```

So:

```text
HEAD -> branch -> commit
```

We will understand this more deeply later.

---

# 14. `mygit init`

Eventually:

```bash
mygit init
```

might create something like:

```text
project/
│
├── .mygit/
│   ├── objects/
│   ├── refs/
│   ├── HEAD
│   └── index
│
└── project files
```

Meaning:

```text
objects/
# stores Git-like objects

refs/
# stores references such as branches

HEAD
# tells us which branch or commit is currently active

index
# could represent our staging area
```

This is only our simplified design.

Real Git has more details.

---

# 15. `mygit add`

Conceptually:

```bash
mygit add hello.txt
```

could mean:

```text
1. Read hello.txt
2. Calculate its hash
3. Store its contents as an object
4. Add information to the staging area
```

Flow:

```text
hello.txt
    |
    v
read contents
    |
    v
calculate hash
    |
    v
store blob
    |
    v
update staging area
```

We have NOT implemented this yet.

This is the mental model we will eventually code.

---

# 16. `mygit commit`

Conceptually:

```bash
mygit commit -m "first commit"
```

may eventually do:

```text
Staging Area
      |
      v
Create Tree
      |
      v
Create Commit
      |
      v
Store Commit Object
      |
      v
Move Branch Pointer
```

---

# 17. Full mental model so far

```text
Files
 |
 v
Working Directory
 |
 | mygit add
 v
Staging Area
 |
 | create blobs
 v
Blob Objects
 |
 | build project structure
 v
Tree Object
 |
 | mygit commit
 v
Commit Object
 |
 | references previous commit
 v
Commit History
```

---

# 18. Important objects

Remember this relationship:

```text
Blob
  =
file contents
```

```text
Tree
  =
directory structure
+
filenames
+
references to blobs/trees
```

```text
Commit
  =
snapshot metadata
+
tree reference
+
parent reference
+
message
```

```text
Branch
  =
name pointing to a commit
```

```text
HEAD
  =
what I currently have checked out
```

---

# 19. One very important Git idea

Git should not be thought of as:

```text
Version 1:
main.cpp

Version 2:
diff from main.cpp

Version 3:
another diff
```

A better beginner mental model is:

```text
Git stores snapshots.
```

Conceptually:

```text
Snapshot 1
   |
Snapshot 2
   |
Snapshot 3
```

Git can efficiently reuse unchanged objects.

Example:

```text
Commit 1
│
├── Blob A
├── Blob B
└── Blob C
```

If only one file changes:

```text
Commit 2
│
├── Blob A
├── Blob B
└── Blob D
```

The unchanged objects can still be referenced.

This is one reason content-addressed storage is powerful.

---

# 20. Commands we want MiniGit to support

```bash
mygit init
# initialize repository
```

```bash
mygit add <file>
# stage a file
```

```bash
mygit status
# inspect repository state
```

```bash
mygit commit -m "<message>"
# create a commit
```

```bash
mygit log
# display commit history
```

```bash
mygit branch <name>
# create a branch
```

```bash
mygit checkout <branch>
# switch branches
```

Later we may add:

```bash
mygit diff
# show differences
```

```bash
mygit cat-file
# inspect raw objects
```

```bash
mygit hash-object
# manually hash/store content
```

These later commands can help us understand Git internals better.

---

# 21. Concepts learned today

Today I learned the basic meaning of:

```text
Git
Working Directory
Staging Area
Repository
.git / .mygit
Hash
Content Addressing
Object Store
Blob
Tree
Commit
Parent Commit
Branch
HEAD
Commit Graph / DAG
```

---

# 22. Things I should be able to answer

### Question 1

What is the difference between the working directory and staging area?

### Question 2

Why can a hash be useful for detecting file changes?

### Question 3

What does a blob represent?

### Question 4

Why do we need a tree if blobs already contain file contents?

### Question 5

What does a commit point to?

### Question 6

What does a branch actually represent internally?

### Question 7

What is the relationship:

```text
HEAD -> branch -> commit
```

### Question 8

Why is Git called content-addressed storage?

---

# 23. Current progress

```text
[✓] Understand the purpose of Git

[✓] Working Directory

[✓] Staging Area

[✓] Repository

[✓] Basic hashing idea

[✓] Content-addressed storage

[✓] Blob concept

[✓] Tree concept

[✓] Commit concept

[✓] Parent commit concept

[✓] Branch concept

[✓] HEAD introduction

[ ] Create MiniGit repository structure

[ ] Implement hashing

[ ] Implement object storage

[ ] Implement mygit add

[ ] Implement staging area

[ ] Implement commits

[ ] Implement log

[ ] Implement branches

[ ] Implement checkout
```

---

# Next Step

Our first real coding milestone should be very small:

```bash
mygit init
```

The goal will be to understand:

```text
How does a program initialize and manage its own hidden repository directory?
```

We should first decide what files and folders our:

```text
.mygit/
```

directory actually needs.

We should NOT copy real Git blindly.

We should design the smallest structure that teaches us the concept.
