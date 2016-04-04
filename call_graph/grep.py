import re
import subprocess
from contextlib import contextmanager

PYTHON_INDENTATION = 4


class Cursor:

    def __init__(self, path, line, col, text=None):
        self.path = path
        self.i = int(line) - 1
        self.j = int(col) - 1
        self.text = text

        with open(self.path) as fp:
            self.buffer = fp.read()
        self.lines = self.buffer.splitlines()

    @property
    def pos(self):
        return self.i, self.j

    @pos.setter
    def pos(self, pos):
        self.i, self.j = pos

    @property
    def char(self):
        i, j = self.pos
        return self.lines[i][j]

    @property
    def ahead(self):
        i, j = self.pos
        return self.lines[i][j:]

    def looking_at(self, regex):
        return re.match(regex, self.ahead)

    @contextmanager
    def save_excursion(self):
        i, j = self.pos
        yield
        self.pos = i, j

    def get_enclosing_function(self, language):
        current_indentation = self.get_indentation()
        with self.save_excursion():
            self.j = 0
            while self.i:
                self.i -= 1
                match = self.looking_at(language.function_regex)
                if match:
                    indentation_text, function = match.groups()
                    if len(indentation_text) < current_indentation:
                        return function
        return None

    def get_indentation(self):
        with self.save_excursion():
            self.j = 0
            match = self.looking_at(r'( *)[^ ]')
            assert match
            indentation = len(match.groups()[0])
            assert not indentation % PYTHON_INDENTATION
            return indentation

    def __eq__(self, other):
        tuple(self) == tuple(other)


class Hit(Cursor):
    regex = None

    @classmethod
    def from_raw(cls, output):
        match = re.match(cls.regex, output.decode('utf-8'))
        if not match:
            raise ValueError(
                "Cannot parse output line: '%s'" % output)
        else:
            return cls(*match.groups())


class AgHit(Hit):
    regex = re.compile(r'([a-zA-Z0-9\./_-]+):(\d+):(\d+):(.+)')

    def __iter__(self):
        return iter((self.path, self.i, self.j, self.text))

    def __repr__(self):
        return '%s:%d:%d:%s' % tuple(self)


def ag(pattern):
    output = subprocess.check_output([
        'ag', '--noheading', '--column', '--nobreak',
        '%s' % pattern,
    ])
    return list(map(AgHit.from_raw, output.strip().splitlines()))


class GitGrepHit(Hit):
    regex = re.compile(r'([a-zA-Z0-9\./_-]+):(\d+):(.+)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.col = None

    def __iter__(self):
        return iter((self.path, self.i, self.text))

    def __repr__(self):
        return '%s:%d:%s' % tuple(self)


def git_grep(pattern):
    output = subprocess.check_output([
        'git', 'grep', '-n',
        '%s' % pattern,
    ])
    return list(map(GitGrepHit.from_raw, output.strip().splitlines()))
