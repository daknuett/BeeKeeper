from gi.repository import Gtk
from objs_main import *
from objs_model import *
import pickle

builder=Gtk.Builder()
builder.add_from_file("BeeKeeperMain.glade")
w=builder.get_object("applicationwindow1")


maincontroller=MainController()
maincontroller.load_volksverwaltung()
maincontroller.build_from_builder(builder)


w.show_all()
w.connect("delete-event", maincontroller.save_and_exit)
Gtk.main()


