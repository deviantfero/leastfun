from gi import require_version
require_version( 'Gtk', '3.0' )
from gi.repository import Gtk
import re as regexp

from ..proc.eparser import *
from ..proc.least import *
from sympy import *

WIDTH = 10

class MainGrid(Gtk.Grid):

    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.parent = parent
        self.set_border_width( WIDTH )
        self.set_column_homogeneous( 1 )
        self.set_row_spacing( WIDTH )
        self.set_column_spacing( WIDTH )

        self.text_grid = Gtk.Grid()
        self.text_grid.set_column_homogeneous(1)
        self.text_grid.set_row_spacing( WIDTH )
        self.text_grid.set_column_spacing( WIDTH )

        self.button_grid = Gtk.Grid()
        self.button_grid.set_column_homogeneous(1)
        self.button_grid.set_row_spacing( WIDTH )
        self.button_grid.set_column_spacing( WIDTH )

        aff_list = Gtk.ListStore( str )
        for elem in ['Custom', 'Exponential', 'Power']:
            aff_list.append( [elem] )


        #--Affinity
        self.txt_aff = Gtk.Entry()
        self.txt_aff.set_placeholder_text('1+var+var² > 1,var,var^2')
        self.txt_aff.set_no_show_all( True )
        self.lbl_aff = Gtk.Label( 'Affinity:' )
        self.lbl_aff.set_justify( Gtk.Justification.LEFT )
        self.lbl_aff.set_xalign(0)
        self.lbl_aff.set_no_show_all( True )

        #--Points in X
        self.txt_ptsx = Gtk.Entry()
        self.txt_ptsx.set_placeholder_text('1,2,3...n')
        self.lbl_ptsx = Gtk.Label( 'Points in X:' )
        self.lbl_ptsx.set_justify( Gtk.Justification.LEFT )
        self.lbl_ptsx.set_xalign(0)

        #--Points in Y
        self.txt_ptsy = Gtk.Entry()
        self.txt_ptsy.set_placeholder_text('1,2,3...n or cos(var)')
        self.lbl_ptsy = Gtk.Label( 'Points in f(X):' )
        self.lbl_ptsy.set_justify( Gtk.Justification.LEFT )
        self.lbl_ptsy.set_xalign(0)

        #--Vars
        self.txt_var = Gtk.Entry()
        self.txt_var.set_placeholder_text('x or y or varx')
        self.lbl_var = Gtk.Label( 'Variable:' )
        self.lbl_var.set_justify( Gtk.Justification.LEFT )
        self.lbl_var.set_xalign(0)

        #--Regression combo box
        self.aff_combo = Gtk.ComboBox.new_with_model( aff_list )
        self.rendr_txt = Gtk.CellRendererText()
        self.aff_combo.pack_start( self.rendr_txt, True )
        self.aff_combo.add_attribute( self.rendr_txt, "text", 0 )
        self.aff_combo.set_entry_text_column(0)
        self.aff_combo.set_title( 'Regression' )
        self.aff_combo.connect( "changed", self.on_aff_change )
        self.aff_combo.set_active(0)

        #--Buttons
        self.button_ok = Gtk.Button( 'Ok' )
        self.button_ok.connect( "pressed", self.on_ok_press )
        self.button_load = Gtk.Button( 'Load' )

        #--Grid attaching
        self.text_grid.attach( self.lbl_var, 1, 1, 1, 1 )
        self.text_grid.attach( self.txt_var, 2, 1, 2, 1 )
        self.text_grid.attach( self.lbl_aff, 1, 2, 1, 1 )
        self.text_grid.attach( self.txt_aff, 2, 2, 2, 1 )
        self.text_grid.attach( self.lbl_ptsx, 1, 3, 1, 1 )
        self.text_grid.attach( self.txt_ptsx, 2, 3, 2, 1 )
        self.text_grid.attach( self.lbl_ptsy, 1, 4, 1, 1 )
        self.text_grid.attach( self.txt_ptsy, 2, 4, 2, 1 )

        self.button_grid.attach( self.button_ok, 1, 1, 1, 1 )
        self.button_grid.attach( self.button_load, 2, 1, 1, 1 )

        self.attach( self.aff_combo, 1, 1, 1, 1 )
        self.attach( self.text_grid, 1, 2, 1, 1 )
        self.attach( self.button_grid, 1, 3, 1, 1 )

    #--Extra methods
    def raise_err_dialog( self, message ):
        err_var = Gtk.MessageDialog( self.parent, 0, Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CANCEL, message)
        err_var.run()
        err_var.destroy()

    #--Actions
    def on_aff_change( self, aff_combo ):
        if( aff_combo.get_active() == 0 ):
            self.txt_aff.show()
            self.lbl_aff.show()
        else:
            self.txt_aff.hide()
            self.lbl_aff.hide()

    def on_ok_press( self, ok_button ):
        rexp = regexp.compile(r"[a-z]+")
        varn = self.txt_var.get_text()

        if not rexp.fullmatch( varn ):
            self.raise_err_dialog( 'Invalid Variable' )
            return
        elif varn == "varn":
            self.raise_err_dialog( 'varn is not a valid Variable' )
            return

        listx = list_parser(self.txt_ptsx.get_text())
        listy = list_parser(self.txt_ptsy.get_text())

        if not listx and listy:
            self.raise_err_dialog( 'Invalid X points list' )
        elif not listy and listx:
            self.raise_err_dialog( 'Invalid F(X) points list' )
        elif not listy and not listx:
            self.raise_err_dialog( 'Invalid or empty points list on X and Y' )
        else:
            expr = Transformer( varn )
            expr.ptsx = listx
            expr.ptsy = listy
            if self.aff_combo.get_active() == 0:
                listaff = list_parser(self.txt_aff.get_text())
                if not listaff:
                    self.raise_err_dialog( 'Invalid affinity selected' )
                    return
                else:
                    print(expr.minimize_disc(listaff))
            elif self.aff_combo.get_active() == 1:
                print(expr.minimize_disc_exp())
            else:
                print(expr.minimize_disc_pot())
