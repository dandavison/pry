from contextlib import contextmanager
from unittest import TestCase
import os
import shutil
import tempfile

from pry.grep import ag as grep


TEST_FILE_CONTENTS_1 = """\
class TestGrep(TestCase):

    def setUpClass(cls):
        cls.directory = mkdtemp()
        os.chdir(cls.directory)
        with open('file.py', 'w') as fp:
            fp.write(TEST_FILE_CONTENTS_1)
"""


@contextmanager
def cd(directory):
    original_directory = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(original_directory)


class TestGrep(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.mkdtemp()
        cls.test_file_name_1 = 'test_file_1.py'
        with cd(cls.directory), open(cls.test_file_name_1, 'w') as fp:
            fp.write(TEST_FILE_CONTENTS_1)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.directory)

    def test_grep(self):
        with cd(self.directory):
            [hit] = grep('setUpClass')
        self.assertEqual(
            (hit.path, hit.i, hit.j, hit.text),
            (self.test_file_name_1, 2, 8, '    def setUpClass(cls):'))
        self.assertEqual(hit.get_indentation(), 4)

        with cd(self.directory):
            [hit] = grep('chdir')
        self.assertEqual(
            (hit.path, hit.i, hit.j, hit.text),
            (self.test_file_name_1, 4, 11, '        os.chdir(cls.directory)'))
        self.assertEqual(hit.get_indentation(), 8)
