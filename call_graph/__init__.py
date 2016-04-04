import logging
import re

from call_graph.grep import ag as grep
from call_graph.languages import Python

logger = logging.getLogger(__file__)
debug = logger.debug


def make_call_graph(function):
    debug('make_call_graph(%s)' % function)

    call_sites = grep(function)
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
