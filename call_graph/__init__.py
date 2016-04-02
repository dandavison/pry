from git_grep import grep


def get_call_sites(pattern):
    hits = grep(pattern).strip().splitlines()
    return hits
