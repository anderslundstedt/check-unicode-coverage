#! /usr/bin/env python3

# IMPORTS

## STD LIB

import argparse as ap
import os
import os.path
import sys

from typing import Dict as D, Final as F, List as L


## EXTERNAL PACKAGES

import fontconfig as fc



# PARSE ARGUMENTS

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



# INSTANCES OF SUITABLE DATA STRUCTURES FOR THE FONTS

## CHECK NO DUPLICATE FONT PATHS
if not len(set(font_paths)) == len(font_paths):
    print('error: duplicate font paths provided', file=sys.stderr)
    sys.exit(1)


## FONT_BY_FONT_PATH, FONT_NAME_BY_FONT_PATH, FONT_BY_FONT_NAME, FONT_NAMES

font_by_font_path : F[D[str,fc.FcFont]] = {
    font_path: fc.FcFont(font_path)
    for
    font_path in font_paths
}

font_name_by_font_path : F[D[str,str]] = {
    font_path: font_by_font_path[font_path].fullname[0][1] # pyright: ignore[reportOptionalSubscript]
    for
    font_path in font_paths
}

font_by_font_name : F[D[str,fc.FcFont]] = {
    font_name: font_by_font_path[font_path]
    for
    font_path,font_name in font_name_by_font_path.items()
}

font_names : F[L[str]] = list(font_name_by_font_path.values())


## CHECK NO DUPLICATE FONT NAMES

if not len(set(font_names)) == len(font_names):
    print('error: duplicate font names', file=sys.stderr)
    for font_path,font_name in font_name_by_font_path.items():
        names : F[L[str]] = [name for name in font_names if name == font_name]
        assert len(names) > 0, names
        if len(names) > 1:
            print(f'name of font {font_path}: ‘{font_name}’', file=sys.stderr)
        del names
    sys.exit(2)



# INSTANCES OF SUITABLE DATA STRUCTURES FOR THE CHARACTER FILE

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


## FIND OUT PRESENT AND MISSING CHARACTERS

found_chars_by_font_name : D[str,L[str]] = {
    font_name: [
        c for c in chars if font.has_char(c)
    ]
    for font_name,font in font_by_font_name.items()
}

missing_chars_by_font_name : F[D[str,L[str]]] = {
    font_name: [
        c
        for
        c in chars
        if
        c not in found_chars
    ]
    for
    font_name,found_chars in found_chars_by_font_name.items()
}

no_of_found_chars_by_font_name : F[D[str,int]] = {
    font_name: len(found_chars)
    for
    font_name,found_chars in found_chars_by_font_name.items()
}

no_of_missing_chars_by_font_name : F[D[str,int]] = {
    font_name: len(missing_chars)
    for
    font_name,missing_chars in missing_chars_by_font_name.items()
}



# OUTPUT

for font_name in font_names:
    print(
        f'{font_name}:',
        f'{no_of_found_chars_by_font_name[font_name]} characters found,',
        f'{no_of_missing_chars_by_font_name[font_name]} characters missing'
    )
    if print_found_chars and len(found_chars_by_font_name[font_name]) > 0:
        print('found:')
        print(' '.join(found_chars_by_font_name[font_name]))
    if print_missing_chars and len(missing_chars_by_font_name[font_name]) > 0:
        print('missing:')
        print(' '.join(missing_chars_by_font_name[font_name]))
    print(40*'=')
