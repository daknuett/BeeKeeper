import time
from gi.repository import Gtk
import datetime
import os,shutil,pickle
from objs_graphics import *
from bee_util.queen_bee import calculations as qb_calc
from bee_util.queen_bee import data as qb_data


class Spendable(object):
	pass

class Futter(Spendable):
	def __init__(self,name,menge,preis_pro_menge,datum):
		self.name=name
		self.menge=menge
		self.preis_pro_menge=preis_pro_menge
		self.datum=datum
	def __str__(self):
		s= self.name+": "+str(self.menge)+" Einheiten mit "+str(self.preis_pro_menge)+" Euro pro Einheit am "+str(self.datum)+" gefüttert"
		return s
	def __add__(self,obj):
		return self.menge*self.preis_pro_menge + obj
	def __radd__(self,obj):
		return self.menge*self.preis_pro_menge + obj

	def to_xml(self,indent=0):
		"""
			convert the object to a xml representation
			"""
		xml_str=""
		xml_str+="\t"*indent
		xml_str+='<futter name="{0}">\n'.format(self.name)
		xml_str+="\t"*(indent+1)
		xml_str+='<property name="{0}">{1}</property>\n'.format("menge",self.menge)
		xml_str+="\t"*(indent+1)
		xml_str+='<property name="{0}">{1}</property>\n'.format("preis_pro_menge",self.preis_pro_menge)
		xml_str+="\t"*(indent+1)
		xml_str+='<property name="{0}">{1}</property>\n'.format("datum",self.datum)
		xml_str+="\t"*indent
		xml_str+='</futter>\n'
		return xml_str
	def to_csv(self,separator=','):
		csv_str=""
		csv_str+="futter{0}{1}{0}{2}{0}{3}\n".format(separator,self.name,self.menge,self.preis_pro_menge)
		return csv_str


	
class Medikament(Spendable):
	def __init__(self,name,menge,preis_pro_menge,datum):
		self.name=name
		self.menge=menge/1000
		self.preis_pro_menge=preis_pro_menge
		self.datum=datum
	def __str__(self):
		s= self.name+": "+str(self.menge)+" Einheiten mit "+str(self.preis_pro_menge)+" Euro pro Einheit am "+str(self.datum)+" verabreicht"
		return s
	def __add__(self,obj):
		return self.menge*self.preis_pro_menge + obj
	def __radd__(self,obj):
		return self.menge*self.preis_pro_menge + obj
	def to_xml(self,indent=0):
		"""
			convert the object to a xml representation
			"""
		xml_str=""
		xml_str+="\t"*indent
		xml_str+='<medikament name="{0}">\n'.format(self.name)
		xml_str+="\t"*(indent+1)
		xml_str+='<property name="{0}">{1}</property>\n'.format("menge",self.menge)
		xml_str+="\t"*(indent+1)
		xml_str+='<property name="{0}">{1}</property>\n'.format("preis_pro_menge",self.preis_pro_menge)
		xml_str+="\t"*(indent+1)
		xml_str+='<property name="{0}">{1}</property>\n'.format("datum",self.datum)
		xml_str+="\t"*indent
		xml_str+='</medikament>\n'
		return xml_str
	def to_csv(self,separator=','):
		csv_str=""
		csv_str+="medikament{0}{1}{0}{2}{0}{3}\n".format(separator,self.name,self.menge,self.preis_pro_menge)
		return csv_str

