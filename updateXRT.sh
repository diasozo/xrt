#!/bin/bash
# This script updates the local github files by pulling the updates from the original 
# xrt location (https://github.com/kklmn/xrt.git)
echo "Pulling updates from master branch of kklm/xrt on github"
git fetch upstream
echo "Ensuring that the master branch is selected"
git checkout master
echo "adding any changes files"
git add --all
echo "Committing changes with generic message"
git commit -m "minor file changes/additions"
echo "Pushing changes to 'master' branch"
git push origin master
echo "Re-writing master branch to include updates"
git rebase upstream/master
echo "Pushing back updates to diasozo/xrt"
git push -f origin master