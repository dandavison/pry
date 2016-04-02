import re


class Cursor:

    def __init__(self, fp, line=0, col=0):
        self.buffer = fp.read()
        self.offset = self.get_offset(line, col)

    @property
    def ahead(self):
        return self.buffer[self.offset:]

    def looking_at(self, regex):
        return re.match(regex, self.ahead)

    def get_offset(self, line_num, col_num):
        lines = self.buffer.splitlines()
        return sum(len(line) + 1
                   for line in lines[:line_num]) + col_num
