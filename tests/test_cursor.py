import os
import tempfile
from unittest import TestCase

from call_graph.grep import Cursor
from call_graph.languages import Python


TEST_FILE_CONTENTS_1 = """\
line1
line2
"""


TEST_FILE_CONTENTS_2 = """\
def fn1():
    fn2()
"""


class TestGrep(TestCase):

    @classmethod
    def setUpClass(cls):
        _, cls.test_file_1 = tempfile.mkstemp()
        with open(cls.test_file_1, 'w') as fp:
            fp.write(TEST_FILE_CONTENTS_1)

        _, cls.test_file_2 = tempfile.mkstemp()
        with open(cls.test_file_2, 'w') as fp:
            fp.write(TEST_FILE_CONTENTS_2)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_file_1)
        os.remove(cls.test_file_2)

    def test_cursor(self):
        cursor = Cursor(self.test_file_1, 1, 1)
        assert cursor.looking_at('line1')

    def test_get_enclosing_function(self):
        cursor = Cursor(self.test_file_2, 2, 5)
        assert cursor.looking_at('fn2')
        assert cursor.get_enclosing_function(Python) == 'fn1'
