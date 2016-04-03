import re
import subprocess


class Hit:
    regex = re.compile(r'([a-zA-Z0-9\./_-]+):(\d+):(.+)')

    def __init__(self, path, line, text):
        self.path = path
        self.line = int(line)
        self.text = text

    def __repr__(self):
        return '%s:%d:%s' % tuple(self)

    @classmethod
    def from_raw(cls, output):
        match = re.match(Hit.regex, output.decode('utf-8'))
        if not match:
            raise ValueError(
                "Cannot parse git grep output line: '%s'" % output)
        else:
            return cls(*match.groups())

    def __iter__(self):
        return iter((self.path, self.line, self.text))


def grep(pattern):
    output = subprocess.check_output([
        'git', 'grep', '-n',
        '%s' % pattern,
    ])
    return map(Hit.from_raw, output.strip().splitlines())
