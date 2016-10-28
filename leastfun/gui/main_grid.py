from gi import require_version
require_version( 'Gtk', '3.0' )
from gi.repository import Gtk

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

        #--Regression combo box
        self.aff_combo = Gtk.ComboBox.new_with_model( aff_list )
        self.rendr_txt = Gtk.CellRendererText()
        self.aff_combo.pack_start( self.rendr_txt, True )
        self.aff_combo.add_attribute( self.rendr_txt, "text", 0 )
        self.aff_combo.set_entry_text_column(0)
        self.aff_combo.set_title( 'Regression' )

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

        self.button_ok = Gtk.Button( 'Ok' )
        self.button_load = Gtk.Button( 'Load' )

        self.text_grid.attach( self.lbl_aff, 1, 1, 1, 1 )
        self.text_grid.attach( self.txt_aff, 2, 1, 2, 1 )
        self.text_grid.attach( self.lbl_var, 1, 2, 1, 1 )
        self.text_grid.attach( self.txt_var, 2, 2, 2, 1 )
        self.text_grid.attach( self.lbl_ptsx, 1, 3, 1, 1 )
        self.text_grid.attach( self.txt_ptsx, 2, 3, 2, 1 )
        self.text_grid.attach( self.lbl_ptsy, 1, 4, 1, 1 )
        self.text_grid.attach( self.txt_ptsy, 2, 4, 2, 1 )

        self.button_grid.attach( self.button_ok, 1, 1, 1, 1 )
        self.button_grid.attach( self.button_load, 2, 1, 1, 1 )

        self.attach( self.aff_combo, 1, 1, 1, 1 )
        self.attach( self.text_grid, 1, 2, 1, 1 )
        self.attach( self.button_grid, 1, 3, 1, 1 )
