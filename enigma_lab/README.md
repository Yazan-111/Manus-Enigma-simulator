# Rotor Lab — Enigma Emulator

Rotor Lab is a self-contained Python/Flask educational emulator of three important Enigma stages: the commercial Enigma D baseline, the Wehrmacht Enigma I / M3, and the Kriegsmarine M4. It includes a local web interface with a procedural Three.js model, historical timeline, keyspace arithmetic, rotor settings, plugboard input, and reciprocal enciphering.

## Run locally

```bash
cd enigma_lab
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. The Three.js runtime is vendored in `static/js/three.min.js`, so the interactive model works without a package build step. Google Fonts are an optional enhancement; the interface falls back to system fonts if offline.

## Scope and historical accuracy

The implementation models the historically important signal path: plugboard, right-to-left rotor traversal, reflector, return traversal, reciprocal substitution, ring settings, and the double-stepping behavior of the moving three-wheel stack. It uses published Wehrmacht rotor wirings I–V, Navy rotor wirings VI–VIII, and reflectors B/C.

The 3D object is a **procedural educational visualization**, not a museum-grade CAD scan. It intentionally communicates the physical arrangement and differences between variants without claiming the user's requested “99% similarity.” A production museum replica would require a specific surviving serial-numbered machine, measured dimensions, and reference photography. The UI also avoids Veritasium logos, fonts, and proprietary assets. Its visual language is an original high-contrast science-editorial treatment using red, yellow, black, and warm paper tones.

The keyspace cards are labeled as configuration counts. They do not represent the effective work factor of historical attacks, which depended on traffic procedures, cribs, operator mistakes, captured material, Bombe search methods, and model-specific constraints. The M4 count is explicitly a simplified educational count based on the same components plus four rotor positions/rings; the fourth wheel's historically specific selection rules and thin-reflector compatibility deserve a separate research mode.

## Historical timeline used in the app

The commercial baseline is based on the 1926–1932 Enigma D lineage: three rotors, a reflector, and no military plugboard. The 1932 Wehrmacht revision added the Steckerbrett. From 1939 the Army and Air Force were supplied with five rotors from which three were selected. The Kriegsmarine M3 used an eight-rotor pool, and early in 1942 the U-boat M4 added a fourth wheel and thin reflector.

The referenced Veritasium video is used as an explanatory source for the machine's physical/electrical concepts and the codebreaking narrative. The historical details and arithmetic are cross-checked against the Crypto Museum, Cipher Machines and Cryptology, NSA historical mathematics publication, and Carnegie Mellon University Libraries.

## Tests

```bash
python -m unittest discover -s tests -v
```

The tests cover reciprocal encryption/decryption, stepping, plugboard validation, and keyspace totals.

## References

[1]: https://youtu.be/JsBZOcqZerk "Veritasium, The Insane Real Engineering of the Nazis' Enigma"
[2]: https://www.cryptomuseum.com/crypto/enigma/working.htm "Crypto Museum, Enigma explained"
[3]: https://www.ciphermachinesandcryptology.com/en/enigma.htm "Cipher Machines and Cryptology, The German Enigma Cipher Machine"
[4]: https://www.nsa.gov/portals/75/documents/about/cryptologic-heritage/historical-figures-publications/publications/wwii/CryptoMathEnigma_Miller.pdf "NSA, The Cryptographic Mathematics of Enigma"
[5]: https://www.cmu.edu/news/stories/archives/2019/october/inside-the-engima-machine.html "Carnegie Mellon University, Inside the Enigma Machine"
