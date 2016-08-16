import os
import sys
import logging
import argparse

from eva.utils.importlib import import_module
from eva.conf import settings

CURDIR = os.path.dirname(os.path.realpath(__file__))


# cache
COMMANDS = {}


def exec_command_file(filepath):
    global_namespace = {
        "__file__": filepath,
        "__name__": "__main__",
        }
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)
    return global_namespace.get('Command') 


def load_commands():
    global COMMANDS

    if len(COMMANDS) == 0:
        dirs = [os.path.join(CURDIR, 'commands')]
        dirs.extend(list(settings.MANAGEMENT_COMMAND_DIRS))
        for cmdDir in dirs:
            for f in os.listdir(cmdDir):
                if not f.endswith('.py'):
                    continue
    
                cmdFile = os.path.join(cmdDir, f)
                Command = exec_command_file(cmdFile)

                if not Command:
                    logging.warn('%s is not a Command Module!', cmdFile)
                    continue
    
                c = Command()
    
                if not (hasattr(c, 'cmd') and
                        hasattr(c, 'help') and
                        hasattr(c, 'run')):
                    logging.warn('%s is not a Command Module!', os.path.join(CURDIR, f))
                    continue
    
                COMMANDS[c.cmd] = c

    return COMMANDS


def print_usage():
    print('''{prog} - Eva Management Tools

Usage:

    {prog} SUBCOMMAND OPTIONS

Help:

    {prog} help | -h | --help

Subcommand:
'''.format(prog=sys.argv[0]))
    global COMMANDS
    for k in COMMANDS:
        c = COMMANDS[k]
        print('    {cmd:16} {help}'.format(cmd=c.cmd, help=c.help))
    print()


def main(argv=sys.argv[1:]):

    load_commands()

    if len(argv) == 0:
        print_usage()
        sys.exit(1)

    cmd = argv[0]
    global COMMANDS

    if cmd in COMMANDS:
        argv = argv[1:] if len(argv) > 1 else []
        COMMANDS[cmd](argv)

    elif cmd in ['help', '-h', '--help']:
        print_usage()

    else:
        print('unknown cmd: ', cmd)
