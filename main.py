from gi.repository import Gtk
from objs_main import *
from objs_model import *
import pickle
import os

if(not os.path.exists(os.getenv("HOME")+"/.BeeKeeper")):
	print("~/.BeeKeeper does not exist, generating it")
	os.mkdir(os.path.expanduser("~/.BeeKeeper"),mode=0o755)


builder=Gtk.Builder()
builder.add_from_file("/etc/BeeKeeper/BeeKeeperMain.glade")
w=builder.get_object("applicationwindow1")


maincontroller=MainController()
maincontroller.load_volksverwaltung()
maincontroller.build_from_builder(builder)


w.show_all()
w.connect("delete-event", maincontroller.save_and_exit)
Gtk.main()


