import argparse
import logging
import re

from pry.grep import ag as grep
from pry.languages import Python

logger = logging.getLogger(__file__)
debug = logger.debug

MAX_CALL_SITES = 50
TOO_MANY_CALL_SITES_MARKER = '<call_sites>'

def make_call_graph(function):
    debug('make_call_graph(%s)' % function)

    call_sites = grep(function)

    if len(call_sites) > MAX_CALL_SITES:
        return {
            TOO_MANY_CALL_SITES_MARKER: len(call_sites)
        }

    call_graph = {}
    for call_site in call_sites:
        debug('call_site: %s' % call_site)

        if re.match(Python.function_regex, call_site.text.strip()):
            debug('skipping definition')
            # It's the function definition; not a call
            continue

        parent_function = call_site.get_enclosing_function(Python)

        debug('parent_function: %s' % parent_function)

        if parent_function is not None and parent_function != function:
            call_graph[parent_function] = make_call_graph(parent_function)

    return call_graph


def print_call_graph(graph, level=0):
    indent = '    ' * level
    for key, subgraph in sorted(graph.items()):
        if key == TOO_MANY_CALL_SITES_MARKER:
            print('{indent}{key}: {subgraph}'.format(**locals()))
        else:
            print('{indent}{key}'.format(**locals()))
            print_call_graph(subgraph, level + 1)


def parse_arguments():
    arg_parser = argparse.ArgumentParser(
        description="Find call sites",
    )

    arg_parser.add_argument(
        'pattern',
        help="Pattern to search for",
    )

    return arg_parser.parse_args()


def main():
    args = parse_arguments()
    graph = make_call_graph(args.pattern)
    print_call_graph(graph)


if __name__ == '__main__':
    main()
