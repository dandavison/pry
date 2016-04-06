import ast


def get_defs(filename):
    _ast = ast.parse(open(filename).read())

    defs = {}

    def _get_defs(node, path):
        for child in node.body:
            if isdef(child):
                _get_defs(child, path + [child.name])
        if isdef(node):
            defs[node.lineno, node.col_offset] = path

    _get_defs(_ast, [])

    return {k: '.'.join(v) for k, v in defs.items()}


def isdef(node):
    return type(node) in {ast.FunctionDef, ast.ClassDef}


if __name__ == '__main__':
    import pprint
    import sys
    (filename,) = sys.argv[1:]
    pprint(get_defs(filename))
