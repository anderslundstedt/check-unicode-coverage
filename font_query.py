# IMPORTS

## STD LIB

from dataclasses import dataclass
from typing import Final as F, NewType, Optional as O


## EXTERNAL PACKAGES

import fontconfig as fc



# INTERFACE AND IMPLEMENTATION

@dataclass(frozen=True)
class _c:
    f: F[fc.FcFont]

t_font = NewType('t_font', _c)

def get_font(path: str) -> O[t_font]:
    fc_font = fc.FcFont(path)
    if len(fc_font.fullname) > 0:
        return t_font(_c(fc_font))
    else:
        return None

def get_path(font: t_font) -> str:
    return font.f.file

def get_name(font: t_font) -> str:
    assert len(font.f.fullname) > 0, font.f.file
    assert font.f.fullname[0] is not None, font.f.file
    return font.f.fullname[0][1]

"""
- returns None if len(c) != 1
- returns True if len(c) == 1 and c is covered by font
- returns False if len(c) == 1 and c is not covered by font
"""
def has_char(font: t_font, c: str) -> O[bool]:
    try:
        return font.f.has_char(c)
    except ValueError:
        return False

"""
returns the number n of code points covered
"""
def count_chars(font: t_font) -> int:
    return font.f.count_chars()
