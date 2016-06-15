import os
import sys
import logging
import argparse

from eva.utils.importlib import import_module

CURDIR = os.path.dirname(os.path.realpath(__file__))


# cache
COMMANDS = {}


def load_commands():
    global COMMANDS

    if len(COMMANDS) == 0:
        for f in os.listdir(os.path.join(CURDIR, 'commands')):
            if not f.endswith('.py'):
                continue

            m = import_module('eva.management.commands.{0}'.format(f[:-3]))
            if not hasattr(m, 'Command'):
                logging.warn('%s is not a Command Module!', os.path.join(CURDIR, f))
                continue

            c = m.Command()

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
