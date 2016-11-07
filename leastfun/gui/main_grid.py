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

        self.answer = ""

        self.set_border_width( WIDTH )
        self.set_column_homogeneous( 1 )
        self.set_row_spacing( WIDTH )
        self.set_column_spacing( WIDTH )

        self.text_grid = Gtk.Grid()
        self.text_grid.set_column_homogeneous(1)
        self.text_grid.set_row_spacing( WIDTH )
        self.text_grid.set_column_spacing( WIDTH )
        self.text_grid.set_vexpand( True )

        self.button_grid = Gtk.Grid()
        self.button_grid.set_column_homogeneous(1)
        self.button_grid.set_row_spacing( WIDTH )
        self.button_grid.set_column_spacing( WIDTH )

        self.radio_grid = Gtk.Grid()
        self.radio_grid.set_column_homogeneous(1)
        self.radio_grid.set_row_spacing( WIDTH )
        self.radio_grid.set_column_spacing( WIDTH )

        aff_list = Gtk.ListStore( str )
        for elem in ['Custom', 'Exponential', 'Power']:
            aff_list.append( [elem] )

        #--Answer
        self.txt_ans = Gtk.Label( 'hello' )
        self.txt_ans.set_no_show_all( True )

        #--Affinity
        self.txt_aff = Gtk.Entry()
        self.txt_aff.set_placeholder_text('1+var+var² > 1,var,var^2')
        self.txt_aff.set_no_show_all( True )
        self.lbl_aff = Gtk.Label( 'Affinity:' )
        self.lbl_aff.set_justify( Gtk.Justification.LEFT )

        self.lbl_aff.set_no_show_all( True )

        #--Points in X
        self.txt_ptsx = Gtk.Entry()
        self.txt_ptsx.set_placeholder_text('1,2,3...n')
        self.lbl_ptsx = Gtk.Label( 'Points in X:' )
        self.lbl_ptsx.set_justify( Gtk.Justification.LEFT )


        #--Points in Y
        self.txt_ptsy = Gtk.Entry()
        self.txt_ptsy.set_placeholder_text('1,2,3...n or cos(var)')
        self.lbl_ptsy = Gtk.Label( 'Points in f(X):' )
        self.lbl_ptsy.set_justify( Gtk.Justification.LEFT )


        #--Vars
        self.txt_var = Gtk.Entry()
        self.txt_var.set_placeholder_text('x or y or vx and so on')
        self.lbl_var = Gtk.Label( 'Variable:' )
        self.lbl_var.set_justify( Gtk.Justification.LEFT )


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
        self.handler_id = self.button_ok.connect( "pressed", self.on_ok_press_disc )
        self.button_load = Gtk.Button( 'Load' )

        #--RadioButtons
        self.radio_disc = Gtk.RadioButton.new_with_label_from_widget( None, 'Discrete' )
        self.radio_cont = Gtk.RadioButton.new_from_widget( self.radio_disc )
        self.radio_cont.set_label( 'Continuous' )
        self.radio_disc.connect( 'toggled', self.on_mode_change, 'disc' )
        self.radio_cont.connect( 'toggled', self.on_mode_change, 'cont' )

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

        self.radio_grid.attach( self.radio_disc, 1, 1, 1, 1 )
        self.radio_grid.attach( self.radio_cont, 2, 1, 1, 1 )

        self.attach( self.aff_combo, 1, 1, 1, 1 )
        self.attach( self.radio_grid, 1, 2, 1, 1 )
        self.attach( self.text_grid, 1, 3, 1, 1 )
        self.attach( self.button_grid, 1, 4, 1, 1 )
        self.attach( self.txt_ans, 1, 5, 1, 1 )

    #--Extra methods
    def raise_err_dialog( self, message ):
        err_var = Gtk.MessageDialog( self.parent, 0, Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CANCEL, message)
        err_var.run()
        err_var.destroy()

    def send_ans( self, eqx, vr, ran ):
        self.parent.gmodule.render_main_eq( eqx, vr, ran )

    #--Actions
    def on_aff_change( self, aff_combo ):
        if( aff_combo.get_active() == 0 ):
            self.txt_aff.show()
            self.lbl_aff.show()
        else:
            self.txt_aff.hide()
            self.lbl_aff.hide()

    def on_mode_change( self, r_button, mode ):
        if r_button.get_active() and mode == 'cont':
            self.button_ok.disconnect( self.handler_id )
            self.handler_id = self.button_ok.connect( "pressed", self.on_ok_press_cont )
            self.lbl_ptsy.set_label( "f(X):" )
            self.txt_ptsy.set_placeholder_text( "var + var^2 etc.." )
            self.lbl_ptsx.set_label( "Range:" )
            self.txt_ptsx.set_placeholder_text( "a,b" )
        elif r_button.get_active() and mode == 'disc':
            self.button_ok.disconnect( self.handler_id )
            self.handler_id = self.button_ok.connect( "pressed", self.on_ok_press_disc )
            self.lbl_ptsy.set_label( "Points in f(X):" )
            self.txt_ptsy.set_placeholder_text('1,2,3...n or cos(var)')
            self.lbl_ptsx.show()
            self.txt_ptsx.show()

    def on_ok_press_disc( self, ok_button ):
        rexp = regexp.compile(r"[a-z]{1,2}")
        varn = self.txt_var.get_text()

        if not rexp.fullmatch( varn ):
            self.raise_err_dialog( 'Invalid Variable' )
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
            try:
                expr = Transformer( varn )
                expr.ptsx = listx
                expr.ptsy = listy
                if self.aff_combo.get_active() == 0:
                    listaff = list_parser(self.txt_aff.get_text())
                    if not listaff:
                        self.raise_err_dialog( 'Invalid affinity selected' )
                        return
                    else:
                        self.answer = expr.minimize_disc(listaff)
                elif self.aff_combo.get_active() == 1:
                    self.answer = expr.minimize_disc_exp()
                else:
                    self.answer = expr.minimize_disc_pot()
                self.send_ans( str(self.answer), varn, [float(expr.ptsx[0]), float(expr.ptsx.pop())])
            except ( ValueError, AttributeError ):
                self.raise_err_dialog( 'Invalid list size' )
        self.txt_ans.set_label( str(self.answer) )
        self.txt_ans.show()

    def on_ok_press_cont( self, ok_button ):
        rexp = regexp.compile(r"[a-z]{1,2}")
        varn = self.txt_var.get_text()

        listx = list_parser(self.txt_ptsx.get_text())

        if not rexp.fullmatch( varn ):
            self.raise_err_dialog( 'Invalid Variable' )
            return
        else:
            try:
                expr = Transformer( varn )
                expr.fx = self.txt_ptsy.get_text()
                expr.ptsx = listx
                if self.aff_combo.get_active() == 0:
                    listaff = list_parser(self.txt_aff.get_text())
                    if not listaff:
                        self.raise_err_dialog( 'Invalid affinity selected' )
                        return
                    else:
                        self.answer = expr.minimize_cont(listaff)
                elif self.aff_combo.get_active() == 1:
                    if 'cos' in expr.fx or 'sin' in expr.fx:
                        self.raise_err_dialog('Invalid fx in this affinity')
                    else:
                        self.answer = expr.minimize_cont_exp()
                else:
                    if 'cos' in expr.fx or 'sin' in expr.fx:
                        self.raise_err_dialog('Invalid fx in this affinity')
                    else:
                        self.answer = expr.minimize_cont_pot()
                self.send_ans( str(self.answer), varn, [expr.ptsx[0], expr.ptsx.pop()] )
            except ( ValueError, AttributeError ): 
                self.raise_err_dialog( 'Wrong range' )
        self.txt_ans.set_label( str(self.answer) )
        self.txt_ans.show()
