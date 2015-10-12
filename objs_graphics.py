from gi.repository import Gtk
import os


class ExportDialog(Gtk.Dialog):
	def __init__(self,parent,*args):
		Gtk.Dialog.__init__(self, "Exportieren", parent, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_default_size(150,150)
		self.contentarea=self.get_content_area()
		self.selection_type=""
		self.selection_folder=""
		self.combo_store=Gtk.ListStore(str)
		self.combo_store.append(["CSV"])
		self.combo_store.append(["XML"])
		self.combo=Gtk.ComboBox.new_with_model_and_entry(self.combo_store)
		self.combo.connect("changed",self.update_select_type)
		self.combo.set_entry_text_column(0)
		self.contentarea.add(self.combo)

		self.filechooser=Gtk.FileChooserButton(Gtk.FileChooserAction.SELECT_FOLDER)
		self.filechooser.connect("file-set",self.update_select_folder)
		self.contentarea.add(self.filechooser)
		self.show_all()

	def update_select_type(self,combo,*args):
		treit=combo.get_active_iter()
		if(treit == None):
			return
		self.selection_type=combo.get_model()[treit][0]
		return
	def update_select_folder(self,chooser,*args):
		self.selection_folder=chooser.get_filename()
		os.mkdir(self.selection_folder)
