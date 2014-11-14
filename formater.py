#!/usr/bin/env python
from __future__ import print_function, absolute_import, unicode_literals
import sys
import argparse
import re
from time import sleep
from collections import OrderedDict
__author__ = 'themson mester'


PROG = 'formater.py'
FORMAT_RULES = OrderedDict([('F', '<fist_name>'),
                            ('f', '<last_initial>'),
                            ('L', '<last_name>'),
                            ('l', '<last_initial>'),
                            ('.', 'delimiter <.>'),
                            ('-', 'delimiter <->'),
                            ('_', 'delimiter <_>'),
                            ('d', '<domain_name>'),
                            ('"', 'wrapper "[username||email]"'),
                            ('\'', 'wrapper \'[username||email]\''),
                            ('<', 'wrapper <[username||email]>')
                            ])
names_file = ''
format_rules = []
secondary_rule = ''
out_file = None
domain = ''


def build_argparser():
    """Create ArgumentParser object

    Add arg options
    Return:: parse_args object."""

    parser = argparse.ArgumentParser(prog=PROG,
                                     description="Tool for rule-based user name and email address generation.",
                                     epilog="")
    parser.add_argument("-n", "--names", nargs=1,
                        help="Input file format: <first><space><last>",
                        metavar='FILE', dest='name_file')
    parser.add_argument("-f", "--primary-format", nargs='+',
                        help="Primary Formats: [<{}>]".format('>, <'.join(FORMAT_RULES.keys())),
                        metavar='RULESETS', dest='formats')
    parser.add_argument("-s", "--secondary-format", nargs=1,
                        help="Secondary Format: <primary format data> [<{}>]".format('>, <'.join(FORMAT_RULES.keys())),
                        metavar='RULESET', dest='secondary_format')
    parser.add_argument("-d", "--domain", nargs=1,
                        help="Email Domain: example.com",
                        metavar='DOMAIN', dest='domain')
    parser.add_argument("-o", "--outfile", nargs=1,
                        help="Output file name",
                        metavar='FILE',  dest='out_file')
    parser.add_argument("-l", "--list-rules", action='store_true', default=False,
                        help="Print formatting rules table",
                        dest='list_formats')
    return parser


def arg_launcher(parser):
    """Parse command line arguments and check formats validity."""
    global names_file
    global format_rules
    global secondary_rule
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

    if args.formats:
        for format_rule in args.formats:
            for rule_char in format_rule:
                if rule_char in FORMAT_RULES:
                    pass
                else:
                    print("ERROR: Invalid Formatting Rule - '{}'".format(rule_char))
                    sys.exit()
        format_rules = args.formats
    else:
        print("ERROR: Format rule required - <{}>".format('>, <'.join(FORMAT_RULES.keys())))
        parser.print_usage()
        sys.exit()

    if args.secondary_format:
        for format_rule in args.secondary_format:
            for rule_char in format_rule:
                if rule_char in FORMAT_RULES:
                    pass
                else:
                    print("ERROR: Invalid Secondary Formatting Rule - '{}'".format(rule_char))
                sys.exit()
        secondary_rule = args.secondary_format

    if 'd' in ''.join(format_rules):
        if not args.domain:
            print("Domain [-d <DOMAIN>] required for format rule 'd'")
            parser.print_usage()
            sys.exit()
        elif is_valid_domain(args.domain[0]) is False:
            print("ERROR: Invalid Domain name: '{}' \n".format(args.domain[0]))
            sys.exit()
        else:
            domain = args.domain[0]

    if args.out_file:
        out_file = args.out_file[0]


def list_formats():
    """Print formatting rules and rule set example"""

    print("\n------ Rules ------")
    for rule_name in FORMAT_RULES.keys():
        print("'{}':  {}".format(rule_name, FORMAT_RULES[rule_name]))
    print("------------------")
    print("\nExample: {} -n filename -f f.Ld -d example.com \nOutput: f.last@example.com\n".format(PROG))


def is_valid_domain(domain_name):
    """Domain name regex on single string, returns bool"""
    return bool(re.search(r'[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63}).', domain_name))


def format_name(name_data, rule_set):
    """Generate Formatted name"""
    username = ''
    first, last = name_data[0].lower(), name_data[1].lower()
    first_initial, last_initial = first[0], last[0]
    rule_data = {'F': first,
                 'f': first_initial,
                 'L': last,
                 'l': last_initial,
                 '.': '.',
                 '-': '-',
                 '_': '_',
                 'd': '@{}'.format(domain)
                 }
    for rule in rule_set:
        username += rule_data[rule]
    return username


def process_names():
    """Iterate, clean, and format names. Write to file or stdout"""
    names_list = []
    output = []
    double_quotes = False
    single_quotes = False
    angle_brackets = False
    with open(names_file, 'r') as names_data:
        for name_data in names_data.readlines():
            name = name_data.split()  # remove multiple spaces & \t
            names_list.append(name)
    for name in names_list:
        if name:
            if len(name) != 2:
                print("ERROR: [<first> <last>] not found. {} currently handles first and last names only.".format(PROG))
                sys.exit()
            for rule_set in format_rules:
                output.append(format_name(name, rule_set))
    output = '\n'.join(output)
    if out_file:
        with open(out_file, 'wb') as output_f:
            output_f.write(output)
        print("{} name formats written to '{}' ".format(len(output.splitlines()), out_file))
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

# TODO: Handle Middle Names
# TODO: Handle 'All' Format Arguments
# TODO: Allow Separate First Last Files
# TODO: add second format for wrapping names and emails