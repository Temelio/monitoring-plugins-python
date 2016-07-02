"""
Monitoring plugin to check protractor json output

Used to manage results of: https://github.com/cbragard/protractor-html-reporter
"""

import argparse
import nagiosplugin

from temelio_monitoring.cli_parser import CommonParser
from temelio_monitoring.cli_parser.authentication import \
    CertificateFileParser, KeyFileParser, UsernameParser, PasswordParser
from temelio_monitoring.cli_parser.web import UrlParser
from temelio_monitoring.resource.json import GetValueByJsonPath
from temelio_monitoring.context.json import CountValuesFromJSON


def parse_args():
    """
    Manage plugin arguments
    """

    parser = argparse.ArgumentParser(
        description=(
            'Check JSON output of '
            'https://github.com/cbragard/protractor-html-reporter '
            'e2e reporter.'),
        parents=[
            CommonParser(),
            CertificateFileParser(),
            KeyFileParser(),
            UsernameParser(),
            PasswordParser(),
            UrlParser(required=True)
        ]
    )

    return parser.parse_args()


@nagiosplugin.guarded
def main():
    """
    Entry point of monitoring plugin
    """

    requests = [
        'failed_tests;;$[*].id where(`parent`.failedExpectations[*].passed);;',
        'failed_exp;;$[*].failedExpectations[*].passed;;',
        'total_exp;;$[*].[passedExpectations,failedExpectations][*].passed;;',
        'total_tests;;$[*].id;;',
    ]

    # Parse plugin arguments
    args = parse_args()

    # Manage check components
    check = nagiosplugin.Check(
        GetValueByJsonPath(
            src=args.url,
            requests=requests,
            username=args.username,
            password=args.password,
            certificate_file=args.certificate_file,
            key_file=args.key_file),
        CountValuesFromJSON('failed_tests', critical='@1:'),
        CountValuesFromJSON('failed_exp', critical='@1:'),
        CountValuesFromJSON('total_tests'),
        CountValuesFromJSON('total_exp'),
    )

    # Execute check
    check.main(args.verbose, args.timeout)


if __name__ == '__main__':
    main()
