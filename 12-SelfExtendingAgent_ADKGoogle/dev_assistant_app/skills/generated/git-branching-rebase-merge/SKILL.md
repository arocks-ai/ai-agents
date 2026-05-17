---
name: git-branching-rebase-merge
description: >
  Technical reference for Git branching strategies, specifically when to use rebase instead of merge. Use when the user asks about Git workflows, history management, or integrating changes.
metadata:
  version: '1.0'
  author: dev-assistant
---

## 1. Executive Summary
Git branching strategies involve decisions on how to integrate changes from one branch into another, primarily through merging or rebasing. Merging integrates changes by creating a new "merge commit" that combines the histories of two branches, preserving the original commit history. Rebasing, on the other hand, rewrites the commit history of a feature branch by moving its base to the tip of another branch, resulting in a linear history. The choice between rebase and merge depends on factors like team collaboration, desired history cleanliness, and whether commits have been pushed to a shared remote repository.

## 2. Technical Concepts & Architecture
**Merge:**
When you merge a branch (e.g., `feature`) into another (e.g., `master`), Git creates a new commit (a merge commit) that has two parent commits: the last commit of `feature` and the last commit of `master`. This preserves the exact history of both branches, showing where and when the branches diverged and were brought back together.

Before merge/rebase:
```
A <- B <- C [master]
^    \
 D <- E [branch]
```

After `git merge master` (from `branch`):
```
A <- B <- C
^    ^    \
 D <- E <- F [branch, master] (F is the merge commit)
```

**Rebase:**
Rebasing takes a series of commits from your current branch and reapplies them one by one onto a new base commit. This effectively rewrites the project history, making it appear as if all the changes on your feature branch were made directly on top of the target branch. This results in a cleaner, linear history without merge commits.

Before merge/rebase:
```
A <- B <- C [master]
^    \
 D <- E [branch]
```

After `git rebase master` (from `branch`):
```
A <- B <- C <- D' <- E' [branch]
```
(D' and E' are new commits with the same changes as D and E but new commit IDs, based on C)

## 3. Implementation & Quick Reference

| Command | Description | When to Use |
|---|---|---|
| `git merge <branch>` | Integrates changes from `<branch>` into the current branch by creating a new merge commit. | When integrating a feature branch into a shared main branch, or when preserving exact history is crucial. |
| `git rebase <base-branch>` | Reapplies commits from the current branch onto the `<base-branch>`, rewriting history. | To keep a feature branch up-to-date with the main branch, or to clean up local commits before pushing. |
| `git rebase -i <commit-hash>` | Interactive rebase. Allows editing, squashing, reordering, or dropping commits. | To clean up a local branch's history before merging or pushing, making it more readable. |

## 4. Practical Examples

**Example 1: Merging a feature branch into master**

```bash
# Assume you are on the 'master' branch
git checkout master
git pull origin master # Ensure master is up-to-date

# Switch to your feature branch
git checkout my-feature-branch

# Make sure your feature branch is up-to-date with master (optional, but good practice)
git merge master # This will create a merge commit on your feature branch if there are conflicts

# Switch back to master and merge the feature branch
git checkout master
git merge my-feature-branch --no-ff # --no-ff ensures a merge commit is always created
git push origin master
```

**Example 2: Rebasing a feature branch onto master**

```bash
# Assume you are on your 'my-feature-branch'
git checkout my-feature-branch

# Ensure master is up-to-date
git fetch origin
git rebase origin/master # Rebase your feature branch onto the latest master

# Resolve any conflicts that arise during the rebase
# After resolving, use:
# git add .
# git rebase --continue

# Once rebase is complete, you can push (force push if already pushed, but be careful!)
# git push origin my-feature-branch --force-with-lease
```

**Example 3: Interactive Rebase to clean up commits**

```bash
# Assume you are on your 'my-feature-branch' and want to clean up the last 3 commits
git checkout my-feature-branch
git rebase -i HEAD~3 # Opens an editor with the last 3 commits

# In the editor, change 'pick' to 'squash' for commits you want to combine,
# or 'reword' to change commit messages, 'drop' to remove commits.
# Save and close the editor.

# Git will then apply your changes. If squashing, it will prompt for a new commit message.
# After cleaning up, you might need to force push if the branch was already remote.
# git push origin my-feature-branch --force-with-lease
```

## 5. Performance & Best Practices

*   **Rebase for local branches:** It is generally recommended to rebase your *local* feature branches onto the main development branch (e.g., `master` or `develop`) to keep your history clean and linear before merging. This makes the project history easier to read and understand.
*   **Merge for shared branches:** Once a branch has been pushed to a shared remote repository and other developers might have based their work on it, you should **never rebase it**. Rebasing a shared branch rewrites history, which can cause significant problems for collaborators who have based their work on the old history. In such cases, merging is the safe option.
*   **"Golden Rule of Rebase":** Do not rebase commits that exist outside your repository and that people might have based their work on. If you have to, communicate clearly with your team.
*   **Squash commits:** Use interactive rebase (`git rebase -i`) to squash small, incremental, or "fixup" commits into more meaningful, atomic commits before merging into a main branch. This keeps the main branch history clean and focused.
*   **Test after rebase:** Since rebasing rewrites history, it's crucial to thoroughly test your code after a rebase to ensure no regressions were introduced, especially if conflicts were resolved.

## 6. Diagnosis & Troubleshooting

*   **Merge Conflicts:** Both merging and rebasing can lead to merge conflicts when the same lines of code have been changed differently in the branches being combined.
    *   **Resolution:** Git will pause the operation and mark the conflicting files. You need to manually edit the files to resolve the conflicts, `git add` the resolved files, and then `git commit` (for merge) or `git rebase --continue` (for rebase).
*   **Lost Commits after Rebase:** If you rebase and then realize you made a mistake or lost commits, you can often recover them using `git reflog`. The reflog keeps a history of where your HEAD has been.
*   **Force Push Issues:** If you rebase a branch that has already been pushed to a remote, you will need to force push (`git push --force` or `git push --force-with-lease`). Force pushing can overwrite history on the remote, potentially causing issues for collaborators. Always use `git push --force-with-lease` as it's safer, preventing you from overwriting work that someone else has pushed in the meantime.
*   **Confusing History after Rebase:** If not done carefully, frequent rebasing or rebasing shared branches can lead to a confusing and difficult-to-follow history for team members. Ensure team agreement on branching and merging strategies.
