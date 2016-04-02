from call_graph.cursor import Cursor
from call_graph.cursor import Python
from call_graph.cursor import get_enclosing_function
from call_graph.git_grep import grep


def get_call_sites(pattern):
    hits = grep(pattern)
    for hit in hits:
        with open(hit.path) as fp:
            cursor = Cursor(fp, line=hit.line)
        function = get_enclosing_function(cursor, Python)

        print('%s:%d:%-90s %s' % (tuple(hit) + (function,)))
