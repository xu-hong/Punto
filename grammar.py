import re
from sys import setswitchinterval
from sly import Lexer, Parser


class SimpleLexer(Lexer):
    tokens = {ID, LSHIFTER, RSHIFTER, END}

    ignore = ' \t'

    ID = r"[,:;'~]"
    LSHIFTER = r'<{1,}'
    RSHIFTER = r'>{1,}'
    END = r'x|\n{2,}'

    def error(self, t):
        print(f"Ignoring {t.value[0]}")
        self.index += 1

    def ID(self ,t):
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
        return t

    
# --- Grammar
class SimpleParser(Parser):
    # uncomment the following line to output the parser logs
    debugfile = 'parser.out'
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
    
    @_('LSHIFTER ID')
    def expr(self, p):
        return (p.LSHIFTER, p.ID)

    @_('ID RSHIFTER')
    def expr(self, p):
        return (p.RSHIFTER, p.ID)

    @_('END')
    def end(self, p):
        return ("end", p.END)
    
    @_('end end')
    def end(self, p):
        return ("end")


lexer = SimpleLexer()
parser = SimpleParser()

example = """;;;  ; 
,,



'''~
'
>>    <
;
x"""

for tok in lexer.tokenize(example):
    print(f"type={tok.type}, value='{tok.value}'")

print(parser.parse(lexer.tokenize(example)))