class Volk(object):
	def __init__(self,name,ort,groesse):
		self.name = name
		self.ort = ort
		self.groesse = groesse
		self.futterlist = []
		self.medikamentenlist = []
		self.old_groesse = []
		self.sizes = []
		self.dead = False
		self.death_reason = ""
		self.death_date = None
		self.xml_values = {"ort":"ort",
			"groesse":"groesse",
			"tot":"dead",
			"todesursache":"death_reason",
			"sterbedatum":"death_date"}
		self.notices = []
		self.dates = []
	def __str__(self):
		return self.name+": steht in "+self.ort+" ist "+str(self.groesse)+" Rähmchen groß"
	def fuettern(self,futter):
		self.futterlist.append(futter)
	def is_dead(self):
		self.update_current_version()
		return self.dead
	def medikament_geben(self,medikament):
		self.medikamentenlist.append(medikament)
	def change_size_by_date(self,date,size):
		for futter in self.futterlist:
			if(futter.datum==datetime.datetime.strptime(date,"%d-%m-%y").date()):
				futter.menge=size
	def update_current_version(self):
		""" add missing attributes of older versions """
		if(not hasattr(self,"dead")):
			print("WARNING: adding attr <dead>")
			self.dead = False
		if(not hasattr(self,"death_reason")):
			print("WARNING: adding attr <death_reason>")
			self.death_reason = ""
		if(not hasattr(self,"death_date")):
			print("WARNING: adding attr <death_date>")
			self.death_date = None
		if(not hasattr(self,"xml_values")):
			print("WARNING: adding attr <xml_values>")
			self.xml_values = {"ort":"ort",
				"groesse":"groesse",
				"tot":"dead",
				"todesursache":"death_reason",
				"sterbedatum":"death_date"}
		if(not hasattr(self,"sizes")):
			self.old_groesse = [(datetime.datetime.today(),self.groesse)]
			self.sizes = []

	def to_xml(self,indent = 0):
		self.update_current_version()
	
		xml_str=""
		xml_str+="\t"*indent
		xml_str+='<volk name="{0}">\n'.format(self.name)
		for name,entity in self.xml_values.items():
			xml_str+="\t"*(indent+1)
			xml_str+='<property name="{0}">{1}</property>\n'.format(name,getattr(self,entity))
		for futter in self.futterlist:
			xml_str+=futter.to_xml(indent+1)
		for med in self.medikamentenlist:
			xml_str+=med.to_xml(indent+1)
		xml_str+="\t"*indent
		xml_str+="</volk>\n"
		return xml_str
	def to_csv(self,pathspec="./",separator=","):
		self.update_current_version()
		"""unlike Futter.to_csv or Medikament.to_csv this will write everyting to a file"""
		_name=pathspec+self.name.replace(" ","_")
		foods=open(_name+"_futter.csv","w")
		for futter in self.futterlist:
			foods.write(futter.to_csv(separator))
		foods.close()
		meds=open(_name+"_med.csv","w")
		for med in self.medikamentenlist:
			meds.write(med.to_csv(separator))
		meds.close()
		csv_str = "volk"
		for name,entity in self.xml_values.items():
			csv_str += '{0}{1}'.format(separator,getattr(self,entity))
		return csv_str + "\n"
	def get_header(self,separator = ","):
		csv_str = "volk"
		for name,entity in self.xml_values.items():
			csv_str += '{0}{1}'.format(separator,name)
		return csv_str + "\n"
	def add_stock(self,stock):
		self.sizes.append((datetime.datetime.today(),stock))

class Stock(object):
	def __init__(self,bees,food,brood,drone_brood):
		self.bees = bees
		self.food = food
		self.brood = brood
		self.drone_brood = brood

	
class Volksverwaltung(object):
	def __init__(self,voelker=None):
		if voelker==None:
			self.voelker=[]
		else:
			self.voelker=voelker
	def add_volk(self,volk):
		self.voelker.append(volk)
	def del_volk(self,pos):
		del(self.voelker[pos])
	def kill_volk(self,pos,reason):
		volk = self.voelker[pos]
		volk.dead = True
		volk.death_reason = reason
		volk.death_date = datetime.datetime.today()
		self.voelker[pos] = volk

	def to_xml(self,indent=0):
		xml_str=""
		xml_str+="\t"*indent
		xml_str+="<voelker>\n"
		for volk in self.voelker:
			xml_str+=volk.to_xml(indent+1)
		xml_str+="\t"*indent
		xml_str+="</voelker>\n"
		return xml_str
	def to_csv(self,pathspec="./",separator=","):
		voelker = open(pathspec + "voelker.csv","w")	
		voelker.write(self.voelker[0].get_header(separator))
		for volk in self.voelker:
			voelker.write(volk.to_csv(pathspec,separator))
		voelker.close()

