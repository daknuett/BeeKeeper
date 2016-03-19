#!/bin/bash

pyfiles=(main.py pythons/objs_model.py pythons/objs_main.py pythons/objs_graphics.py bee_util/__init__.py bee_util/queen_bee/__init__.py bee_util/queen_bee/data.py bee_util/queen_bee/calculations.py )
etcfiles=(BeeKeeperMain.glade micon.png BeeKeeperAbout.glade stock_export_dialog.glade)

dirs=(pythons/ bee_util/ bee_util/queen_bee/)
yes="j"

echo "Installing Beekeeper..."

echo "Do you want to install BeeKeeper locally(l) or globally(g) [G/l]?"
read input
if [[ "$input" == "l" ]]
then 
	echo "installing locally..."
	if [ -e ~/.BeeKeeper/ ]
	then 
		echo "Path  ~/.BeeKeeper/  exists already is BeeKeeper installed?"
		echo "Do you want to install BeeKeeper anyway?"
		echo "this will remove the current ~/.BeeKeeper."
		echo "continue installing BeeKeeper [j/N]?"
		read input
		if [[ "$input" == "$yes" ]]
		then
			rm -r ~/.BeeKeeper
			echo "continue"
		else
			echo "exiting."
			exit 1
		fi
	fi
	echo "checking for requirements..."
	python3 -c"import time;time.sleep(1)" || { echo "requirement python3 not satisfied";exit 1; }

	python3 -c"import gi.repository" || { echo "requirement gi.repository not satisfied"; exit 1; }
	python3 -c"import datetime" || { echo "requirement datetime not satisfied"; exit 1; }
	python3 -c"import pickle" || { echo "requirement pickle not satisfied"; exit 1; }

	echo "done."

	echo "touching DIR ~/.BeeKeeper ..."
	mkdir ~/.BeeKeeper
	echo "done."

	echo "touching DIR ~/.BeeKeeper/usr"
	mkdir ~/.BeeKeeper/usr
	echo "done."
	echo "touching DIR ~/.BeeKeeper/pys"
	mkdir ~/.BeeKeeper/pys
	echo "done."
	echo "touching DIR ~/.BeeKeeper/etc"
	mkdir ~/.BeeKeeper/etc
	echo "done."

	echo "creating dirs..."
	for dir in ${dirs[*]}
	do
		echo $dir
		mkdir ~/.BeeKeeper/pys/$dir
	done
	echo "done."


	echo "copying over py files ..."
	for file in ${pyfiles[*]}
	do
		echo $file
		cp $file ~/.BeeKeeper/pys/$file
	done
	echo "done."
	echo "copying over etc files ..."
	for file in ${etcfiles[*]}
	do
		echo $file
		cp etc/$file ~/.BeeKeeper/etc/$file
	done
	echo "done."

	echo "copying Executable ... "
	cp etc/BeeKeeper.local ~/.BeeKeeper/usr/BeeKeeper
	chmod +x ~/.BeeKeeper/usr/BeeKeeper
	echo "done."

	echo "extending .desktop file ..."
	cp etc/BeeKeeper.desktop.local BeeKeeper.desktop
	echo "Icon=$HOME/.BeeKeeper/etc/micon.png">>BeeKeeper.desktop
	echo "Exec=$HOME/.BeeKeeper/usr/BeeKeeper">>BeeKeeper.desktop
	echo "done."

	echo "copying .desktop file ... "
	if [ -z ~/.local/share/applications ]
	then 
		echo "~/.local/share/applications does not exist. cannot install."
		exit 1
	fi
	cp etc/BeeKeeper.desktop ~/.local/share/applications/BeeKeeper.desktop
	chmod +x ~/.local/share/applications/BeeKeeper.desktop
	rm etc/BeeKeeper.desktop
	echo "done."

	


else
	echo "installing globally..."

	if [ -e ~/.BeeKeeper/ ]
	then 
		echo "Path  ~/.BeeKeeper/  exists already is BeeKeeper installed?"
		echo "Do you want to install BeeKeeper anyway?"
		echo "continue installing BeeKeeper [j/N]?"
		read input
		if [[ "$input" == "$yes" ]]
		then
			echo "continue"
		else
			echo "exiting."
			exit 1
		fi
	fi

	echo "checking for requirements..."
	python3 -c"import time;time.sleep(1)" || { echo "requirement python3 not satisfied";exit 1; }

	python3 -c"import gi.repository" || { echo "requirement gi.repository not satisfied"; exit 1; }

	echo "done."
		

	echo "touching DIR ~/.BeeKeeper ..."
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

	echo "touching DIR /etc/BeeKeeper"
	sudo mkdir /etc/BeeKeeper
	echo "done."

	echo "creating dirs..."
	for dir in ${dirs[*]}
	do
		echo $dir
		sudo mkdir /etc/BeeKeeper/$dir
	done
	echo "done."


	echo "Copying files to /etc/BeeKeeper..."

	for file in ${pyfiles[*]}
	do
		echo $file
		sudo cp $file /etc/BeeKeeper/$file
	done
	for file in ${etcfiles[*]}
	do
		echo $file
		sudo cp etc/$file /etc/BeeKeeper/$file
	done
	echo "done."

	echo "copying file to /usr/bin"
	sudo cp etc/BeeKeeper.nonlocal /usr/bin/BeeKeeper
	echo "done."

	echo "generating executable ..."
	sudo chmod +x /usr/bin/BeeKeeper || { echo "Failed!";exit 1; }
	echo "done."

	echo "copiyng over desktop file ..."
	sudo cp etc/BeeKeeper.desktop.nonlocal /usr/share/applications/BeeKeeper.desktop
	echo "done"
fi


echo "done."
printf "BeeKeeper ready for usage.\nThank you\n"

printf "\n\n\n\n\n"

printf "Thanks to Katherina Knuettel for the Icon.\n This program is FREE Software. See the GNU AGPL v3 for more information.\nCopyright (C) 2015 Daniel Knuettel\nhttps://www.gnu.org/licenses/agpl-3.0.html\n"


printf "\n\n\n\n\n"

printf "BeeKeeper does support exporting to CSV and to XML in version 0.3!\n"
exit 0
