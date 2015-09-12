#!/bin/bash

files=(main.py objs_model.py objs_main.py BeeKeeperMain.glade icon.png )
yes="j"

echo "Installing Beekeeper..."

if [ -e ~/.BeeKeeper/ ]
then 
	echo "Path  ~/.BeeKeeper/  exists already is BeeKeeper installed?"
	echo "If you want to install BeeKeeper anyway remove ~/.BeeKeeper/"
	echo "remove ~/.BeeKeeper [j/N]?"
	read input
	if [[ "$input" == "$yes" ]]
	then
		rm -r ~/.BeeKeeper
		echo "removed ~/.BeeKeeper"
	else
		echo "exiting."
		exit 1
	fi
fi

echo "checking for requirements..."
python3 -c"import time;time.sleep(1)" || { echo "requirement python3 not satisfied";exit 1; }

python3 -c"import gi.repository" || { echo "requirement gi.repository not satisfied"; exit 1; }

echo "done."
	

echo "making DIR ~/.BeeKeeper ..."
mkdir ~/.BeeKeeper
echo "done."

echo "Copying files to ~/.BeeKeeper..."

for file in ${files[*]}
do
	echo $file
	cp $file ~/.BeeKeeper/$file
done
echo "done."

echo "copying file to /usr/bin"
sudo cp BeeKeeper /usr/bin/BeeKeeper
echo "done."

echo "generating executable ..."
sudo chmod +x /usr/bin/BeeKeeper || { echo "Failed!";exit 1; }
echo "done."


echo "done."
printf "BeeKeeper ready ror usage.\nThank you\n"

printf "Thanks to Katherina Knuettel for the Icon.\n This program is FREE Software. See the GNU AGPL v3 for more information.\nCopyright (C) 2015 Daniel Knuettel\nhttps://www.gnu.org/licenses/agpl-3.0.html\n"

exit 0
