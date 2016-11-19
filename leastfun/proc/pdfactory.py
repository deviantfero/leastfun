from sympy import *
from .least import *

import copy

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

LINEBREAK = 8

class PdfFactory():

    """Docstring for PdfFactory. """

    def __init__(self):
        self.story=[]
        self.proc_count = 0
        self.transformer = 0

    def add_procedure(self, transformer, case, interpolation=False):
        """creates and saves a document with all the
        procedure to create a leastsquare interpolation
        to the filename specified

        :transformer: data structure that holds all information
        """
        mode = ''
        graph = 'ans' + str( self.proc_count ) + '.png'
        self.transformer = transformer
        self.proc_count += 1

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
            ptext = '<font size=11><strong>EQ%d: </strong></font><font size=10>' % i
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
                ptext = '<font size=10>C%s = %s </font>' % ( str(i), str(round(c,6)) )
                self.story.append(Paragraph(ptext, styles["Normal"]))
            except ( AttributeError, TypeError ):
                ptext = '<font size=10>C%s = %s </font>' % ( str(i), str(c) )
                self.story.append(Paragraph(ptext, styles["Normal"]))

        self.story.append(Spacer(1, LINEBREAK*2))

        ptext = '<font size=12><strong>g(x):</strong> %s</font>' % str(transformer.eq).replace( '**', '^' )
        self.story.append(Paragraph(ptext, styles["Normal"]))
        self.story.append(Spacer(1, LINEBREAK))

        if case == 1:
            ptext = '<font size=12><strong>f(x):</strong> %s</font>' % str(transformer.fx).replace( '**', '^' )
            self.story.append(Paragraph(ptext, styles["Normal"]))
            self.story.append(Spacer(1, LINEBREAK))

        im = Image(graph, 6*inch, 4*inch)
        self.story.append(im)
        if not interpolation:
            self.story.append(PageBreak())
        print( ':: Procedure Added' )

    def add_interpolation_table( self, data, disc=True ):
        if len(data[0]) > 8:
            raise Exception
        data[0] = [ round(x, 6) for x in data[0] ]
        data[1] = [ round(x, 6) for x in data[1] ]
        if not disc:
            tmp = []
            data[2] = [ round(x, 6) for x in data[2] ]
            for i, r in enumerate(data[1]):
                tmp.append(str(round( abs((data[2][i] - r)/data[2][i])*0.1, 3)) + "%")
            data.append(tmp)
            data[2] = ['f(x)'] + data[2]
            data[3] = ['ERR%'] + data[3]
        data[0] = ['PUNTOS'] + data[0]
        data[1] = ['g(x)'] + data[1]

        t = Table( data )
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.lavender),
                               ('BACKGROUND',(0,0),(0,-1),colors.beige),
                               ('GRID',(0,0),(-1,-1),0.5,colors.black)]))
        self.story.append(t)
        self.story.append(PageBreak())

    def save_pdf( self, filename ):
        doc = SimpleDocTemplate(filename,pagesize=letter,
                                rightMargin=72,leftMargin=72,
                                topMargin=72,bottomMargin=18)
        doc.build(copy.deepcopy(self.story))
