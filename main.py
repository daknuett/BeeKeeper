from gi.repository import Gtk
from objs_main import *
from objs_model import *
import pickle
import os

def show_about(*args):
	about_builder=Gtk.Builder()
	about_builder.add_from_file("./BeeKeeperAbout.glade")
	about=about_builder.get_object("aboutdialog1")
	about.show_all()

if(not os.path.exists(os.getenv("HOME")+"/.BeeKeeper")):
	print("~/.BeeKeeper does not exist, generating it")
	os.mkdir(os.path.expanduser("~/.BeeKeeper"),mode=0o755)


builder=Gtk.Builder()
builder.add_from_file("/etc/BeeKeeper/BeeKeeperMain.glade")
w=builder.get_object("applicationwindow1")

abm=builder.get_object("menu3")
if (abm ==None):
	print(abm)
else:
	abd=Gtk.ImageMenuItem(label="_Über",use_underline=True)
	abd.connect("activate",show_about)
	abm.append(abd)

maincontroller=MainController()
maincontroller.load_volksverwaltung()
maincontroller.build_from_builder(builder)

w.show_all()
w.connect("delete-event", maincontroller.save_and_exit)
Gtk.main()


