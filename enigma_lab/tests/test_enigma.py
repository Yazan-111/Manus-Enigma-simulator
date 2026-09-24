import unittest
from enigma import Enigma, keyspace, plugboard_total

class EnigmaTests(unittest.TestCase):
    def test_reciprocal_transform(self):
        settings = dict(rotors=("I","II","III"), reflector="B", positions="AAA", rings="AAA", plugs="AV BS CG DL FU HZ IN KM OW RX")
        plain = "THEEAGLEHASLANDED"
        cipher = Enigma(**settings).transform(plain)
        self.assertNotEqual(cipher, plain)
        self.assertEqual(Enigma(**settings).transform(cipher), plain)

    def test_plugboard_total(self):
        self.assertEqual(plugboard_total(), 532985208200576)

    def test_versions_have_expected_shapes(self):
        self.assertEqual(keyspace("commercial-d")["rotor_orders"], 6)
        self.assertEqual(keyspace("wehrmacht-m3")["rotor_orders"], 60)
        self.assertEqual(keyspace("kriegsmarine-m4")["positions"], 26**4)

    def test_invalid_plug(self):
        with self.assertRaises(ValueError):
            Enigma(plugs="AA")

if __name__ == '__main__':
    unittest.main()
