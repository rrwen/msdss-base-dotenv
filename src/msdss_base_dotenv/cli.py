import argparse

from .core import *

def _get_parser():
    """
    Builds an ``argparse`` parser for the ``msdss-dotenv`` command line tool.

    Returns
    -------
    :class:`argparse.ArgumentParser`
        An ``argparse`` parser for ``msdss-dotenv``.

    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>

    Example
    -------

    .. jupyter-execute::
        :hide-output:

        from msdss_base_dotenv.cli import _get_parser

        parser = _get_parser()
        parser.print_help()

    """

    # (_get_parser__parsers) Create main parser and sub parsers
    parser = argparse.ArgumentParser(description='Manages encrypted .env files')
    subparsers = parser.add_subparsers(title='commands', dest='command')

    # (_get_parser__init) Add init command
    init_parser = subparsers.add_parser('init', help='create env file and key')
    
    # (_get_parser__set) Add set command
    set_parser = subparsers.add_parser('set', help='set an env var')
    set_parser.add_argument('name', type=str, help='env var name to set')
    set_parser.add_argument('value', type=str, help='env var value to set')

    # (_get_parser__del) Add del command
    del_parser = subparsers.add_parser('del', help='delete an env var')
    del_parser.add_argument('name', type=str, help='env var name to delete')

    # (_get_parser__clear) Add clear command
    clear_parser = subparsers.add_parser('clear', help='clear env file and key')

    # (_get_parser__file_key) Add file and key arguments to all commands
    for p in [parser, init_parser, set_parser, del_parser, clear_parser]:
        p.add_argument('--file_path', type=str, default='./.env', help='path of .env file')
        p.add_argument('--key_path', type=str, default=None, help='path of key file')
    
    # (_get_parser_out) Return the parser
    out = parser
    return out

def run():
    """
    Runs the ``msdss-dotenv`` command.

    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>

    Example
    -------
    >>> msdss-dotenv --help

    .. jupyter-execute::
        :hide-code:

        from msdss_base_dotenv.cli import _get_parser

        parser = _get_parser()
        parser.print_help()

    Initialize env and key files (run this first):

    >>> msdss-dotenv init

    Set ``USER`` var to ``msdss``:

    >>> msdss-dotenv set USER msdss

    Remove ``USER`` var:

    >>> msdss-dotenv del USER

    Clear env and key files:

    >>> msdss-dotenv clear
    """

    # (run_kwargs) Get arguments and command
    parser = _get_parser()
    kwargs = vars(parser.parse_args())
    command = kwargs.pop('command')

    # (run_command) Run commands
    if command == 'init':
        if env_exists(**kwargs):
            print('Environmental variable files already initialized.')
        else:
            save_env_file(env={}, **kwargs)
    elif command == 'set':
        set_env_var(**kwargs)
    elif command == 'del':
        del_env_var(**kwargs)
    elif command == 'clear':
        clear_env_file(**kwargs)
    else:
        parser.print_help()