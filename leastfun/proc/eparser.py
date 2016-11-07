import re
from sympy.parsing.sympy_parser import *

def list_parser( txt ):
    """This function provides validations for a single list
    from a txt input

    :txt: the text to be parsed
    :returns: a list if it's succesfull or [] if it fails
    """
    rexp = re.compile( "\d+\.?\d*?" )
    txt = txt.replace( '^', '**' )
    txtlist = txt.replace(' ', '').split(',')

    try:
        return [ parse_expr(n, evaluate=True) for n in txtlist ]
    except ( SyntaxError, sympy.parsing.sympy_tokenize.TokenError ):
        return []
