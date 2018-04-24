This is a test.

Keatoooooooooooooooon wuz heerrre


git commands:
navigate to tailgunner file
git init (initialize local github repository)
git status (show every file you have changed relative to your current branch)
git add filename (do this for every file you've changed, and want to commit)
git commit -m “yournamefortheupdate” (commit said changes to your local branch)
git push origin nameofbranch (updates the shared branch on GitHub, so it is the same as your local branch)
git pull origin nameofbranch (updates your local branch, so it is the same as the shared branch on GitHub)

git branch (shows all local branches on your computer, * next to the branch you are currently on)
git checkout -b “nameofbranch” (creates a new local branch, that is initially a copy of whatever local branch you are currently on)
git push --set-upstream origin "nameofbranch" (creates a copy your branch on GitHub, so you can push and pull updates to/from GitHub)

git checkout "nameofbranch" (switches to the named local branch)
git checkout -f "nameofbranch" (discards all non-commited changes, and then switches to the named local branch)

To obtain a local copy of a branch that is shared on github:
git fetch
git checkout branchnamehere
