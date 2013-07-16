"""
Marketplace CLI - to make everyday things easy to work with Marketplace.
"""

import argparse
import yaml

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
        if path.exists('marketplacecli.yml'):
            args.config = 'marketplacecli.yml'
        elif path.exists(path.join(path.expanduser('~'),
                         'marketplacecli.yml')):
            args.config = path.join(path.expanduser('~'), 'marketplacecli.yml')
        else:
            parser.error('marketplacecli.yml not found. Use --config to '
                         'provide path or create a marketplace.yml in your '
                         'home directory or working directory.')

    with open(args.config, 'r') as config_file:
        config = yaml.load(config_file.read())

    if config.get(args.env, None) is None:
        raise Exception('Configuration for "%s" environment is missing. Add '
                        'configuration to marketplace.yml file.' % args.env)
    args.config = config.get(args.env)

    # do the work
    args.func(args)


if __name__ == '__main__':
    main()
