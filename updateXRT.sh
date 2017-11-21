#!/bin/bash
# This script updates the local github files by pulling the updates from the original 
# xrt location (https://github.com/kklmn/xrt.git)
echo "Pulling updates from master branch of kklm/xrt on github"
git fetch upstream
echo "Ensuring that the master branch is selected"
git checkout master
echo "Re-writing master branch to include updates"
git rebase upstream/master
echo "Pushing back updates to diasozo/xrt"
git push -f origin master