@echo off
echo Commit all your pending changes
pause
REM Remove everything from the git index in order to refresh your git repository:
git rm -r --cached .
REM Add everything back into the repo:
git add .
REM Commit these changes:
git commit -m ".gitignore re-applied"