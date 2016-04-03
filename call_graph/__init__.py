from call_graph.cursor import Cursor
from call_graph.cursor import Python
from call_graph.cursor import get_enclosing_function
from call_graph.git_grep import grep


def make_call_graph(pattern):
    return {
        caller: make_call_graph(caller)
        for caller in get_callers(pattern)
    }


def get_callers(pattern):
    print(pattern)
    hits = grep(pattern)
    for hit in hits:
        with open(hit.path) as fp:
            cursor = Cursor(fp, line=hit.line)
        yield get_enclosing_function(cursor, Python)
