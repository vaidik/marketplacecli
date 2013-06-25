"""
Marketplace CLI - to make everyday things easy to work with Marketplace.
"""

import Queue
import signal

from . import app
from marketplace import Client
from marketplace.auth import OAuth


try:
    from gevent import monkey
    monkey.patch_all()
finally:
    import threading

DOMAINS = {
    'dev': 'marketplace-dev.allizom.org',
    'stage': 'marketplace.allizom.org',
    'prod': 'marketplace.mozilla.org',
}


def get_client(args):
    config = args.config
    client = Client(domain=DOMAINS[args.env],
                    auth=OAuth(consumer_secret=config.get('oauth',
                                                          'consumer_secret'),
                               consumer_key=args.config.get('oauth',
                                                            'consumer_key')))
    return client


def _print_table_row(row):
    column = '%25s\t| '
    to_print = column * len(row)
    print to_print % tuple(row)


def create_app(args):
    client = get_client(args)

    class ThreadCreateApp(threading.Thread):
        def __init__(self, queue):
            threading.Thread.__init__(self)
            self.queue = queue

        def run(self):
            while self.queue.qsize():
                tier = self.queue.get()

                try:
                    app_details = app.create_app(client, tier['price'])
                    _print_table_row([app_details['name'],
                                      app_details['price'],
                                      tier['localized']['locale'],
                                      ('https://%s/developers/app/%s/edit' %
                                       (DOMAINS[args.env], app_details['slug'])
                                       )])
                except Exception, exc:
                    print '**** Failure ****'
                    print 'Ignoring error: %s: %s' % (
                        exc.__class__.__name__, exc)
                    print '**** Failure ****'

    queue = Queue.Queue()
    tiers = app.get_tiers(client)

    for tier in tiers:
        queue.put(tier)

    def sigint_handler(signum, frame):
        print 'Exiting'
        while not queue.empty():
            queue.get()

        print 'Interrupted. Exiting...'

    signal.signal(signal.SIGINT, sigint_handler)

    threads = []
    for i in range(3):
        t = ThreadCreateApp(queue)
        t.setDaemon(True)
        t.start()
        threads.append(t)

    _print_table_row(['APP NAME', 'TIER', 'PRICE', 'REVIEWER TOOLS URL'])
    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        import sys
        print 'Exiting...'
        sys.exit(1)

    print 'Complete.'


def get_tiers(args):
    print 'Getting payment tiers from marketplace...'
    tiers = app.get_tiers()
