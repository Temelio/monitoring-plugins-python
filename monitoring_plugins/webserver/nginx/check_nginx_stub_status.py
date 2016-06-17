"""
Monitoring plugin to check Nginx stub status page output
"""

import argparse
import nagiosplugin

from temelio_monitoring.resource.webserver.nginx import StubStatusPage
from temelio_monitoring.context.connection import ConnectionCount

from temelio_monitoring.cli_parser import CommonParser
from temelio_monitoring.cli_parser.authentication import \
    UsernameParser, PasswordParser
from temelio_monitoring.cli_parser.connection import \
    ActiveConnectionParser, WaitingConnectionParser
from temelio_monitoring.cli_parser.web import UrlParser


def parse_args():
    """
    Manage plugin arguments
    """

    parser = argparse.ArgumentParser(
        description=('Check output of Nginx stub status page.'),
        parents=[
            CommonParser(),
            UsernameParser(),
            PasswordParser(),
            ActiveConnectionParser(),
            WaitingConnectionParser(),
            UrlParser(required=True)
        ]
    )

    return parser.parse_args()


@nagiosplugin.guarded
def main():
    """
    Entry point of monitoring plugin
    """

    # Specific metric used with metric context
    contexts = ['active_connections', 'active_waiting']

    # Parse plugin arguments
    args = parse_args()

    # Manage check components
    check = nagiosplugin.Check(
        StubStatusPage(
            url=args.url,
            username=args.username,
            password=args.password,
            contexts=contexts),
        ConnectionCount(
            'active_connections',
            args.warn_active_connection,
            args.crit_active_connection),
        ConnectionCount(
            'active_waiting',
            args.warn_waiting_connection,
            args.crit_waiting_connection),
    )

    # Execute check
    check.main(args.verbose, args.timeout)


if __name__ == '__main__':
    main()
