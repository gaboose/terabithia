import unittest
import sys, os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import bluesky

class TestFormatter(unittest.TestCase):

    def test_formatter(self):
        self.assertEqual(bluesky.format({
            'header': 'žodis',
            'uuid': 'mano_uuid',
            'details': {
                'Reikšmė ir vartosena': {
                    'Apibrėžtis': 'kalbos dalis.',
                    'Vartojimo sritys': 'šen, ten'
                }
            }
        }).build_text(), "✒️ žodis – kalbos dalis.\n#šen #ten")

        self.assertEqual(bluesky.format({
            'header': 'žodis',
            'uuid': 'mano_uuid',
            'details': {
                'Reikšmė ir vartosena': {
                    'Apibrėžtis': 'kalbos dalis.'
                }
            }
        }).build_text(), "✒️ žodis – kalbos dalis.")

if __name__ == '__main__':
    unittest.main()