import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
import threading
import os
from TarFile import TarFile


class Installation(Gtk.Assistant):

    def __init__(self):
        Gtk.Assistant.__init__(self)
        self.connect("delete-event",Gtk.main_quit)
        self.connect("cancel", self.on_cancel_clicked)
        self.connect("close", self.on_close_clicked)
        self.connect("apply", self.on_apply_clicked)
        self.set_default_size(720,460)
        self.set_resizable(False)

        ## Giris Ekranı

        box=Gtk.Box()
        label=Gtk.Label(label="Welcome to installation. This program an example for assistan widget and setup tools")
        label.set_line_wrap(True)
        self.append_page(box)
        self.set_page_title(box,"Introduction")
        self.set_page_type(box,Gtk.AssistantPageType.INTRO)
        box.pack_start(label,True,False,0)
        self.set_page_complete(box,True)

        ## Sözleşme Ekranı

        self.box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=5)
        self.append_page(self.box)
        self.set_page_type(self.box, Gtk.AssistantPageType.CONTENT)
        self.set_page_title(self.box, "Agreement")

        scrolled=Gtk.ScrolledWindow()
        scrolled.set_border_width(5)
        scrolled.set_min_content_height(300)
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC)

        text=open('Aggrement/agg','r')
        label=Gtk.Label(label=text.read())
        text.close()

        label.set_line_wrap(True)
        scrolled.add_with_viewport(label)

        checkbutton = Gtk.CheckButton(label="Sözleşmeyi okuduğumu ve imzaladığımı kabul ediyorum")
        checkbutton.connect("toggled", self.on_accept_aggrement)
        self.box.pack_start(scrolled,True,True,0)
        self.box.pack_start(checkbutton,True,True,0)

        ## Kurulacak modullerin seçimi

        self.box_module=Gtk.Box()
        self.append_page(self.box_module)
        self.set_page_title(self.box_module,"Module Selection")
        self.set_page_type(self.box_module,Gtk.AssistantPageType.CONTENT)
        list_zip=os.listdir("Zips/")

        self.liststoremodules=Gtk.ListStore(str,bool)

        for i in range(len(list_zip)) :
            self.liststoremodules.append([list_zip[i],False])

        treeviewmodule=Gtk.TreeView()
        treeviewmodule.set_model(self.liststoremodules)

        cellrenderertext=Gtk.CellRendererText()
        cellrenderertoggle=Gtk.CellRendererToggle()
        cellrenderertoggle.connect("toggled",self.toggled_module)

        treeviewcolumn=Gtk.TreeViewColumn("Module Name")
        treeviewcolumn.pack_start(cellrenderertext,False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 0)
        treeviewmodule.append_column(treeviewcolumn)

        treeviewcolumn=Gtk.TreeViewColumn("Status")
        treeviewcolumn.pack_start(cellrenderertoggle,False)
        treeviewcolumn.add_attribute(cellrenderertoggle,"active",1)
        treeviewmodule.append_column(treeviewcolumn)

        self.box_module.pack_start(treeviewmodule,True,True,0)

        ## Destination Directory

        self.box2=Gtk.Box()
        self.append_page(self.box2)

        grid=Gtk.Grid()
        self.box2.pack_start(grid,True,True,0)

        self.set_page_title(self.box2, "Select Destination Directory")
        self.set_page_type(self.box2, Gtk.AssistantPageType.CONTENT)

        filechooserbutton=Gtk.FileChooserButton(title="Select Destination File")
        filechooserbutton.set_action(2)                                           ## Sadece dizin seçebilmeye ayarladık
        filechooserbutton.connect("file-set",self.on_select_file)

        label=Gtk.Label(label="Please select your destination directory!")
        label.set_halign(Gtk.Align.CENTER)
        label.set_line_wrap(True)
        grid.set_row_homogeneous(False)
        grid.add(label)
        grid.attach_next_to(filechooserbutton,label,Gtk.PositionType.BOTTOM,1,1)

        ## Onay Sayfası

        box=Gtk.VBox(spacing=0)
        self.append_page(box)
        self.set_page_title(box,"Verification")
        self.set_page_type(box,Gtk.AssistantPageType.CONFIRM)

        self.liststorechoosen=Gtk.ListStore(str)

        self.treeviewchoosen=Gtk.TreeView()
        self.treeviewchoosen.set_model(self.liststorechoosen)

        cellrenderertext=Gtk.CellRendererText()

        treeviewcolumn=Gtk.TreeViewColumn("Modules to Install")
        treeviewcolumn.pack_start(cellrenderertext,True)
        treeviewcolumn.add_attribute(cellrenderertext,"text",0)
        self.treeviewchoosen.append_column(treeviewcolumn)

        self.label=Gtk.Label()
        self.label.set_line_wrap(False)

        box.pack_start(self.treeviewchoosen,False,True,0)
        box.pack_end(self.label,False,False,0)
        self.set_page_complete(box, True)

        ## Extract Progress

        self.box_progress=Gtk.VBox()
        self.append_page(self.box_progress)
        self.start=False
        self.set_page_title(self.box_progress,"Progress")
        self.set_page_type(self.box_progress,Gtk.AssistantPageType.PROGRESS)

        self.liststoreprogress=Gtk.ListStore(str,bool,int)

        self.treeviewprogress=Gtk.TreeView()
        self.treeviewprogress.set_model(self.liststoreprogress)

        cellrenderertext=Gtk.CellRendererText()
        self.cellrendererspinner=Gtk.CellRendererSpinner()

        treeviewcolumn=Gtk.TreeViewColumn("Installing Modules")
        self.treeviewprogress.append_column(treeviewcolumn)
        treeviewcolumn.pack_start(cellrenderertext,False)
        treeviewcolumn.add_attribute(cellrenderertext,"text",0)

        treeviewcolumn=Gtk.TreeViewColumn("Progress")
        self.treeviewprogress.append_column(treeviewcolumn)
        treeviewcolumn.pack_start(self.cellrendererspinner,False)
        treeviewcolumn.add_attribute(self.cellrendererspinner,"active",1)

        self.box_progress.pack_start(self.treeviewprogress,True,True,0)

        ## Final Page

        self.box_final=Gtk.VBox()
        self.append_page(self.box_final)
        self.set_page_type(self.box_final,Gtk.AssistantPageType.SUMMARY)
        self.set_page_title(self.box_final,"Finish")
        label=Gtk.Label(label="Kurulum başarılı bir şekilde sonuçlandı")
        label.set_line_wrap(True)
        self.box_final.pack_start(label,True,True,0)
        self.set_page_complete(self.box_final,True)

    def on_apply_clicked(self, *args):
        if self.get_current_page() == 4 :
            self.push_progress_page()
        else :
            pass

    def on_close_clicked(self, *args):
        Gtk.main_quit()

    def on_cancel_clicked(self, *args):
        Gtk.main_quit()

    ## Sözleşme kutusu
    def on_accept_aggrement(self,checkbutton):
        self.set_page_complete(self.box, checkbutton.get_active())

    ## Modul secimi
    def toggled_module(self,widget,treepath):
        self.liststoremodules[treepath][1]=not self.liststoremodules[treepath][1]
        a=False
        for item in self.liststoremodules : ## Modul secili mi degil mi ?
            if item[1] == True :
                a = True
                break
            else :
                a = False
        if a :
            self.set_page_complete(self.box_module, True)
        else :
            self.set_page_complete(self.box_module, False)

        ## Eğer modül seçildiyse kaydet
        if self.liststoremodules[treepath][1] is True :
            self.liststorechoosen.append([self.liststoremodules[treepath][0]])
            self.treeviewchoosen.set_model(self.liststorechoosen)

        ## Seçimden çıkartıldı ise sil
        else :
            iter=self.liststorechoosen.get_iter_first()
            while iter is not None :
                if(self.liststorechoosen[iter][0]==self.liststoremodules[treepath][0]):
                    self.liststorechoosen.remove(iter)
                    self.treeviewchoosen.set_model(self.liststorechoosen)
                    break
                else :
                    iter=self.liststorechoosen.iter_next(iter)

    ## Seçilen dizinin isminin tutulması ve seçme işleminin bitimi
    def on_select_file(self,widget):
        if widget.get_filename() is not None: ## Eğer bir dizin seçildiyse kaydet ve sayfayı kapat
            self.destinationfile=widget.get_filename()
            self.label.set_markup("Choosen modules will install to " + self.destinationfile + ".\n"
                            "If you sure <b>continuing the installation</b> please click the <u>Apply</u> button!")
            self.set_page_complete(self.box2,True)
        else :
            pass

    ## Onaylanan sayfadaki modüllerin bir sonraki süreç sayfasındaki tabloda güncellenmesi
    def push_progress_page(self):
        iter = self.liststorechoosen.get_iter_first()
        while iter is not None: # Onaylanan modüllerin işlem sayfasına gönderilmesi
            self.liststoreprogress.append([self.liststorechoosen[iter][0],True,0])
            iter=self.liststorechoosen.iter_next(iter)
        self.treeviewprogress.set_model(self.liststoreprogress)
        GObject.timeout_add(100, self.on_pulse_spinner)                         # Spinner Dönüşü
        process=progressThread(self)
        process.start()                                                         # Eş zamanlı unzip işlemi
        
    ## Spinnerların dönmeleri için gerekli kod
    def on_pulse_spinner(self):

        for item in self.liststoreprogress:
            if item[1]:
                if item[2] == 12:
                    item[2] = 0
                else:
                    item[2] += 1

            self.cellrendererspinner.set_property("pulse", item[2])
        return True

    ## Unzip Yapma Islemi
    def on_extract_progress(self):

        for item in self.liststoreprogress :
            self.bar=TarFile("Zips/"+item[0],self.destinationfile)
            self.bar.extract()
            item[1]=False

        self.set_page_complete(self.box_progress,True)

## Spinnnerların dönmesi için gerekli thread

class progressThread(threading.Thread):
    a=Installation()
    def __init__(self,window):
        threading.Thread.__init__(self)
        self.a=window
    def run(self):
        self.a.on_extract_progress()

window = Installation()
window.show_all()
Gtk.main()
