
import binascii
import struct
import math

class Track(object):
    _div = 4

    def __init__(self, id, name, steps):
        self.id = id
        self.name = name
        self.steps = steps

    def notes(self):
        qns = list(_chunked(self._div, self.steps))

        assert len(qns) == self._div
        assert all(len(qn) == self._div for qn in qns)

        return qns

    def __str__(self):
        template = '({id}) {name}\t{steps}'

        stepsstring = '|' + '|'.join(''.join('x' if step else '-'
                                             for step in note)
                                     for note in self.notes()) + '|'

        return template.format(id=self.id,
                               name=self.name,
                               steps=stepsstring)

class Song(object):
    def __init__(self, version, tempo, tracks):
        self.version = version
        self.tempo = tempo
        self.tracks = tracks

    def __str__(self):
        template = '''Saved with HW Version: {version}
Tempo: {tempo}
{tracks}\n'''

        tracksstring = '\n'.join(str(track)
                                 for track in self.tracks)

        tempo_is_int = self.tempo.is_integer()

        tempo = int(self.tempo) if tempo_is_int else round(self.tempo, 1)

        return template.format(version=self.version,
                               tempo=tempo,
                               tracks=tracksstring)

def decode(f):
    """ Decode a Splice drum machine file. """

    signature, size, version = _header(f)

    if signature != 'SPLICE':
        raise ValueError('Could not decode file contents.')
    else:
        tempo, tracks = _body(f, size)

        return Song(version=version,
                    tempo=tempo,
                    tracks=[Track(id, name, steps)
                            for id, name, steps in tracks])

def _trimright(string):
    return string.rstrip('\0')

def _header(f):
    headerstruct = ('>' '6s' 'q' '32s')

    signature, size, version = struct.unpack(headerstruct, f.read(46))

    return (signature, size, _trimright(version))

def _body(f, size):
    tempo, = struct.unpack('f', f.read(4))

    tracks = []
    while f.tell() < size:
        tracks.append(_track(f))

    return (tempo, tracks)

def _track(f):
    id, name = _trackheader(f)
    steps = _trackbody(f)

    steps_ = ''.join('x' if step else '-' for step in steps)

    return (id, name, steps)

def _trackheader(f):
    headerstruct = ('>' '1s' 'I')

    id, namelen = struct.unpack(headerstruct, f.read(5))

    namestruct = '>{length}s'.format(length=namelen)

    name, = struct.unpack(namestruct, f.read(namelen))

    return (ord(id), name)

def _trackbody(f):
    steps = list(struct.unpack('>16?', f.read(16)))
    assert len(steps) == 16
    return steps

def _chunked(size, sliceable):
    length = int(math.ceil(len(sliceable) / float(size)))
    for i in xrange(length):
        offset = i * size
        yield tuple(sliceable[offset:offset+size])


