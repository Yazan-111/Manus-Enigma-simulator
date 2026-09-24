"""Educational Enigma emulator: Wehrmacht M3 and Kriegsmarine M4 variants."""
from dataclasses import dataclass
from math import factorial
from typing import Iterable

ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ROTOR_WIRINGS = {
    "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    "IV": ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    "V": ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
    "VI": ("JPGVOUMFYQBENHZRDKASXLICTW", "ZM"),
    "VII": ("NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM"),
    "VIII": ("FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM"),
}
REFLECTORS = {
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
}

@dataclass
class Rotor:
    name: str
    position: int = 0
    ring: int = 0

    @property
    def wiring(self):
        return ROTOR_WIRINGS[self.name][0]

    @property
    def notches(self):
        return ROTOR_WIRINGS[self.name][1]

    def at_notch(self):
        return ABC[self.position] in self.notches

    def forward(self, value: int) -> int:
        offset = (value + self.position - self.ring) % 26
        mapped = ABC.index(self.wiring[offset])
        return (mapped - self.position + self.ring) % 26

    def reverse(self, value: int) -> int:
        offset = (value + self.position - self.ring) % 26
        mapped = self.wiring.index(ABC[offset])
        return (mapped - self.position + self.ring) % 26

class Enigma:
    def __init__(self, rotors: Iterable[str] = ("I", "II", "III"), reflector="B", positions="AAA", rings="AAA", plugs=""):
        names = tuple(rotors)
        if len(names) not in (3, 4):
            raise ValueError("Enigma supports 3 or 4 rotors")
        if any(n not in ROTOR_WIRINGS for n in names):
            raise ValueError("Unknown rotor")
        if reflector not in REFLECTORS:
            raise ValueError("Unknown reflector")
        if len(positions) != len(names) or len(rings) != len(names):
            raise ValueError("Positions and rings must match rotor count")
        self.rotors = [Rotor(n, ABC.index(p), ABC.index(r)) for n, p, r in zip(names, positions, rings)]
        self.reflector = reflector
        self.plugboard = self._parse_plugs(plugs)
        self.steps = 0

    @staticmethod
    def _parse_plugs(plugs: str):
        plugs = plugs.replace(" ", "").upper()
        if len(plugs) % 2 or len(set(plugs)) != len(plugs) or any(c not in ABC for c in plugs):
            raise ValueError("Plugboard must contain unique A-Z pairs")
        mapping = {c: c for c in ABC}
        for a, b in zip(plugs[::2], plugs[1::2]):
            mapping[a], mapping[b] = b, a
        return mapping

    def _step(self):
        # Rightmost wheel always advances. Middle wheel double-steps at its notch.
        if len(self.rotors) == 3:
            left, middle, right = self.rotors
        else:
            left, middle, right = self.rotors[-3:]
        middle_step = middle.at_notch()
        left_step = middle_step or right.at_notch()
        if left_step:
            left.position = (left.position + 1) % 26
        if middle_step or right.at_notch():
            middle.position = (middle.position + 1) % 26
        right.position = (right.position + 1) % 26
        self.steps += 1

    def transform(self, text: str) -> str:
        out = []
        for ch in text.upper():
            if ch not in ABC:
                continue
            self._step()
            x = ABC.index(self.plugboard[ch])
            for rotor in reversed(self.rotors):
                x = rotor.forward(x)
            x = ABC.index(REFLECTORS[self.reflector][x])
            for rotor in self.rotors:
                x = rotor.reverse(x)
            out.append(self.plugboard[ABC[x]])
        return "".join(out)

def plugboard_total():
    return sum(factorial(26) // (factorial(26 - 2*p) * factorial(p) * (2 ** p)) for p in range(14))

def keyspace(version: str):
    if version == "commercial-d":
        return {"rotor_orders": 3 * 2 * 1, "positions": 26**3, "rings": 26**3, "plugboard": 1, "total": 6 * 26**6}
    if version == "wehrmacht-m3":
        return {"rotor_orders": 5 * 4 * 3, "positions": 26**3, "rings": 26**3, "plugboard": plugboard_total(), "total": 60 * 26**6 * plugboard_total()}
    if version == "kriegsmarine-m4":
        # Simplified educational count: choose/order 4 from 8, plus positions/rings and plugboard.
        return {"rotor_orders": 8 * 7 * 6 * 5, "positions": 26**4, "rings": 26**4, "plugboard": plugboard_total(), "total": (8 * 7 * 6 * 5) * 26**8 * plugboard_total()}
    raise ValueError("Unknown version")

VERSIONS = [
    {"id":"commercial-d","year":"1926–1932","name":"Commercial Enigma D","rotors":3,"rotor_pool":"I–III (illustrative)","reflector":"Settable reflector","plugboard":False,"summary":"Commercial three-rotor platform. No military plugboard; compact lamp-panel design."},
    {"id":"wehrmacht-m3","year":"1932–1941","name":"Wehrmacht Enigma I / M3","rotors":3,"rotor_pool":"5 Army rotors","reflector":"B or C","plugboard":True,"summary":"The Wehrmacht revision adds the front Steckerbrett. From 1939, operators received five rotors and selected three."},
    {"id":"kriegsmarine-m4","year":"1942–1945","name":"Kriegsmarine M4","rotors":4,"rotor_pool":"8 Navy rotors + thin fourth wheel","reflector":"Thin B or C","plugboard":True,"summary":"U-boat M4 adds a fourth wheel and thin reflector. The fourth wheel does not step in the same way as the fast three."},
]

def version_details():
    result = []
    for v in VERSIONS:
        item = dict(v)
        item["keyspace"] = keyspace(v["id"])
        result.append(item)
    return result
