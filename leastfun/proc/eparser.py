import re
from sympy.parsing.sympy_parser import *

def list_parser( txt ):
    """This function provides validations for a single list
    from a txt input

    :txt: the text to be parsed
    :returns: a list if it's succesfull or [] if it fails
    """
    rexp = re.compile( "\d+\.\.\.\d+" )
    txt = txt.replace( '^', '**' )
    if rexp.fullmatch(txt):
        tmp = txt.split('...')
        txtlist = list(range(int(tmp[0]), int(tmp[1]) + 1))
        txtlist = [str(x) for x in txtlist]
    else:
        txtlist = txt.replace(' ', '').split(',')

    try:
        return [ parse_expr(n, evaluate=True) for n in txtlist ]
    except ( SyntaxError, sympy.parsing.sympy_tokenize.TokenError ):
        return []
