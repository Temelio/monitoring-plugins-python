"""
Monitoring plugin to check Redis INFO data
"""

import argparse
import nagiosplugin

from temelio_monitoring.resource.database.redis import ScalarInfoValue

from temelio_monitoring.cli_parser import CommonParser
from temelio_monitoring.cli_parser.authentication import PasswordParser
from temelio_monitoring.cli_parser.database import DatabaseIdParser
from temelio_monitoring.cli_parser.generic_thresholds import \
    GenericThresholdsParser
from temelio_monitoring.cli_parser.location import HostParser, PortParser
from temelio_monitoring.cli_parser.metric import MetricNameParser


def parse_args():
    """
    Manage plugin arguments
    """

    parser = argparse.ArgumentParser(
        description=('Check output of Nginx stub status page.'),
        parents=[
            CommonParser(),
            DatabaseIdParser(default=0),
            GenericThresholdsParser(),
            HostParser(),
            MetricNameParser(required=True),
            PasswordParser(),
            PortParser(default=6379),
        ]
    )

    return parser.parse_args()


@nagiosplugin.guarded
def main():
    """
    Entry point of monitoring plugin
    """

    # Parse plugin arguments
    args = parse_args()

    # Manage check components
    check = nagiosplugin.Check(
        ScalarInfoValue(
            database_id=args.database_id,
            host=args.host,
            metric_name=args.metric_name,
            password=args.password,
            port=args.port),
        nagiosplugin.ScalarContext(
            'db{}_{}'.format(args.database_id, args.metric_name),
            args.warning,
            args.critical),
    )

    # Execute check
    check.main(args.verbose, args.timeout)


if __name__ == '__main__':
    main()