class MainController(object):
	def __init__(self):
		self.t1_model = None
		self.t2_model = None
		self.t3_model = None
		self.t4_model = None
		self.t1 = None
		self.t2 = None
		self.t3 = None
		self.t4 = None
		self.add_food_button = None
		self.add_med_button = None
		self.del_button = None
		self.add_button = None
		self.food_name_ent = None
		self.food_size_ent = None
		self.food_cost_ent = None
		self.med_name_ent = None
		self.med_size_ent = None
		self.med_cost_ent = None
		self.volksverwaltung = None
		self.archived = None
		self.new_name_ent=None
		self.new_ort_ent = None
		self.new_size_ent = None


		self.stat_food_ent = None
		self.stat_med_ent = None
		self.stat_all_ent = None

		# ON STD
		self.savename = os.getenv("HOME")+"/.BeeKeeper/bees.pik"
		# ON TEST
		self.savename = "bees.pik"

	def build_t1_model(self):
		for volk in self.volksverwaltung.voelker:
			try:
				if volk.is_dead():
					continue
			except:
				pass
			self.t1_model.append((volk.name,volk.ort,volk.groesse))
	def build_t1_model_with_dead(self):
		for volk in self.volksverwaltung.voelker:
			if volk.is_dead():
				self.t1_model.append((volk.name + "  (tot)",volk.ort,volk.groesse))
			else:
				self.t1_model.append((volk.name,volk.ort,volk.groesse))

