
import unittest
import os

from .decoder import decode

class TestDecode(unittest.TestCase):
    def assert_decodes_to(self, fixturename, correct):
        srcpath = os.path.dirname(os.path.abspath(__file__))
        fixture = os.path.join(srcpath, 'fixtures', fixturename)

        with open(fixture, 'rb') as f:
            self.assertEqual(correct, str(decode(f)))

    def test_1(self):
        correct = '''Saved with HW Version: 0.808-alpha
Tempo: 120
(0) kick	|x---|x---|x---|x---|
(1) snare	|----|x---|----|x---|
(2) clap	|----|x-x-|----|----|
(3) hh-open	|--x-|--x-|x-x-|--x-|
(4) hh-close	|x---|x---|----|x--x|
(5) cowbell	|----|----|--x-|----|
'''
        self.assert_decodes_to('pattern_1.splice', correct)

    def test_2(self):
        correct = '''Saved with HW Version: 0.808-alpha
Tempo: 98.4
(0) kick	|x---|----|x---|----|
(1) snare	|----|x---|----|x---|
(3) hh-open	|--x-|--x-|x-x-|--x-|
(5) cowbell	|----|----|x---|----|
'''
        self.assert_decodes_to('pattern_2.splice', correct)

    def test_3(self):
        correct = '''Saved with HW Version: 0.808-alpha
Tempo: 118
(40) kick	|x---|----|x---|----|
(1) clap	|----|x---|----|x---|
(3) hh-open	|--x-|--x-|x-x-|--x-|
(5) low-tom	|----|---x|----|----|
(12) mid-tom	|----|----|x---|----|
(9) hi-tom	|----|----|-x--|----|
'''
        self.assert_decodes_to('pattern_3.splice', correct)

    def test_4(self):
        correct = '''Saved with HW Version: 0.909
Tempo: 240
(0) SubKick	|----|----|----|----|
(1) Kick	|x---|----|x---|----|
(99) Maracas	|x-x-|x-x-|x-x-|x-x-|
(255) Low Conga	|----|x---|----|x---|
'''
        self.assert_decodes_to('pattern_4.splice', correct)

    def test_5(self):
        correct = '''Saved with HW Version: 0.708-alpha
Tempo: 999
(1) Kick	|x---|----|x---|----|
(2) HiHat	|x-x-|x-x-|x-x-|x-x-|
'''
        self.assert_decodes_to('pattern_5.splice', correct)




