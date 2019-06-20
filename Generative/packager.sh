#!/bin/sh

mkdir demo
python "$@"

echo 'Enter Name for Output Archive: '
read fname

zip -r --encrypt $fname demo/
ls demo/ | while read n; do rm demo/$n; done; rmdir demo/; clear

git add $fname; git commit -m 'Automated Commit'; git push origin
#EOF
