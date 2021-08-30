import re
from sys import setswitchinterval
from sly import Lexer, Parser


class SimpleLexer(Lexer):
    
    """TODO:
    I want to make it less precise -
    letting the space breath
    letting the space do the "rhythm"
    you can kind of build up the space between notes and beats
    using your intuition, your "feeling"
    """


    tokens = {ID, LSHIFTER, RSHIFTER, EXT, DOCT, UOCT, END}

    ignore = ' \t'

    ID = r"[,:;'~^.]"
    LSHIFTER = r'<{1,}'
    RSHIFTER = r'>{1,}'
    EXT=r'`|_'
    DOCT=r'\-{1,}'
    UOCT=r'\+{1,}'
    END = r'v|\n{2,}|\|'

    def error(self, t):
        print(f"Ignoring {t.value[0]}")
        self.index += 1

    def ID(self, t):
        if t.value == ",":
            t.value = "C"
        elif t.value == ":":
            t.value = "D"
        elif t.value == ";":
            t.value = "E"
        elif t.value == "'":
            t.value = "G"
        elif t.value == "~":
            t.value = "A"
        elif t.value == "^":
            t.value = "R"
        elif t.value == '.':
            t.value = "r"
        return t
    
# --- Grammar
class SimpleParser(Parser):
    # uncomment the following line to output the parser logs
    # debugfile = 'parser.out'
    # required
    tokens = SimpleLexer.tokens

    @_('scores score')
    def scores(self, p):
        return p.scores + [ p.score ]

    @_('score')
    def scores(self, p):
        return [ p.score ]

    @_('patterns end')
    def score(self, p):
        return 'score', p.patterns

    @_('patterns pattern')
    def patterns(self, p):
        return p.patterns + [ p.pattern ]

    @_('pattern')
    def patterns(self, p):
        return [ p.pattern ]

    @_('expr')
    def pattern(self, p):
        return (p.expr)

    @_('ID')
    def expr(self, p):
        return (p.ID)
    
    @_('DOCT expr')
    def expr(self, p):
        """Return note, 'down', and the number of octaves"""
        fs = re.findall(r'\-', p.DOCT)
        return (p.expr, 'down', len(fs))

    @_('expr UOCT')
    def expr(self, p):
        """Return note, 'up', and the number of octaves"""
        ss = re.findall(r'\+', p.UOCT)
        return (p.expr, 'up', len(ss))
    
    @_('LSHIFTER ID')
    def expr(self, p):
        """Return note, 'flat', and the number of seminote"""
        matches = re.findall(r'\<', p.LSHIFTER)
        return (p.ID, 'flat', len(matches))

    @_('ID RSHIFTER')
    def expr(self, p):
        """Return note, 'sharp', and the number of seminote"""
        matches = re.findall(r'\>', p.RSHIFTER)
        return (p.ID, 'sharp', len(matches))

    @_('expr EXT')
    def expr(self, p):
        """Return a note with its length of extension"""
        if len(p.expr) == 2:
            n_ext = p.expr[1] + 1
            return (p.expr[0], n_ext)
        else:
            return (p.expr, 1)

    @_('END')
    def end(self, p):
        return ("end", p.END)
    
    @_('end end')
    def end(self, p):
        return ("end")


lexer = SimpleLexer()
parser = SimpleParser()

example = """
;;;  ; 
,,

,,,,,,--,,>> v
         ,>>,,,,,
            ,,,,,

   ,`,`:`,~~
    _,~:_,_ |
    ._______^
     _____
        ;`


    '''~++
     --' 
  >>    <
    ;++
     v


"""

# for tok in lexer.tokenize(example):
#     print(f"type={tok.type}, value='{tok.value}'")

print(parser.parse(lexer.tokenize(example)))
