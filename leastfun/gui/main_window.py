import os
import sys

from gi import require_version
require_version( 'Gtk', '3.0' )
from gi.repository import Gtk
from .main_grid import *
from .graph_grid import *
from ..proc.least import *

WIDTH = 10

class MainWin( Gtk.Window ):
    def __init__( self ):
        Gtk.Window.__init__( self, title='leastfun')
        self.connect('delete-event', Gtk.main_quit)
        self.set_border_width( WIDTH )
        self.set_default_size( 200, 400 )

        self.tabs = Gtk.Notebook()

        self.cmodule = MainGrid( self )
        self.gmodule = GraphGrid( self )
        self.add( self.tabs )
        self.tabs.append_page( self.cmodule, Gtk.Label( "Control" ) )
        self.tabs.append_page( self.gmodule, Gtk.Label( "Graph" ) )

    def raise_err_dialog( self, message ):
        err_var = Gtk.MessageDialog( self , 0, Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CANCEL, message)
        err_var.run()
        err_var.destroy()

def run():
    win = MainWin()
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    run()
