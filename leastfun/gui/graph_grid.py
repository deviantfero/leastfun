from gi import require_version
require_version( 'Gtk', '3.0' )
from gi.repository import Gtk

from matplotlib.figure import Figure
from sympy import *
from sympy.plotting import plot
from ..proc.zoom import *

from numpy import *
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

WIDTH = 10
COLOR = ['b','g','c', 'm', 'k']
STYLE = ['','o', '-', '+', '', '--', '-.', 'd', 'x']

class GraphGrid(Gtk.Grid):

    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.parent = parent

        self.fig = Figure( figsize=(5,5), dpi=72 )
        self.axis = self.fig.add_subplot( 211 )
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

        #--Buttons
        self.button_clear = Gtk.Button( "Clear" )
        self.button_clear.connect( 'pressed', self.on_clear_press )


        #--Graph added to canvas
        self.canvas = FigureCanvas( self.fig )
        self.canvas.set_size_request( 300, 300 )
        self.canvas.set_hexpand( True )
        self.canvas.set_vexpand( True )

        #--Button attachmetns
        self.button_grid.attach( self.button_clear, 1,1,1,1 )

        #--Main Grid attachments
        self.attach( self.canvas, 1, 1, 1, 1 )
        self.attach( self.button_grid, 1, 2, 1, 1 )

    def render_main_eq( self, eq, vr, ran ):
        seq = sympify( eq )
        evaleq = lambdify(sympify( vr ), seq, modules=['numpy'])
        ran = linspace( ran[0], ran[1], 200)
        self.axis.set_title( eq )
        zp = ZoomPan()
        figZoom = zp.zoom_factory( self.axis, base_scale=0.5 )
        figPan = zp.pan_factory( self.axis )
        if self.graph_count > 0:
            line = COLOR[random.randint(0, len(COLOR) - 1)] + STYLE[random.randint(0, len(STYLE) - 1)]
            self.axis.set_ylim( top=10 )
            self.axis.plot( ran, evaleq(ran), line, label=seq )
            self.axis.legend( loc='best' )
        else:
            self.axis.plot( ran, evaleq(ran), 'r', label=seq )
            self.axis.legend( loc='best' )
        self.graph_count += 1

    def on_clear_press( self, button ):
        self.axis.cla()
