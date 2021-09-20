from dataclasses import dataclass

# default velocity: mezzo forte
VELOCITY = 64 

def to_midi_value(n, up=0, sharp=0):
  #Octave 4, the default
  notes = {
    "C": 72,
    "Cs": 73,
    "D": 74,
    "Ds": 75,
    "E": 76,
    "F": 77,
    "Fs": 78,
    "G": 79,
    "Gs": 80,
    "A": 81,
    "As": 82,
    "B": 83
  }
  val = notes.get(n, 72)
  val = val + up * 12 + sharp
  return val


class ParserError(Exception):
    pass


@dataclass
class Data:
    data: int
    data2: int = VELOCITY

    @classmethod
    def from_grammar(cls, *g):
        """
        Accepts grammar like:
        'E'
        ('A', 2, 'up')
        ('C', 1, 'sharp')
        (('G', 2, 'sharp'), 2, 'down')
        
        """
        g = g[0]
        if len(g) == 1:
            val = to_midi_value(g)
            return Data(val)

        elif len(g) == 3:
            def _parse_directive(val, directive):
                up = 0
                if directive == "up":
                    up = 1 * val
                if directive == "down":
                    up = -1 * val

                sharp = 0
                if directive == "sharp":
                    sharp += val
                if directive == "flat":
                    sharp -= val
                return up, sharp

            up, sharp = _parse_directive(g[1], g[2])
            e = g[0]
            if len(e) == 3:
                up0, sharp0 = _parse_directive(e[1], e[2])
                up = up + up0
                sharp = sharp + sharp0
                e = e[0]
            return Data(to_midi_value(e, up, sharp))
        else:
            raise ParserError(f"Malformed parsed message {g}")



@dataclass
class Message:
    """A proxy for midi message

    Accept grammar like:
    'E'
    ('E', 1)
    ('A', 2, 'up')
    (('G', 2, 'sharp'), 2, 'down')
    ((('E', 1, 'flat'), 2, 'up'), 3)
    
    """
    time: float
    status: int
    data: Data


if __name__ == '__main__':
    print(Data.from_grammar("C"))
    print(Data.from_grammar(('A', 2, 'up')))
    print(Data.from_grammar(('C', 1, 'sharp')))
    print(Data.from_grammar((('G', 2, 'sharp'), 2, 'down')))