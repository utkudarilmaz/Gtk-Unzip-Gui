#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject

class CellRendererSpinner(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("CellRendererSpinner")
        self.connect("destroy", Gtk.main_quit)

        self.liststore = Gtk.ListStore(str, bool, int)
        self.liststore.append(["Copying files", True,  0])
        self.liststore.append(["Downloading access logs", False, 0])
        self.liststore.append(["Connecting to server", True, 0])

        treeview = Gtk.TreeView()
        treeview.set_model(self.liststore)
        self.add(treeview)

        cellrenderertext = Gtk.CellRendererText()
        self.cellrendererspinner = Gtk.CellRendererSpinner()

        treeviewcolumn = Gtk.TreeViewColumn("Activity")
        treeview.append_column(treeviewcolumn)
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 0)

        treeviewcolumn = Gtk.TreeViewColumn("Status")
        treeview.append_column(treeviewcolumn)
        treeviewcolumn.pack_start(self.cellrendererspinner, False)
        treeviewcolumn.add_attribute(self.cellrendererspinner, "active", 1)

        GObject.timeout_add(100, self.on_spinner_pulse)

    def on_spinner_pulse(self):
        for item in self.liststore:
            if item[1]:
                if item[2] == 12:
                    item[2] = 0
                else:
                    item[2] += 1

        self.cellrendererspinner.set_property("pulse", item[2])

        return True

window = CellRendererSpinner()
window.show_all()
Gtk.main()

