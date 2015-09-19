from gi.repository import Gtk
from objs_main import *
from objs_model import *
import pickle
import os

def show_about():
	global builder
	about=builder.get_object("aboutdialog1")
	about.show_all()

if(not os.path.exists(os.getenv("HOME")+"/.BeeKeeper")):
	print("~/.BeeKeeper does not exist, generating it")
	os.mkdir(os.path.expanduser("~/.BeeKeeper"),mode=0o755)


builder=Gtk.Builder()
if( not sys.argv[1]=="--local"):
	builder.add_from_file("/etc/BeeKeeper/BeeKeeperMain.glade")
else:
	builder.add_from_file("~/.BeeKeeper/etc/BeeKeeperMain.glade")

w=builder.get_object("applicationwindow1")


maincontroller=MainController()
maincontroller.load_volksverwaltung()
maincontroller.build_from_builder(builder)


w.show_all()
w.connect("delete-event", maincontroller.save_and_exit)
Gtk.main()


