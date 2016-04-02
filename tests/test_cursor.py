from StringIO import StringIO

from call_graph.cursor import Cursor
from call_graph.cursor import Python
from call_graph.cursor import get_enclosing_function


TEST_FILE_CONTENTS_1 = """\
line1
line2
"""


TEST_FILE_CONTENTS_2 = """\
def fn1():
    fn2()
"""


def test_cursor():
    cursor = Cursor(StringIO(TEST_FILE_CONTENTS_1))
    assert cursor.offset == 0
    assert cursor.buffer[cursor.get_offset(0, 0)] == 'l'
    assert cursor.looking_at('line1')
    assert cursor.buffer[cursor.get_offset(1, 3)] == 'e'


def test_get_enclosing_function():
    cursor = Cursor(StringIO(TEST_FILE_CONTENTS_2), 1, 4)
    assert cursor.looking_at('fn2')
    assert get_enclosing_function(cursor, Python) == 'fn1'
