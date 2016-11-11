from sympy import *
from .least import *

import time

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def make_pdf(transformer, filename):
    """creates and saves a document with all the
    procedure to create a leastsquare interpolation
    to the filename specified

    :transformer: data structure that holds all information
    :filename: file to be created
    """
    doc = SimpleDocTemplate("form_letter.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    Story=[]
    graph = "ans.png"
    magName = "Least"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"

    formatted_time = time.ctime()
    full_name = "Mike Driscoll"
    address_parts = ["411 State St.", "Marshalltown, IA 50158"]

    im = Image(graph, 6*inch, 4*inch)
    Story.append(im)

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    # Start Document
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Equation: %s</font>' % str(transformer.eq).replace( '**', '^' )
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    for i, c in enumerate(transformer.cs):
        try:
            ptext = '<font size=12>C%s = %s </font>' % ( str(round(i,6)), str(c) )
            Story.append(Paragraph(ptext, styles["Normal"]))
        except AttributeError:
            print( "UPS CAUGHT" )
    Story.append(Spacer(1, 12))

    ptext = '<font size=12>We would like to welcome you to our subscriber base for %s Magazine!\
            You will receive %s issues at the excellent introductory price of $%s. Please respond by\
            %s to start receiving your subscription and get the following free gift: %s.</font>' % (magName,
                                                                                                    issueNum,
                                                                                                    subPrice,
                                                                                                    limitedDate*1000,
                                                                                                    freeGift)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Sincerely,</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 48))
    ptext = '<font size=12>Ima Sucker</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    doc.build(Story)
