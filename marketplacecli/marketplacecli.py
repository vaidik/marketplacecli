"""
Marketplace CLI - to make everyday things easy to work with Marketplace.
"""

import argparse
import ConfigParser

from os import path
from . import commands


def main():
    parser = argparse.ArgumentParser(description='Marketplace CLI - do '
                                                 'repititive things quickly.')
    parser.add_argument('--env', help='Environment: dev, stage, prod',
                        choices=['dev', 'stage', 'prod'], default='dev')
    parser.add_argument('--config', help='Configuration file.',
                        default=None)

    # Add sub-commands
    cmd = parser.add_subparsers(help='sub-command help')

    create_app = cmd.add_parser('create_apps', help='Create dummy apps and '
                                                    'submit them to '
                                                    'marketplace.')
    create_app.set_defaults(func=commands.create_app)

    '''
    create_app.add_argument('--packaged', help='Create a packaged app.')
    create_app.add_argument('--hosted', help='Create a hosted app.')
    create_app.add_argument('--premium', help='Premium type for app.')
    create_app.add_argument('--tier', help='Payment tier.')

    tiers = cmd.add_parser('tiers', help='Get Payment Tiers from marketplace.')
    tiers.set_defaults(func=commands.get_tiers)
    '''

    args = parser.parse_args()

    if args.config is None:
        if path.exists('marketplacecli.ini'):
            args.config = 'marketplacecli.ini'
        elif path.exists(path.join(path.expanduser('~'), 'marketplacecli.ini')):
            args.config = path.join(path.expanduser('~'), 'marketplacecli.ini')
        else:
            parser.error('marketplacecli.ini not found. Use --config to provide '
                         'path or create a marketplace.ini in your home'
                         'directory or working directory.')

    config = ConfigParser.ConfigParser()
    config.read(path.abspath(args.config))
    args.config = config

    # do the work
    args.func(args)


if __name__ == '__main__':
    main()
