import unittest
import sys, os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import parser

def save_json(fname):
    with open(fname, 'w') as file:
        json.dump(actual_details, file, indent=2, ensure_ascii=False)

class TestStringMethods(unittest.TestCase):

    def test_parser(self):
        with open('view_html_1.html', 'r') as file:
            actual_details = parser.parse_html_details(file.read())
        with open('view_html_1.expected.json', 'r') as file:
            expected_details = json.load(file)
        self.assertEqual(actual_details, expected_details)

if __name__ == '__main__':
    unittest.main()