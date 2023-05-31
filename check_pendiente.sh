#!/bin/sh
exec >scripts/check_pendiente.txt 2>&1

TODAY=`date`
echo $TODAY


/usr/bin/python3 scripts/check_pendiente.py

#echo "git add check_pendiente.txt"
/usr/bin/git add scripts/check_pendiente.txt
#echo "git commit"
/usr/bin/git commit -m "check pendiente diario"
#echo "git push"
#echo "Proceso terminado!"
/usr/bin/git push 
