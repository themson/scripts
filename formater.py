#!/usr/bin/env python
from __future__ import print_function, absolute_import, unicode_literals
import sys
import argparse
import re
from time import sleep

__author__ = 'themson mester'

# TODO: Handle Middle Names
# TODO: Handle 'All || All@' Format Arguments
# TODO: Allow Separate First Last Files

PROG = 'formater.py'
USER_FORMATS = {'IL': '<first_initial><last_name>',
                'I.L': '<first_initial>.<last_name>',
                'FL': '<first_name><last_name>',
                'F.L': '<first_initial>.<last_name>'
                }
EMAIL_FORMATS = {'IL@': '<first_initial><last_name>@<domain>',
                 'I.L@': '<first_initial>.<last_name>@<domain>',
                 'FL@': '<first_name><last_name>@<domain>',
                 'F.L@': '<first_initial>.<last_name>@<domain>'
                 }

names_file = ''
output_formats = []
out_file = None
domain = ''


def build_argparser():
    """Create ArgumentParser object

    Add arg options
    Return:: parse_args object."""

    parser = argparse.ArgumentParser(prog=PROG,
                                     description="Tool for generating user names and email addresses.",
                                     epilog="")
    parser.add_argument("-n", "--names", nargs=1,
                        help="Input file format: <first><space><last>",
                        metavar='FILE', dest='name_file')
    parser.add_argument("-f", "--format", nargs='+',
                        help="Output formats: {}, {}".format(' '.join(USER_FORMATS.keys()),
                                                             ' '.join(EMAIL_FORMATS.keys())),
                        metavar='FORMAT', dest='format')
    parser.add_argument("-d", "--domain", nargs=1,
                        help="Email Domain: example.com",
                        metavar='DOMAIN', dest='domain')
    parser.add_argument("-o", "--outfile", nargs=1,
                        help="Output file name",
                        metavar='FILE',  dest='out_file')
    parser.add_argument("-l", "--list-formats", action='store_true', default=False,
                        help="Print available output formats",
                        dest='list_formats')
    return parser


def arg_launcher(parser):
    """Parse command line arguments and check formats validity."""
    global names_file
    global output_formats
    global out_file
    global domain
    args = parser.parse_args()

    if args.list_formats is True:
        list_formats()
        sys.exit()

    if args.name_file:
        names_file = args.name_file[0]
        try:
            with open(names_file, 'r'):
                pass
        except IOError as e:
            print("ERROR: File '{}' Could Not Be Loaded - {}".format(names_file, e.args[1]))
            sys.exit()
    else:
        print("ERROR: Names file required [-n <FILENAME>]")
        parser.print_usage()
        sys.exit()

    if args.format:
        for format_type in args.format:
            format_ = format_type.upper()
            if format_ in USER_FORMATS or format_ in EMAIL_FORMATS:
                output_formats.append(format_)
            else:
                print("ERROR: Invalid output format: '{}' - Formats: {} {}".format(args.format[0],
                      ' '.join(USER_FORMATS.keys()), ' '.join(EMAIL_FORMATS.keys())))
                sys.exit()
    else:
        print("ERROR: Format Required - Formats: {} {}".format(' '.join(USER_FORMATS.keys()),
                                                               ' '.join(EMAIL_FORMATS.keys())))
        parser.print_usage()
        sys.exit()

    for format_ in output_formats:
            if format_ in EMAIL_FORMATS.keys() and not args.domain:
                print("Domain [-d <DOMAIN>] required for format: {}".format(format_))
                parser.print_usage()
                sys.exit()
            elif args.domain:
                domain = args.domain[0]
                print(is_valid_domain(domain))
                if is_valid_domain(domain) is False:
                    print("ERROR: Invalid Domain name: '{}' \n".format(domain))
                    sys.exit()

    if args.out_file:
        out_file = args.out_file[0]


def list_formats():
    """Print current format arguments and their resulting output formats"""
    print("[-f <FORMATS>] - {} {}".format(' '.join(USER_FORMATS.keys()), ' '.join(EMAIL_FORMATS.keys())))
    for format_name in USER_FORMATS.keys():
        print("{}:  {}".format(format_name, USER_FORMATS[format_name]))
    for format_name in EMAIL_FORMATS.keys():
        print("{}: {}".format(format_name, EMAIL_FORMATS[format_name]))


def is_valid_domain(domain_name):
    """Domain name regex on single string, returns bool"""
    return bool(re.search(r'[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63}).', domain_name))


def format_name(name_data, format_):
    """Output Formats"""
    if len(name_data) != 2:
        print("ERROR: [<first> <last>] not found. {} currently handles first and last names only.".format(PROG))
        sys.exit()

    if format_ == 'IL':  # <first_initial><last_name>
        return "{}{}".format(name_data[0][0].lower(), name_data[1].lower())
    elif format_ == 'I.L':  # <first_initial>.<last_name>
        return "{}.{}".format(name_data[0][0].lower(), name_data[1].lower())
    elif format_ == 'FL':  # <first_name><last_name>
        return "{}{}".format(name_data[0].lower(), name_data[1].lower())
    elif format_ == 'F.L':  # <first_name>.<last_name>
        return "{}.{}".format(name_data[0].lower(), name_data[1].lower())

    elif format_ == 'IL@':  # <first_initial><last_name>@<domain>
        return "{}{}@{}".format(name_data[0][0].lower(), name_data[1].lower(), domain)
    elif format_ == 'I.L@':  # <first_initial>.<last_name>@<domain>
        return "{}.{}@{}".format(name_data[0][0].lower(), name_data[1].lower(), domain)
    elif format_ == 'FL@':  # <first_name><last_name>@<domain>
        return "{}{}@{}".format(name_data[0].lower(), name_data[1].lower(), domain)
    elif format_ == 'F.L@':  # <first_name>.<last_name>@<domain>
        return "{}.{}@{}".format(name_data[0].lower(), name_data[1].lower(), domain)


def process_names():
    """Iterate, clean, and format names. Write to file or stdout"""
    names_list = []
    output = []

    with open(names_file, 'r') as names_data:
        for name_data in names_data.readlines():
            name = name_data.split()  # remove multiple spaces & \t
            names_list.append(name)
    for name in names_list:
        if name:
            for format_ in output_formats:
                output.append(format_name(name, format_))

    output = '\n'.join(output)
    if out_file:
        with open(out_file, 'wb') as output_f:
            output_f.write(output)
        print("{} lines written to '{}' . ".format(len(output.splitlines()), out_file))
    else:
        print(output)


def main():
    """Call arg launcher"""
    parser = build_argparser()
    arg_launcher(parser)
    process_names()
    exit()


if __name__ == '__main__':
    main()