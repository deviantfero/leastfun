from sympy import *
from .least import *

import copy

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

LINEBREAK = 8

class PdfFactory():

    """Docstring for PdfFactory. """

    def __init__(self):
        self.story=[]
        self.proc_count = 0

    def add_procedure(self, transformer, case):
        """creates and saves a document with all the
        procedure to create a leastsquare interpolation
        to the filename specified

        :transformer: data structure that holds all information
        """
        mode = ''
        self.proc_count += 1
        graph = 'ans' + str( self.proc_count ) + '.png'

        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

        # Start Document
        if case == 1:
            mode = 'Continuo'
        else:
            mode = 'Discreto'
        if self.proc_count < 2:
            ptext = '<font size=15><strong>Reporte de Procedimiento - %s</strong></font>' %(mode)
            self.story.append(Paragraph(ptext, styles["Normal"]))
            self.story.append(Spacer(1, LINEBREAK*2))
        else:
            ptext = '<font size=15><strong>%d - %s</strong></font>' %( self.proc_count, mode)
            self.story.append(Paragraph(ptext, styles["Normal"]))
            self.story.append(Spacer(1, LINEBREAK*2))

        ptext = '<font size=12><strong>Afinidad</strong></font>'
        self.story.append(Paragraph(ptext, styles["Normal"]))
        ptext = '<font size=10>%s</font>' %(transformer.aff)
        self.story.append(Paragraph(ptext, styles["Normal"]))
        self.story.append(Spacer(1, LINEBREAK*2))

        ptext = '<font size=12><strong>Ecuaciones normales</strong></font>'
        self.story.append(Paragraph(ptext, styles["Normal"]))
        self.story.append(Spacer(1, LINEBREAK))
        for i, c in enumerate(transformer.unsolved_m):
            ptext = '<font size=10>'
            for j, e in enumerate( c ):
                if j < len(c) - 2:
                    try:
                        ptext += 'C%s*'%(j) + str(round(N(e), 6))
                    except TypeError:
                        ptext += 'C%s*'%(j) + str(N(e))
                    ptext += ' + '
                elif j < len(c) - 1:
                    try:
                        ptext += 'C%s*'%(j) + str(round(N(e), 6))
                    except TypeError:
                        ptext += 'C%s*'%(j) + str(N(e))
                    ptext += ' = '
                else:
                    try:
                        ptext += str(round(N(e), 6))
                    except TypeError:
                        ptext += str(N(e))
            ptext += '</font>'
            self.story.append(Paragraph(ptext, styles["Normal"]))

        self.story.append(Spacer(1, LINEBREAK*2))

        ptext = '<font size=12><strong>Resolucion de ecuaciones Normales</strong></font>'
        self.story.append(Paragraph(ptext, styles["Normal"]))
        self.story.append(Spacer(1, LINEBREAK))
        for i, c in enumerate(transformer.cs):
            try:
                ptext = '<font size=10>C%s = %s </font>' % ( str(round(i,6)), str(c) )
                self.story.append(Paragraph(ptext, styles["Normal"]))
            except AttributeError:
                print( "UPS CAUGHT" )

        self.story.append(Spacer(1, LINEBREAK*2))

        ptext = '<font size=12><strong>Ecuación:</strong> %s</font>' % str(transformer.eq).replace( '**', '^' )
        self.story.append(Paragraph(ptext, styles["Normal"]))
        self.story.append(Spacer(1, LINEBREAK))

        im = Image(graph, 6*inch, 4*inch)
        self.story.append(im)
        self.story.append(PageBreak())
        print( ':: Procedure Added' )

    def save_pdf( self, filename ):
        doc = SimpleDocTemplate(filename,pagesize=letter,
                                rightMargin=72,leftMargin=72,
                                topMargin=72,bottomMargin=18)
        doc.build(copy.deepcopy(self.story))
