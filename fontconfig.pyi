# note:
# types and docstrings are based on testing the FcFont interface
# they are thus not based on inspection of source code

from typing import Final as F, List as L, Tuple as T

class FcFont:
    file : F[str]
    """
    the path given as argument to the constructor
    need not be either of:
    - a valid path
    - a path that exists
    - a path pointing to a font file parseable by fontconfig
    """

    fullname : F[L[None] | L[T[str,str]]]
    """
    a list of pairs (language, name)
    empty if the instance was created with a path not representing a font file
    parseable by fontconfig. currently this is represented by the union type
    # TODO:
    # how to correctly type hint that the empty list may be returned?
    """

    def __init__(self: FcFont, path: str) -> None: ...

    """
    returns the number n of code points covered
    note: n = 0 if the instance was created with a path not representing a font
    file parseable by fontconfig
    """
    def count_chars(self) -> int: ...

    """
    returns True if and only if the char is among the covered code points
    note: returns  if the instance was created with a path not representing a
    font file parseable by fontconfig
    """
    def has_char(self, c: str) -> bool: ...
