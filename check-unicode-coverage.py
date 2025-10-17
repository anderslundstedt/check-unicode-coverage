#! /usr/bin/env python3.12

# IMPORTS

## STD LIB

import argparse as ap
import os
import os.path
import sys

from typing import Dict as D, Final as F, Iterable as I, List as L


## INTERNAL PACKAGES

import font_query as fq



# PARSE AND VALIDATE ARGUMENTS

## CREATE PARSER

parser : F[ap.ArgumentParser]  = ap.ArgumentParser(
    description='check fonts\' Unicode coverage',
    formatter_class=ap.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    '--characters',
    help='path to input text file',
    default=os.path.join(os.path.dirname(__file__), 'characters.txt')
)
parser.add_argument(
    'font',
    nargs='+',
    help='path to font'
)
parser.add_argument(
    '--print-found',
    action='store_true',
    help='print found characters'
)
parser.add_argument(
    '--ignore-missing',
    action='store_true',
    help='do not print missing characters'
)


## PARSE AND STORE ARGS IN THEIR OWN VARIABLES

args                : F[ap.Namespace] = parser.parse_args()
chars_path          : F[str]          = args.characters
font_paths          : F[L[str]]       = args.font
print_found_chars   : F[bool]         = args.print_found
print_missing_chars : F[bool]         = not args.ignore_missing
del args # we have all we need from args now

## VERIFY NO DUPLICATE FONT PATHS

if not len(set(font_paths)) == len(font_paths):
    print('error: duplicate font paths provided', file=sys.stderr)
    sys.exit(2)


## VERIFY THAT CHARS_PATH EXIST AND IS A FILE

if not os.path.exists(chars_path):
    print(f'error: path ‘{chars_path}’ does not exist', file=sys.stderr)
    sys.exit(3)

if not os.path.isfile(chars_path):
    print(f'error: {chars_path} is not a file', file=sys.stderr)
    sys.exit(4)


## VERIFY THAT ALL FONT_PATHS EXIST AND ARE FILES

exit_code : int = 0
for font_path in font_paths:
    if not os.path.exists(font_path):
        print(f'error: path ‘{font_path}’ does not exist', file=sys.stderr)
        exit_code = 5
    elif not os.path.isfile(font_path):
        print(f'error: {font_path} is not a file', file=sys.stderr)
        exit_code = 5
if exit_code != 0:
    sys.exit(5)
del exit_code


## CREATE FONT OBJECTS FROM THE FONT PATHS

exit_code : int = 0
fonts : F[L[fq.t_font]] = []
for p in font_paths:
    f = fq.get_font(p)
    if f is None:
        print(f'error: {p} is not a file supported by fontconfig')
        exit_code = 6
    else:
        fonts.append(f)
if exit_code != 0:
    sys.exit(exit_code)
del exit_code



# INSTANCES OF SUITABLE DATA STRUCTURES

## FONT_NAMES

font_names : F[L[str]] = [fq.get_name(f) for f in fonts]


## CHECK NO DUPLICATE FONT NAMES

if not len(set(font_names)) == len(font_names):
    print('error: duplicate font names', file=sys.stderr)
    for f in fonts:
        name : F[str] = fq.get_name(f)
        names : F[I[str]] = list(filter(lambda n: n == name, font_names))
        assert len(names) > 0, names
        if len(names) > 1:
            print(f'name of font {fq.get_path(f)}: ‘{fq.get_name(f)}’', file=sys.stderr)
        del names
    sys.exit(2)


## CHARACTER LIST WITH DUPLICATES REMOVED

with open(chars_path) as tmp_f:
    tmp_chars : F[str] = ''.join(tmp_f.read().split())
del tmp_f
chars : F[list[str]] = [
    char
    for
    i,char in enumerate(tmp_chars)
    if
    char not in tmp_chars[:i]
]
del tmp_chars


## PRESENT CHARACTERS BY FONT

present_chars_by_font : D[fq.t_font,L[str]] = {
    f: [
        c for c in chars if fq.has_char(f, c)
    ]
    for f in fonts
}

## MISSING CHARS BY FONT

missing_chars_by_font : F[D[fq.t_font,L[str]]] = {
    font: [c for c in chars if c not in found_chars]
    for
    font,found_chars in present_chars_by_font.items()
}


## NO OF PRESENT CHARS BY FONT

no_of_present_chars_by_font : F[D[fq.t_font,int]] = {
    font: len(found_chars)
    for
    font,found_chars in present_chars_by_font.items()
}


## NO OF MISSING CHARS BY FONT

no_of_missing_chars_by_font : F[D[fq.t_font,int]] = {
    font: len(missing_chars)
    for
    font,missing_chars in missing_chars_by_font.items()
}



# OUTPUT

for font in fonts:
    print(
        f'{fq.get_name(font)}:'
        f'{no_of_present_chars_by_font[font]} characters found,',
        f'{no_of_missing_chars_by_font[font]} characters missing'
    )
    if print_found_chars and len(present_chars_by_font[font]) > 0:
        print('found:')
        print(' '.join(present_chars_by_font[font]))
    if print_missing_chars and len(missing_chars_by_font[font]) > 0:
        print('missing:')
        print(' '.join(missing_chars_by_font[font]))
    print(40*'=')
