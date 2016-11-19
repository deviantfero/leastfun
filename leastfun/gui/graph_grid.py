from gi import require_version
require_version( 'Gtk', '3.0' )
from gi.repository import Gtk

import copy
import os

from matplotlib.figure import Figure
from sympy import *
from sympy.plotting import plot
from ..proc.zoom import *
from ..proc.eparser import *
from ..proc.least import *
from ..proc.pdfactory import *

from numpy import *
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

WIDTH = 10
COLOR = ['b','g','c', 'm', 'k']
STYLE = ['','-', '+', '', '--', '-.']

class GraphGrid(Gtk.Grid):

    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.parent = parent

        self.fig = Figure( figsize=(6,6), dpi=65 )
        self.axis = self.fig.add_subplot( 111 )
        self.axis.grid( True )
        self.graph_count = 0

        self.set_border_width( WIDTH )
        self.set_column_homogeneous( 1 )
        self.set_row_spacing( WIDTH )
        self.set_column_spacing( WIDTH )

        #--ButtonGrid
        self.button_grid = Gtk.Grid()
        self.button_grid.set_border_width( WIDTH )
        self.button_grid.set_column_homogeneous( 1 )
        self.button_grid.set_row_spacing( WIDTH )
        self.button_grid.set_column_spacing( WIDTH )

        #--InputGrid
        self.txt_grid = Gtk.Grid()
        self.txt_grid.set_column_homogeneous( 1 )
        self.txt_grid.set_column_spacing( WIDTH )


        #--Buttons
        self.button_clear = Gtk.Button( 'Clear' )
        self.button_clear.connect( 'pressed', self.on_clear_press )
        self.button_add = Gtk.Button( 'Add' )
        self.button_add.connect( 'pressed', self.on_add_press )
        self.button_save = Gtk.Button( 'Save' )
        self.button_save.connect( 'pressed', self.on_save_press )
        self.button_snapshot = Gtk.Button( 'Snapshot' )
        self.button_snapshot.connect( 'pressed', self.on_snapshot_press )

        #--Text Input
        self.txt_eq = Gtk.Entry()
        self.txt_eq.set_placeholder_text('cos(var)...etc')
        self.lbl_eq = Gtk.Label( 'Equation:' )
        self.lbl_eq.set_justify( Gtk.Justification.LEFT )
        self.txt_var = Gtk.Entry()
        self.txt_var.set_placeholder_text('xc or x or y')
        self.lbl_var = Gtk.Label( 'Variables:' )
        self.lbl_var.set_justify( Gtk.Justification.LEFT )
        self.txt_ran = Gtk.Entry()
        self.txt_ran.set_placeholder_text('a,b')
        self.lbl_ran = Gtk.Label( 'Range:' )
        self.lbl_ran.set_justify( Gtk.Justification.LEFT )
        self.lbl_snapshot = Gtk.Label( 'Snapshot Taken' )
        self.lbl_snapshot.set_no_show_all( True )


        #--Graph added to canvas
        self.canvas = FigureCanvas( self.fig )
        self.canvas.set_size_request( 300, 300 )
        self.canvas.set_hexpand( True )
        self.canvas.set_vexpand( True )

        #--Button attachments
        self.button_grid.attach( self.txt_grid, 1,1,2,1 )
        self.button_grid.attach( self.button_add, 1,2,1,1 )
        self.button_grid.attach( self.button_clear, 2,2,1,1 )
        self.button_grid.attach( self.button_snapshot, 1,3,1,1 )
        self.button_grid.attach( self.button_save, 2,3,1,1 )
        self.button_grid.attach( self.lbl_snapshot, 1,4,2,1 )

        #--Entry attachments
        self.txt_grid.attach( self.lbl_var, 1,1,1,1 )
        self.txt_grid.attach( self.txt_var, 1,2,1,1 )
        self.txt_grid.attach( self.lbl_eq, 2,1,1,1 )
        self.txt_grid.attach( self.txt_eq, 2,2,1,1 )
        self.txt_grid.attach( self.lbl_ran, 3,1,1,1 )
        self.txt_grid.attach( self.txt_ran, 3,2,1,1 )

        #--Main Grid attachments
        self.attach( self.canvas, 1, 1, 1, 1 )
        self.attach( self.button_grid, 1, 2, 1, 1 )

    def render_main_eq( self, eq, vr, ran ):
        seq = sympify( eq )
        eq = eq.replace( '**', '^' )
        evaleq = lambdify(sympify( vr ), seq, modules=['numpy'])
        ran = linspace( ran[0], ran[1], 200)
        self.axis.set_title( 'fig.' + str(self.parent.cmodule.document.proc_count) )
        zp = ZoomPan()
        figZoom = zp.zoom_factory( self.axis, base_scale=0.9 )
        figPan = zp.pan_factory( self.axis )
        if self.graph_count > 0:
            line = COLOR[random.randint(0, len(COLOR) - 1)] + STYLE[random.randint(0, len(STYLE) - 1)]
            self.axis.set_ylim( top=10 )
            self.axis.plot( ran, evaleq(ran), line, label=eq )
            print( str(seq) )
            self.axis.legend( loc='best' )
            self.axis.margins( 0.4 )
        else:
            self.axis.plot( ran, evaleq(ran), 'r', label=eq )
            self.axis.legend( loc='best' )
            self.axis.margins( 0.4 )
        self.graph_count += 1

    def save_render( self, filename ):
        self.fig.savefig(filename)

    def on_snapshot_press( self, button ):
        if self.parent.cmodule.document.proc_count > 0:
            self.save_render( 'ans' + str(self.parent.cmodule.document.proc_count - 1) + '.png' )
        else:
            self.save_render( 'ans' + str(self.parent.cmodule.document.proc_count) + '.png' )
        self.lbl_snapshot.show()

    def render_points( self, ptsx, ptsy, ran, lbl='Points given' ):
        if self.graph_count < 2:
            try:
                self.axis.plot( ptsx, ptsy, COLOR[random.randint(0, len(COLOR) - 1)] + 'o', label=lbl)
                self.axis.legend( loc='best' )
                self.axis.margins( 0.4 )
            except Exception:
                self.parent.raise_err_dialog( "Invalid points to interpolate" )

    def on_clear_press( self, button, opt=True ):
        self.axis.cla()
        self.axis.grid( True )
        self.graph_count = 0
        if opt:
            dialog = Gtk.MessageDialog(self.parent, 0, Gtk.MessageType.QUESTION,
                    Gtk.ButtonsType.YES_NO, "Warning!")
            dialog.format_secondary_text(
                    "Do you wish to delete the Document in progress too?")
            response = dialog.run()

            if response == Gtk.ResponseType.YES:
                self.parent.cmodule.document.proc_count = 0
                self.parent.cmodule.document.story = []
            self.lbl_snapshot.hide()
            dialog.destroy()

    def on_add_press( self, button ):
        try:
            ran = list_parser( self.txt_ran.get_text() )
            if len(ran) == 2:
                try:
                    ran = [float(x) for x in ran]
                except TypeError:
                    self.parent.raise_err_dialog( 'Invalid range for plotting' )
                    return
            else:
                self.parent.raise_err_dialog( 'Invalid range for plotting' )
                return
            ran.sort()
            eq = list_parser( self.txt_eq.get_text() )
            if not ran:
                self.parent.raise_err_dialog( 'Invalid Range' );
                return
            elif not eq:
                self.parent.raise_err_dialog( 'Invalid Equation' )
                return
            elif len(self.txt_var.get_text()) > 2:
                self.parent.raise_err_dialog( 'Invalid Variable' )
                return
            else:
                self.render_main_eq( eq[0], self.txt_var.get_text(), ran )
        except Exception as e:
            self.parent.raise_err_dialog( 'Something went wrong' )
        self.lbl_snapshot.hide()

    def on_save_press( self, button ):
        if self.parent.cmodule.document.story:
            sdialog = Gtk.FileChooserDialog( 'Saving', self.parent,
                    Gtk.FileChooserAction.SAVE,
                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                        Gtk.STOCK_OK, Gtk.ResponseType.OK))
            sdialog.set_current_name( "procedure.pdf" )
            response = sdialog.run()
            #--Checking if file exists and overwriting
            if response == Gtk.ResponseType.OK:
                if not os.path.exists( sdialog.get_filename() ):
                    self.parent.cmodule.document.save_pdf( sdialog.get_filename() )
                    print( 'saved' )
                    sdialog.destroy()
                else:
                    dialog = Gtk.MessageDialog(self.parent, 0, Gtk.MessageType.QUESTION,
                            Gtk.ButtonsType.YES_NO, "Warning!")
                    dialog.format_secondary_text(
                            "Do you wish to overwrite this file?")
                    overwrite = dialog.run()
                    if overwrite == Gtk.ResponseType.YES:
                        self.parent.cmodule.document.save_pdf( sdialog.get_filename() )
                        print( 'overwrite' )
                    dialog.destroy()
                    sdialog.destroy()
