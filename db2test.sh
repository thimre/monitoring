#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Pass only one arguement, the DB name"
    exit 3
fi

dbName=$1

scriptFullPath=$(readlink -f "$0")
runningProcesses=$(ps -ef | grep $scriptFullPath | grep $dbName)
numberOfRunningProcesses=$(echo $runningProcesses | wc -l)

if [[ $numberOfRunningProcesses -gt 1 ]]
then
  echo "Previous process stucked."
  exit 1
fi

# test if connection timeout occurs in timeoutSec seconds
timeoutSec=20

connectOutput=$(timeout ${timeoutSec}s bash -c "db2 connect to $dbName user db2user using db2user; db2 ping $dbName 10; db2 connect reset")

if [ "$?" -eq 124 ]; then
  echo "Timeout db2 connect to $dbName. Tried for ${timeoutSec} sec."
  exit 2
fi

##db2 connect to $dbName user db2user using db2user
##db2 ping $dbName 10
##elapsedTime=$(db2 ping $dbName 10)
##db2 connect reset

replyTimes=$(echo "$connectOutput" | grep "Elapsed time" | grep -o -E '[0-9]+')
#echo "$replyTimes"

x=0
for i in $replyTimes
do
  x=$(($x+$i))
done
x=$(($x/10))

echo "$dbName db2 ping has $x ms avarage response time."
exit 0
