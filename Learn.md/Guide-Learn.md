# MiniGit Learning Log — 30 Sep 2026

## Today's goal

Learn the core ideas behind Git by designing a deliberately small version: **MiniGit**. We are learning how Git thinks before writing its implementation.

## What problem does Git solve?

When a project changes over time, Git helps us:

- save meaningful snapshots of the project;
- see what changed between snapshots;
- return to an earlier snapshot if needed;
- work on separate ideas without mixing them together; and
- share a history of work with other people.

Git does not simply copy every file on every save. It stores objects efficiently and connects them into a history.

## The three places Git tracks

| Place | Plain-English meaning | Why it exists |
|---|---|---|
| **Working directory** | The files currently visible and editable on the computer. | This is where we make changes. |
| **Staging area** | A proposed list of changes for the next snapshot. | It lets us choose exactly what belongs in one commit. |
| **Repository** | The saved project history and Git metadata. | It keeps permanent snapshots and their relationships. |

Think of a commit like mailing a package:

1. Edit items on your desk = working directory.
2. Put selected items in the box = staging area.
3. Seal, label, and store the box = repository commit.

## MiniGit

Our MiniGit will mirror a few essential Git ideas:

```text
# Files you edit live in the working directory.
working-directory/

# MiniGit's hidden data folder stores its history and objects.
.minigit/
  objects/       # Content-addressed saved objects: blobs, trees, and commits.
  index          # The staging area: what the next commit should include.
  HEAD           # A pointer to the currently checked-out branch or commit.
  refs/          # Named pointers, such as branches.
```

This is an **illustrative layout**, not implementation code.

## Hashes and content addressing

A **hash** is a deterministic, fixed-size fingerprint calculated from content.

```text
# Illustrative only: changing the content produces a different hash.
"Hello, MiniGit"  ->  a1b2c3...

# The arrow means "is transformed into" for this example.
# a1b2c3... stands for a much longer hash value.
```

MiniGit uses **content addressing**: it can name saved content by its hash rather than by a generated number.

Why this matters:

- identical content gets the same hash, so it need not be stored twice;
- changing even a small part of the content changes its identity;
- an object can refer to another object by its hash.

## Core MiniGit objects

### Blob

A **blob** stores the contents of one file. It does not remember the filename; a tree handles names.

```text
# Illustrative relationship.
README.md  ->  blob hash

# README.md is the file's name in a project tree.
# blob hash identifies the stored file content.
```

### Tree

A **tree** represents a directory snapshot. It maps filenames to blobs (and subdirectories to other trees).

```text
# Illustrative tree entries.
README.md  ->  blob: a1b2c3...
src/       ->  tree: d4e5f6...

# blob: says that README.md points to file content.
# tree: says that src/ points to another directory snapshot.
```

### Commit

A **commit** records a complete project snapshot by pointing to a tree, plus useful history information.

```text
# Illustrative commit fields.
tree    d4e5f6...       # The root directory snapshot for this commit.
parent  9a8b7c...       # The commit immediately before this one.
message "Add README"    # A human explanation of this snapshot.

# The first commit has no parent because there is no earlier snapshot.
```

### Parents and history

Most commits have one **parent**: the commit that came directly before them. Following parent pointers backwards creates project history.

```text
# Each arrow means "this newer commit points to its parent".
C3 -> C2 -> C1

# C3 is newest; C1 is oldest.
```

### Branches

A **branch** is a readable name that points to a commit. As new commits are made on that branch, its pointer moves forward.

```text
# Illustrative branch pointer.
main -> C3

# main is the branch name.
# C3 is the latest commit on that branch in this example.
```

## Example MiniGit commands

These are **illustrative command examples**. They describe the intended MiniGit interface; they are not implementation code.

### Start a repository

```sh
minigit init
# minigit: our learning project's command-line program.
# init: initialize MiniGit metadata in the current project folder.
```

### Stage a file

```sh
minigit add README.md
# minigit: the MiniGit command-line program.
# add: place a file's current version into the staging area.
# README.md: the path of the file being staged.
```

### See the current state

```sh
minigit status
# minigit: the MiniGit command-line program.
# status: report changed, staged, and untracked files.
```

### Save a snapshot

```sh
minigit commit -m "Add project README"
# minigit: the MiniGit command-line program.
# commit: save the staged changes as a new repository snapshot.
# -m: provide the commit message directly in the command.
# "Add project README": the message describing this snapshot.
```

### View history

```sh
minigit log
# minigit: the MiniGit command-line program.
# log: display commits by following parent links from the latest commit.
```

### Create a branch

```sh
minigit branch feature-notes
# minigit: the MiniGit command-line program.
# branch: create a named pointer to the current commit.
# feature-notes: the new branch name.
```

### Switch branches

```sh
minigit checkout feature-notes
# minigit: the MiniGit command-line program.
# checkout: switch the working directory and HEAD to another branch or commit.
# feature-notes: the branch to switch to.
```

## Key takeaway

MiniGit is a small system of saved objects and pointers:

```text
# A commit names a tree; a tree names files; a branch names a commit.
branch -> commit -> tree -> blobs

# Each arrow means "points to by hash or reference."
```

Next, we can turn these concepts into a first small feature, one piece at a time.
