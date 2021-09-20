import re
from sly import Lexer, Parser


class SimpleLexer(Lexer):

    tokens = {ID, LSHIFTER, RSHIFTER, EXT, DOCT, UOCT, END}

    ignore = ' \t'

    ID = r"[,:;'~^.]"
    LSHIFTER = r'<{1,}'
    RSHIFTER = r'>{1,}'
    EXT=r'[`|_]{1,}'
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
            # rhythm
            t.value = "R"
        elif t.value == '.':
            # rest
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
    def note(self, p):
        return (p.ID)
    
    @_('DOCT note')
    def note(self, p):
        """Return note, 'down', and the number of octaves"""
        fs = re.findall(r'\-', p.DOCT)
        return (p.note, len(fs), 'down')

    @_('note UOCT')
    def note(self, p):
        """Return note, 'up', and the number of octaves"""
        ss = re.findall(r'\+', p.UOCT)
        return (p.note, len(ss), 'up')
    
    @_('LSHIFTER note')
    def note(self, p):
        """Return note, 'flat', and the number of seminote"""
        matches = re.findall(r'\<', p.LSHIFTER)
        return (p.note, len(matches), 'flat')

    @_('note RSHIFTER')
    def note(self, p):
        """Return note, 'sharp', and the number of seminote"""
        matches = re.findall(r'\>', p.RSHIFTER)
        return (p.note, len(matches), 'sharp')

    @_('note EXT')
    def expr(self, p):
        """Return a note with its length of extension"""
        extensions = re.findall(r'`|_', p.EXT)
        return (p.note, len(extensions))

    @_('note')
    def expr(self, p):
        return (p.note)

    @_('END')
    def end(self, p):
        return ("end", p.END)
    
    @_('end end')
    def end(self, p):
        return ("end")


lexer = SimpleLexer()
parser = SimpleParser()

example = """
;;;  ; |
mmmm,___,_,,


xxxxxxxx this is ignored
,,,,,,--,,>>` v
         ,>>,,,,,
            ,,,,,

   ,`,`:`,~~
    _,~:_,_ |
    ._______^
     _____
        ;`


    '''~++`
     --'>>_
     
     <
     ;++```
     v
"""

e1 = ";>++__v"
e2 = ";+>> __v"
e3 = '-;> __v'
e4 = "<-; __v"
e5 = "-<; __ v"
e6 = "-;> __v"
e7 = " <;+ `` <;+ __ ;+ ;_v"

examples = [e1, e2, e3, e4, e5, e6, e7]

# for tok in lexer.tokenize(example):
#     print(f"type={tok.type}, value='{tok.value}'")
for e in examples:
    print(e, parser.parse(lexer.tokenize(e)))
