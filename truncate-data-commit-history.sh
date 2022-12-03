echo NOTE: manually run the lines below one by one, and perform the manual tasks
echo this is not fully automated!!!

exit 0

#
# 0. backup original Repo!!!
#

#
# 1. Backup data to new repo
#

# create new repo at GitHub.com
https://github.com/entorb/COVID-19-Coronavirus-German-Regions-OLD-DATA-BACKUP-221203

# clone orig repo in a new dir
f:
mkdir covid
wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar

git clone git@github.com:entorb/COVID-19-Coronavirus-German-Regions.git
cp -r COVID-19-Coronavirus-German-Regions COVID-19-Coronavirus-German-Regions-OLD-DATA-BACKUP-221203
cd COVID-19-Coronavirus-German-Regions-OLD-DATA-BACKUP-221203

# modify files
sed -i -e 's/COVID-19-Coronavirus-German-Regions/COVID-19-Coronavirus-German-Regions-OLD-DATA-BACKUP-221203/g' .git/config

# removing git workflows V1
# rm -r .github/workflows
# # commit changes
# git add .
# git commit -m "deactivating workflows"
# # remove .github/workflow files from git history, since otherwise pushing will fail
# java -jar ../bfg-1.14.0.jar --delete-folders .github
# java -jar ../bfg-1.14.0.jar --delete-folders maps/out
# # cleanup git
# git reflog expire --expire=now --all && git gc --prune=now --aggressive
# fix warning: symbolic ref is dangling: refs/remotes/origin/HEAD
# rm .git/refs/remotes/origin/HEAD

# # removing git workflows V2 using git-filter-repo from https://github.com/newren/git-filter-repo
python3 ../git-filter-repo.py --prune-empty always --invert-paths --path .github --path maps/out

# in case the repo update is > 2GB, the commits need to be pushed in smaller chunks
# remote: fatal: pack exceeds maximum allowed size (2.00 GiB)

# get id of inital commit
git log --pretty=oneline --reverse | head -1
5265fb3292c3d034ebc53a88c067431c3a52a53e

# push initial commit
git push origin 5265fb3292c3d034ebc53a88c067431c3a52a53e:refs/heads/master
git log --pretty=oneline --reverse >../git-history.txt

# push other commits from git-history.txt, 250 per run,
git push origin 03d35afab4df784b6b70c5483bbd2ea2eb4909e2:master
git push origin dbeb9c0679edbd34311c9e2d10f493e36933089d:master
git push origin 5fc27cc71f4da443f5344849b52c253d9f35af7f:master
git push origin ed90dfdd33fce0f922e99e987ebb8690bd895e39:master

git push

ggf .git/config von orig Repo kopieren (und pfad anpassen, siehe oben), wenn push target fehlt

# check new Repo (files are up to date?)
https://github.com/entorb/COVID-19-Coronavirus-German-Regions-OLD-DATA-BACKUP-221203

# done

#
# 2. cleanup original data by deleting data file changes from git commit history
#

# clone orig repo in a new dir
# or use copy from above
cd ..
git clone git@github.com:entorb/COVID-19-Coronavirus-German-Regions.git
# not using --bare, since I want to remove the current files

mkdir bfg-backup-dirs

cd COVID-19-Coronavirus-German-Regions

move cache ..\bfg-backup-dirs\
move data ..\bfg-backup-dirs\
move draft ..\bfg-backup-dirs\
move maps ..\bfg-backup-dirs\
move old ..\bfg-backup-dirs\
move plots-gnuplot ..\bfg-backup-dirs\
move plots-python ..\bfg-backup-dirs\
move plots-Excel ..\bfg-backup-dirs\

git add .
git commit -m "remove data files before cleanup of git history"

python3 ../git-filter-repo.py --prune-empty always --invert-paths --path cache --path data --path draft --path maps --path old --path plots-gnuplot --path plots-python --path plots-Excel

# java -jar ../bfg-1.14.0.jar --no-blob-protection --delete-folders cache
# java -jar ../bfg-1.14.0.jar --no-blob-protection --delete-folders data
# java -jar ../bfg-1.14.0.jar --no-blob-protection --delete-folders draft
# java -jar ../bfg-1.14.0.jar --no-blob-protection --delete-folders maps
# java -jar ../bfg-1.14.0.jar --no-blob-protection --delete-folders old
# java -jar ../bfg-1.14.0.jar --no-blob-protection --delete-folders plots-gnuplot
# java -jar ../bfg-1.14.0.jar --no-blob-protection --delete-folders plots-python
# java -jar ../bfg-1.14.0.jar --no-blob-protection --delete-folders plots-Excel
# git reflog expire --expire=now --all && git gc --prune=now --aggressive

# restore dirs and files
move ..\bfg-backup-dirs\cache .\
move ..\bfg-backup-dirs\data .\
move ..\bfg-backup-dirs\draft .\
move ..\bfg-backup-dirs\maps .\
move ..\bfg-backup-dirs\old .\
move ..\bfg-backup-dirs\plots-gnuplot .\
move ..\bfg-backup-dirs\plots-python .\
move ..\bfg-backup-dirs\plots-Excel .\

git add .
git commit -m "restoring data files after cleanup"

# overwrite GitHub repo
# git push --set-upstream origin master -f

ggf .git/config von orig Repo kopieren, wenn push target fehlt

git push -f
