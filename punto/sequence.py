from dataclasses import dataclass

# default velocity: mezzo forte
VELOCITY = 64 

def to_midi_value(n, up=0):
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
  val = notes.get(n)
  val = val + up * 12
  return val


@dataclass
class Data:
    data: int
    data2: int = VELOCITY

    @classmethod
    def from_grammar(cls, g):
        if len(g) == 1:
            data = to_midi_value(g)
            return Data(data, cls.data2)



@dataclass
class Message:
    """A proxy for midi message"""
    time: float
    status: int
    data: Data


if __name__ == '__main__':
    d = Data.from_grammar("C")
    m = Message(0.0, 0, d)
    print(d)
    print(m)