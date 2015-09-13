#!/bin/bash

files=(main.py objs_model.py objs_main.py BeeKeeperMain.glade micon.png )
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

if [ -e /etc/BeeKeeper ]
then
	echo "Path  /etc/BeeKeeper/  exists already is BeeKeeper installed?"
	echo "If you want to install BeeKeeper anyway remove /etc/BeeKeeper/"
	echo "remove /etc/BeeKeeper [j/N]?"
	read input
	if [[ "$input" == "$yes" ]]
	then
		sudo rm -r /etc/BeeKeeper
	else
		exit 1
	fi
fi

echo "making DIR /etc/BeeKeeper"
sudo mkdir /etc/BeeKeeper
echo "done."


echo "Copying files to /etc/BeeKeeper..."

for file in ${files[*]}
do
	echo $file
	sudo cp $file /etc/BeeKeeper/$file
done
echo "done."

echo "copying file to /usr/bin"
sudo cp BeeKeeper /usr/bin/BeeKeeper
echo "done."

echo "generating executable ..."
sudo chmod +x /usr/bin/BeeKeeper || { echo "Failed!";exit 1; }
echo "done."

echo "copiyng over desktop file ..."
sudo cp BeeKeeper.desktop /usr/share/applications
echo "done"


echo "done."
printf "BeeKeeper ready ror usage.\nThank you\n"

printf "Thanks to Katherina Knuettel for the Icon.\n This program is FREE Software. See the GNU AGPL v3 for more information.\nCopyright (C) 2015 Daniel Knuettel\nhttps://www.gnu.org/licenses/agpl-3.0.html\n"

exit 0
