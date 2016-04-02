import subprocess


def grep(pattern):
    return subprocess.check_output(['git', 'grep', '%s' % pattern])
