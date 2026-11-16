"""Spanish (CX8ANM test line): every text translated, the same {placeholders}, and the texts the
radio shows in U-Boot in plain ASCII (its console font has no accents)."""
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from x6100mb import i18n          # noqa: E402
from x6100mb import compose       # noqa: E402

RADIO = [compose.COUNTDOWN, compose.WAITING, compose.POWERING_OFF, "domyslny"]


class SpanishTest(unittest.TestCase):
    def test_every_english_text_has_spanish(self):
        missing = [k for k in i18n.EN if k not in i18n.ES]
        self.assertEqual(missing, [])

    def test_placeholders_match(self):
        for k, v in i18n.ES.items():
            self.assertEqual(sorted(re.findall(r"\{\w*\}", k)), sorted(re.findall(r"\{\w*\}", v)), k)

    def test_radio_texts_are_ascii(self):
        for k in RADIO + [k for k in i18n.ES if k.startswith("# ")]:
            self.assertTrue(i18n.ES[k].isascii(), i18n.ES[k])
        self.assertIn("${bm_left}", i18n.ES[compose.COUNTDOWN])

    def test_doom_readme(self):
        self.assertIn("es", i18n.DOOM_README)

    def test_locale_names(self):
        for loc, code in (("es_UY.UTF-8", "es"), ("Spanish_Uruguay", "es"), ("pl_PL", "pl"), ("en_US", "en")):
            self.assertEqual(i18n._code(loc), code)


if __name__ == "__main__":
    unittest.main()