### ACTIONS ###
	def name_changed(self,widget,path,text):
		self.t1_model[path][0] = text
		self.volksverwaltung.voelker[int(path)].name = text
	def food_val_changed(self,widget,path,text):
		self.t2_model[path][2] = float(text)
		self.volksverwaltung.voelker[self.food_stats_volk_index].change_size_by_date(self.t2_model[path][3],float(self.t2_model[path][2]))
	def ort_changed(self,widget,path,text):
		self.t1_model[path][1] = text
		self.volksverwaltung.voelker[int(path)].ort = text
	def groesse_changed(self,widget,path,text):
		self.t1_model[path][2] = int(text)
		self.volksverwaltung.voelker[int(path)].old_groesse.append((datetime.datetime.today(),self.volksverwaltung.voelker[int(path)].groesse))
		self.volksverwaltung.voelker[int(path)].groesse = int(text)
	def save_and_exit(self,*args):
		pickle.dump(self.volksverwaltung,open(self.savename,"wb"))
		Gtk.main_quit(*args)
	def del_volk(self,button):
		sel = self.t1.get_selection()
		model,row = sel.get_selected()
		place = 0
		name = self.t1_model[row][0]
		for volk in self.volksverwaltung.voelker:
			if(volk.name == name):
				break
			place += 1
		del(self.volksverwaltung.voelker[place])
		del(self.t1_model[row])
	def add_volk(self,button):
		name = self.new_name_ent.get_text()
		if(name == ""):
			self.new_name_ent.set_text("Name benötigt")
		ort = self.new_ort_ent.get_text()
		if(ort==""):
			self.new_ort_ent.set_text("Ort benötigt")
		groesse_s=self.new_size_ent.get_text()
		groesse=0
		try:
			groesse=int(groesse_s)
		except:
			self.new_size_ent.set_text("Größe als Zahl angeben")
			return
		newVolk=Volk(name,ort,groesse)
		self.volksverwaltung.add_volk(newVolk)
		self.t1_model.append((newVolk.name,newVolk.ort,newVolk.groesse))
	def kill_volk(self,button):
		sel = self.t1.get_selection()
		model,row = sel.get_selected()
		place = 0
		name = self.t1_model[row][0]
		for volk in self.volksverwaltung.voelker:
			if(volk.name == name):
				break
			place += 1
		self.volksverwaltung.kill_volk(place,self.death_reason_ent.get_text())
		del(self.t1_model[row])

		

	def add_food(self,button):
		name=self.food_name_ent.get_text()
		if(name==""):
			self.food_name_ent.set_text("Name benötigt")
			return
		menge_s=self.food_size_ent.get_text()
		menge=0.0
		try:
			menge=float(menge_s)
		except:
			self.food_size_ent.set_text("Menge als Zahl angeben")
			return
		preis_s=self.food_cost_ent.get_text()
		preis=0.0
		try:
			preis=float(preis_s)
		except:
			self.food_cost_ent.set_text("Preis als Zahl angeben")
			return
		sel=self.t1.get_selection()
		model,row=sel.get_selected()
		place=0
		vname=self.t1_model[row][0]
		for volk in self.volksverwaltung.voelker:
			if(volk.name==vname):
				break
			place+=1
		self.volksverwaltung.voelker[place].fuettern(Futter(name,menge,preis,datetime.date.today()))
	def add_med(self,button):
		name=self.med_name_ent.get_text()
		if(name==""):
			self.med_name_ent.set_text("Name benötigt")
			return
		menge_s=self.med_size_ent.get_text()
		menge=0.0
		try:
			menge=float(menge_s)
		except:
			self.med_size_ent.set_text("Menge als Zahl angeben")
			return
		preis_s=self.med_cost_ent.get_text()
		preis=0.0
		try:
			preis=float(preis_s)
		except:
			self.med_cost_ent.set_text("Preis als Zahl angeben")
			return
		sel=self.t1.get_selection()
		model,row=sel.get_selected()
		place=0
		vname=self.t1_model[row][0]
		for volk in self.volksverwaltung.voelker:
			if(volk.name==vname):
				break
			place+=1
		self.volksverwaltung.voelker[place].medikament_geben(Medikament(name,menge,preis,datetime.date.today()))

	def build_food_stats(self,ent):
		self.show_food_stats(self.stat_food_ent.get_text())
	def build_med_stats(self,ent):
		self.show_med_stats(self.stat_med_ent.get_text())
	def build_all_stats(self,ent):
		self.show_all_stats(self.stat_all_ent.get_text())
	def show_all_stats(self,dfrom):
		self.t4_model=Gtk.ListStore(str,float)
		self.t4.set_model(self.t4_model)
		da=None
		try:
			da=datetime.datetime.strptime(dfrom,"%d-%m-%y").date()
			print(da)
		except BaseException as e:
			self.stat_all_ent.set_text("Datum als DD-MM-JJ angeben")
			print(e)
			return

		sel=self.t1.get_selection()
		model,row=sel.get_selected()
		place=0
		vname=None
		try:
			vname=self.t1_model[row][0]
		except:
			return
		for volk in self.volksverwaltung.voelker:
			if(volk.name==vname):
				break
			place+=1
		meds=self.volksverwaltung.voelker[place].medikamentenlist
		foods=self.volksverwaltung.voelker[place].futterlist
		stat_foods=[]
		for futter in foods:
			if(futter.datum>=da):
				stat_foods.append(futter)
		stat_meds=[]
		for med in meds:
			if(med.datum>=da):
				stat_meds.append(med)
		all_stats=stat_foods+stat_meds
		for stat in all_stats:
			self.t4_model.append((stat.name,stat.preis_pro_menge*stat.menge))
		self.t4_model.append(("ges",sum(all_stats)))

	def show_food_stats(self,dfrom):
		self.t2_model=Gtk.ListStore(str,float,float,str)
		self.t2.set_model(self.t2_model)
		da=None
		try:
			da=datetime.datetime.strptime(dfrom,"%d-%m-%y").date()
		except BaseException as e:
			self.stat_food_ent.set_text("Datum als DD-MM-JJ angeben")
			print(e)
			return

		sel = self.t1.get_selection()
		model,row = sel.get_selected()
		place = 0
		vname = None
		try:
			vname=self.t1_model[row][0]
		except Exception as e:
			print(e)
			return
		for volk in self.volksverwaltung.voelker:
			if(volk.name==vname):
				break
			place+=1
		self.food_stats_volk_index=place
		foods = self.volksverwaltung.voelker[place].futterlist
		stat_foods = []
		for futter in foods:
			if(futter.datum>=da):
				stat_foods.append(futter)
		self.stat_foods = stat_foods
		for food in stat_foods:
			self.t2_model.append((food.name,food.preis_pro_menge,food.menge,food.datum.strftime("%d-%m-%y")))
	def show_med_stats(self,dfrom):
		self.t3_model=Gtk.ListStore(str,float,float,str)
		self.t3.set_model(self.t3_model)
		da=None
		try:
			da=datetime.datetime.strptime(dfrom,"%d-%m-%y").date()
		except BaseException as e:
			self.stat_med_ent.set_text("Datum als DD-MM-JJ angeben")
			print(e)
			return

		sel=self.t1.get_selection()
		model,row=sel.get_selected()
		place=0
		vname=None
		try:
			vname=self.t1_model[row][0]
		except:
			return
		for volk in self.volksverwaltung.voelker:
			if(volk.name==vname):
				break
			place+=1
		meds=self.volksverwaltung.voelker[place].medikamentenlist
		stat_meds=[]
		for med in meds:
			if(med.datum>=da):
				stat_meds.append(med)
		for med in stat_meds:
			self.t3_model.append((med.name,med.preis_pro_menge,med.menge,med.datum.strftime("%d-%m-%y")))
		return

	def make_backup(self,*args):
		chooser=Gtk.FileChooserDialog("Backupdatei wählen",self.window,Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
		response=chooser.run()
		if(response==Gtk.ResponseType.OK):
			fname=chooser.get_filename()
			pickle.dump(self.volksverwaltung,open(fname,"wb"))
		chooser.destroy()
	def import_from_file(self,*args):
		chooser=Gtk.FileChooserDialog("Backupdatei zum Import wählen",self.window,Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
		response = chooser.run()
		if(response == Gtk.ResponseType.OK):
			fname = chooser.get_filename()
			try:
				volksverwaltung = pickle.load(open(fname,"rb"))
				self.volksverwaltung = volksverwaltung
			except Exception as e:
				print(e)
			self.t1_model = Gtk.ListStore(str,str,int)
			t1.set_model(self.t1_model)
			self.build_t1_model()

		chooser.destroy()
		self.load_volksverwaltung()
	def export_data(self,*args):
		dialog=ExportDialog(self.window)
		response=dialog.run()
		if(response!=Gtk.ResponseType.OK):
			dialog.destroy()
			return
		todo_export=dialog.selection_type
		if(todo_export=="CSV"):
			self.volksverwaltung.to_csv(pathspec=dialog.selection_folder+"/")
		else:
			txt=self.volksverwaltung.to_xml()
			f=open(dialog.selection_folder+"/export-"+str(int(time.time()))+".xml","w")
			f.write(txt)
			f.close()
		dialog.destroy()





	def build_from_builder(self,b):
		self.window = b.get_object("window1")
		self.add_food_button = b.get_object("button1")
		self.add_med_button = b.get_object("button2")
		self.del_button = b.get_object("button3")
		self.add_button = b.get_object("button4")
		self.build_treeview1(b.get_object("treeview1"))
		self.build_treeview2(b.get_object("treeview2"))
		self.build_treeview3(b.get_object("treeview3"))
		self.build_treeview4(b.get_object("treeview4"))
		self.food_name_ent = b.get_object("entry1")
		self.food_size_ent = b.get_object("entry2")
		self.food_cost_ent = b.get_object("entry3")
		self.med_name_ent = b.get_object("entry4")
		self.med_size_ent = b.get_object("entry5")
		self.med_cost_ent = b.get_object("entry6")
		self.new_name_ent = b.get_object("entry7")
		self.new_ort_ent =  b.get_object("entry8")
		self.new_size_ent = b.get_object("entry9")

		self.stat_food_ent = b.get_object("entry10")
		self.stat_med_ent = b.get_object("entry11")
		self.stat_all_ent = b.get_object("entry12")

		self.death_reason_ent = b.get_object("entry13")
		self.kill_volk_button = b.get_object("button5")

		self.stat_food_ent.connect("activate",self.build_food_stats)
		self.stat_med_ent.connect("activate",self.build_med_stats)
		self.stat_all_ent.connect("activate",self.build_all_stats)

		self.del_button.connect("clicked",self.del_volk)
		self.add_button.connect("clicked",self.add_volk)
		self.add_food_button.connect("clicked",self.add_food)
		self.add_med_button.connect("clicked",self.add_med)

		b.get_object("imagemenuitem4").connect("activate",self.make_backup)
		b.get_object("imagemenuitem2").connect("activate",self.import_from_file)
		b.get_object("imagemenuitem11").connect("activate",self.export_data)

		self.kill_volk_button.connect("clicked",self.kill_volk)

		queen_bee_color_this_year = b.get_object("queen_bee_color_this_year")
		queen_bee_year_select = b.get_object("queen_bee_year_select")
		queen_bee_color_of_year = b.get_object("queen_bee_color_of_year")
		queen_bee_color_select = b.get_object("queen_bee_color_select")
		queen_bee_last_year = b.get_object("queen_bee_last_year")
		self.information_controller = InformationController(queen_bee_color_this_year,
				queen_bee_year_select,
				queen_bee_color_of_year,
				queen_bee_color_select,
				queen_bee_last_year)
		self.information_controller.__start__()




	def build_treeview1(self,treeview):
		global t1_model
		t1_renderer1 = Gtk.CellRendererText(editable=True)
		t1_renderer2 = Gtk.CellRendererText(editable=True)
		t1_renderer3 = Gtk.CellRendererText(editable=True)

		t1_renderer1.connect("edited",self.name_changed)
		t1_renderer2.connect("edited",self.ort_changed)
		t1_renderer3.connect("edited",self.groesse_changed)

		t1_col1=Gtk.TreeViewColumn("Name",t1_renderer1,text=0)
		t1_col2=Gtk.TreeViewColumn("Ort",t1_renderer2,text=1)
		t1_col3=Gtk.TreeViewColumn("Größe in Rähmchen",t1_renderer3,text=2)

		t1_model=Gtk.ListStore(str,str,int)

		treeview.append_column(t1_col1)
		treeview.append_column(t1_col2)
		treeview.append_column(t1_col3)

		self.t1_model= t1_model
		treeview.set_model(t1_model)
		self.t1=treeview
		if(self.volksverwaltung != None):
			self.build_t1_model()
	def build_treeview2(self,treeview):
		t2_renderer1=Gtk.CellRendererText()
		t2_renderer2=Gtk.CellRendererText()
		t2_renderer3=Gtk.CellRendererText(editable=True)
		t2_renderer4=Gtk.CellRendererText()

		t2_renderer3.connect("edited",self.food_val_changed)

		t2_col1=Gtk.TreeViewColumn("Posten",t2_renderer1,text=0)
		t2_col2=Gtk.TreeViewColumn("Preis",t2_renderer2,text=1)
		t2_col3=Gtk.TreeViewColumn("Menge",t2_renderer3,text=2)
		t2_col4=Gtk.TreeViewColumn("Datum",t2_renderer4,text=3)

		treeview.append_column(t2_col1)
		treeview.append_column(t2_col2)
		treeview.append_column(t2_col3)
		treeview.append_column(t2_col4)

		t2_model=Gtk.ListStore(str,float,float,str)
		treeview.set_model(t2_model)
		self.t2=treeview
		self.t2_model= t2_model
	def build_treeview3(self,treeview):

		t3_renderer1=Gtk.CellRendererText()
		t3_renderer2=Gtk.CellRendererText()
		t3_renderer3=Gtk.CellRendererText()
		t3_renderer4=Gtk.CellRendererText()

		t3_col1=Gtk.TreeViewColumn("Posten",t3_renderer1,text=0)
		t3_col2=Gtk.TreeViewColumn("Preis",t3_renderer2,text=1)
		t3_col3=Gtk.TreeViewColumn("Menge",t3_renderer3,text=2)
		t3_col4=Gtk.TreeViewColumn("Datum",t3_renderer4,text=3)

		treeview.append_column(t3_col1)
		treeview.append_column(t3_col2)
		treeview.append_column(t3_col3)
		treeview.append_column(t3_col4)

		t3_model=Gtk.ListStore(str,float,float,str)
		treeview.set_model(t3_model)
		self.t3=treeview
		self.t3_model= t3_model
	def build_treeview4(self,treeview):
		t4_renderer1=Gtk.CellRendererText()
		t4_renderer2=Gtk.CellRendererText()

		t4_col1=Gtk.TreeViewColumn("Posten",t4_renderer1,text=0)
		t4_col2=Gtk.TreeViewColumn("Preis",t4_renderer2,text=1)

		treeview.append_column(t4_col1)
		treeview.append_column(t4_col2)

		t4_model=Gtk.ListStore(str,int)
		treeview.set_model(t4_model)
		self.t4=treeview
		self.t4_model= t4_model
	def load_volksverwaltung(self):
		volksverwaltung=None
		try:
			volksverwaltung=pickle.load(open(self.savename,"rb"))
		except BaseException as e:
			print(e)
		if(volksverwaltung==None):
			volksverwaltung=Volksverwaltung()
			volksverwaltung.add_volk(Volk("TestVolk","Haus",10))
		self.volksverwaltung= volksverwaltung
		

class InformationController(object):
	def __init__(self,queen_bee_color_this_year_label,
			queen_bee_year_select_spin_button,
			queen_bee_color_of_year_label,
			queen_bee_color_select_combo,
			queen_bee_last_year_label):
		self.queen_bee_color_this_year_label = queen_bee_color_this_year_label
		self.queen_bee_year_select_spin_button = queen_bee_year_select_spin_button
		self.queen_bee_color_of_year_label = queen_bee_color_of_year_label
		self.queen_bee_color_select_combo = queen_bee_color_select_combo
		self.queen_bee_last_year_label = queen_bee_last_year_label

	def __start__(self):
		self.queen_bee_color_this_year_label.set_text(qb_calc.get_current_color())
		
		
		self.color_select_model = Gtk.ListStore(str)
		renderer_text = Gtk.CellRendererText()
		self.queen_bee_color_select_combo.set_model(self.color_select_model)
		self.queen_bee_color_select_combo.set_entry_text_column(0)
		self.queen_bee_color_select_combo.connect("changed",self.set_new_year_by_color)
		for k,v in qb_data.color_de.items():
			self.color_select_model.append([v])

		self.queen_bee_color_select_combo.pack_start(renderer_text,True)
		self.queen_bee_color_select_combo.add_attribute(renderer_text, "text", 0)


		self.queen_bee_year_select_spin_button.set_numeric(True)
		self.queen_bee_year_select_spin_button.set_range(1990,3000)
		self.queen_bee_year_select_spin_button.set_value(datetime.datetime.today().year)
		self.queen_bee_year_select_spin_button.connect("value-changed",self.set_new_color_by_year)

	def set_new_year_by_color(self,combo):
		tree_iter = combo.get_active_iter()
		if(tree_iter == None):
			return
		color = self.color_select_model[tree_iter][0]
		self.queen_bee_last_year_label.set_text(str(qb_calc.last_year_from_color(color)))
	def set_new_color_by_year(self,button):
		year = int(button.get_value())
		self.queen_bee_color_of_year_label.set_text(qb_calc.color_from_year(year))

class ExtraDataController(object):
	def __init__(self):
		pass
