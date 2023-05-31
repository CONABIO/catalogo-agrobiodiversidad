#!/bin/sh
exec >scripts/check_sinonimos.txt 2>&1

TODAY=`date`
echo $TODAY


/usr/bin/python3 scripts/check_sinonimos.py
/usr/bin/python3 scripts/correo_adjunto.py
#echo "git add check_sinonimos.txt"
/usr/bin/git add scripts/check_sinonimos.txt
#echo "git commit"
/usr/bin/git commit -m "check sinonimos diario"
#echo "git push"
#echo "Proceso terminado!"
/usr/bin/git push 
