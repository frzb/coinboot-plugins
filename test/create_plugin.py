#!/usr/bin/python3

"""Create Coinboot Plugins

Usage:
  create_plugin start
  create_plugin finish <plugin-name>

Options:
  -h --help     Show this screen.

"""

import os
import tarfile
import re
from docopt import docopt
from fnmatch import fnmatch
from subprocess import call

DPKG_STATUS = '/var/lib/dpkg/status'
INITIAL_DPKG_STATUS = '/tmp/initial_status'
FINAL_DPKG_STATUS = '/tmp/dpkg_status'
PLUGIN_DIR = '/mnt/plugin/rootfs'

exclude = ('/dev',
           '/proc',
           '/run',
           '/sys',
           '/tmp',
           '/usr/share/dbus-1/system-services',
           '/vagrant',
           '/var/cache',
           '/var/lib/dpkg/[^info]',
           '/var/log',
           '.*__pycache__.*'
           )


def find(pathin):
    """Return results similar to the Unix find command run without options
    i.e. traverse a directory tree and return all the file paths
    """
    return [os.path.join(path, file)
            for (path, dirs, files) in os.walk(pathin)
            for file in files]

def main(arguments):
    #print(arguments)
    if arguments['start']:
         call(['cp', '-v', DPKG_STATUS, INITIAL_DPKG_STATUS])
    elif arguments['finish']:
        f = open(FINAL_DPKG_STATUS, 'w')
        call(['dpkg_status.py', '--old', 'INITIAL_DPKG_STATUS', '--new', 'DPKG_STATUS', '--diff'], stdout=f)

        valid_files = []

        for path in  find(PLUGIN_DIR):
            if any(re.findall(pattern, path) for pattern in exclude):
                print('Ignore:', path)
            else:
                print(' Valid:', path)
                valid_files.append(path)

        tar = tarfile.open("sample.tar.gz", "w:gz")
        for name in ["foo", "bar", "quux"]:
            tar.add(name)
        tar.close()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Create Coinboot Plugins v0.1')
    main(arguments)


