from victims import shoptridung
from chrome_fingerprints import FingerprintGenerator

import capsolver
capsolver.api_key = "CAP-FFE2271E0A6E1961C4FB2BF717C81F0D"


fp_gen = FingerprintGenerator()
victim = shoptridung('brZgipEN:OvBNcLMk@171.235.160.120:21001', fp_gen)
victim.run()
