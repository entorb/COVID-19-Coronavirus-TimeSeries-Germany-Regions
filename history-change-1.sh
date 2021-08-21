#!/bun/bash
myFilePath=data/de-districts/de-district_timeseries-03353.tsv
# 02000 : Hamburg
# 09162 : München
# 09562 : Erlangen
# 03353 : Harburg

myDateToInvestigate=2021-08-12

myFileName=$(basename -- "$myFilePath")
myFileExt="${myFileName##*.}"
myFileName="${myFileName%.*}"


#
# 1. list all commits for file
#

# list all commits
myCommitLogFile=cache/history-change.tsv
mkdir -p cache/history-change
git log --no-decorate --pretty=format:"%h%x09%ad%x09%an%x09%s" --date=short -- $myFilePath > $myCommitLogFile
# --date=short : only date, not time
# --date=iso   : include time as well

# add linebreak to the end
echo "" >> $myCommitLogFile

#
# 2. revert old versions from commits
#

# loop over all commits/changes for that file
while read line ; do
    set $line
	myCommit=$1
	myDate=$2
    echo "$myCommit ; $myDate"
	# revert file from commit
	git checkout $myCommit $myFilePath
	# copy to 
	cp $myFilePath cache/history-change/${myFileName}_${myDate}.${myFileExt}
done <"$myCommitLogFile"
# rm $myCommitLogFile

# revert changes to file
# git reset -- $myFilePath
git reset -- $myFilePath
git checkout $myFilePath

#
# 3. extract data for specific date from old versions of file
# TODO: do this in Python, as the column order was changed on 2021-08-13
#
fileResults=history-change-$myFileName-$myDateToInvestigate.tsv
echo -e "filedate\t"$(head -n 1 $myFilePath | cut -f1,2,3,4,5,6,7,12) > $fileResults
grep -H "$myDateToInvestigate" cache/history-change/${myFileName}* | sed "s/cache\/history-change\/${myFileName}_//" | sed "s/.tsv:/\t/" | cut -f1,2,3,4,5,6,7,8,13 >> $fileResults