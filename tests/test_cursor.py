from StringIO import StringIO

from call_graph.cursor import Cursor


TEST_FILE_CONTENTS_1 = """\
line1
line2
"""


def test_cursor():
    cursor = Cursor(StringIO(TEST_FILE_CONTENTS_1))
    assert cursor.offset == 0
    assert cursor.buffer[cursor.get_offset(0, 0)] == 'l'
    assert cursor.looking_at('line1')
    assert cursor.buffer[cursor.get_offset(1, 3)] == 'e'
