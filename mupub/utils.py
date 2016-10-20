"""Utility functions for mupub.
"""
__docformat__ = 'reStructuredText'

import os
import argparse
import ruamel.yaml as yaml
import mupub.config


def _find_files(folder, outlist):
    for entry in os.scandir(path=folder):
        # ignore hidden and backup files
        if entry.name.startswith('.') or entry.name.endswith('~'):
            continue
        if entry.is_file():
            outlist.append(os.path.join(folder, entry.name))
        elif entry.is_dir():
            # recurse to get files under this folder
            outlist = _find_files(os.path.join(folder, entry.name), outlist)
    return outlist


def find_files(folder):
    """Return a list of all files in a folder

    :param str folder: The top-most folder.
    :returns: list of files under folder
    :rtype: list of strings

    """
    return _find_files(folder, [])


def resolve_input(infile=None):
    base = os.path.basename(os.getcwd())
    if not infile:
        if os.path.exists(base+'.ly'):
            infile = base+'.ly'
        elif os.path.exists(base+'-lys'):
            candidate = os.path.join(base+'-lys', base+'.ly')
            if os.path.exists(candidate):
                infile = candidate

    return base,infile


class ConfigDumpAction(argparse.Action):
    """Dump the configuration to stdout.

    An argparse action to dump configuration values.

    """

    def __init__(self, option_strings, dest, **kwargs):
        super(ConfigDumpAction, self).__init__(
            option_strings,
            dest,
            **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, True)
        print(yaml.dump(mupub.config.CONFIG_DICT,
                        Dumper=yaml.RoundTripDumper)
        )


class EnvDefault(argparse.Action):
    """Get values from environment variable.

    A custom argparse action that checks the environment for the value
    of an argument in the parser.

    """
    def __init__(self, env, required=True, default=None, **kwargs):
        default = os.environ.get(env, default)
        self.env = env
        if default:
            required = False
        super(EnvDefault, self).__init__(
            default=default,
            required=required,
            **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
