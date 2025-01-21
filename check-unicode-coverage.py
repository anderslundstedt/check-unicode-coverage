#! /usr/bin/env python3

import argparse
import os
import os.path
import sys

import fontconfig

parser = argparse.ArgumentParser(
    description="check fonts' Unicode coverage",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--characters", help="path to input text file",
    default=os.path.join(os.path.dirname(__file__), "characters.txt")
)
parser.add_argument("font", nargs="+", help="path to font")
parser.add_argument(
    "--print-found", action="store_true", help="print found characters"
)
parser.add_argument(
    "--ignore-missing", action="store_true",
    help="do not print missing characters"
)
args = parser.parse_args()
chars_path = args.characters
font_paths = args.font
print_found = args.print_found
print_missing = not args.ignore_missing

with open(chars_path) as f:
    tmp_chars = "".join(f.read().split())
chars = []
for c in tmp_chars:
    if c not in chars:
        chars.append(c)

fonts = [fontconfig.FcFont(font_path) for font_path in font_paths]
chars_by_font = {f: [c for c in chars if f.has_char(c)] for f in fonts}
missing_chars_by_font =\
    {f: [c for c in chars if c not in chars_by_font[f]] for f in fonts}
no_of_chars_by_font = {f: len(chars_by_font[f]) for f in fonts}
no_of_missing_chars_by_font = {f: len(missing_chars_by_font[f]) for f in fonts}
for font in sorted(fonts, key=lambda f: no_of_chars_by_font[f]):
    print(
        font.fullname, no_of_chars_by_font[font], "characters",
        no_of_missing_chars_by_font[font], "missing",
    )
    if print_found:
        print("found:")
        print(" ".join(chars_by_font[font]))
    if print_missing:
        print("missing:")
        print(" ".join(missing_chars_by_font[font]))
    print(40 * "=")
for font in fonts:
    if no_of_missing_chars_by_font[font] > 0:
        sys.exit(1)
