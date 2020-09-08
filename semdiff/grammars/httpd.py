"""
Make interpreters of httpd style configuration files.
"""
import string

from parsr import (Char, EOF, EOL, EndTagName, Forward, FS, GT, InSet,
     Literal, LT, Letters, Lift, LineEnd, Many, Number, OneLineComment,
     PosMarker, QuotedString, skip_none, StartTagName, String, WS, WSChar)


def make_parser(section_meaning, directive_meaning):
    Section = Forward()
    Comment = (WS >> OneLineComment("#")).map(lambda x: None)

    Name = String(string.ascii_letters + "_/")
    Num = Number & (WSChar | LineEnd)

    StartName = WS >> PosMarker(StartTagName(Letters)) << WS
    EndName = WS >> EndTagName(Letters, ignore_case=True) << WS

    Cont = Char("\\") + EOL
    AttrStart = Many(WSChar)
    AttrEnd = (Many(WSChar) + Cont) | Many(WSChar)

    OpAttr = (Literal("!=") | Literal("<=") | Literal(">=") | InSet("<>")) & WSChar
    BareAttr = String(set(string.printable) - (set(string.whitespace) | set("<>'\"")))
    Attr = AttrStart >> PosMarker(Num | QuotedString | OpAttr | BareAttr) << AttrEnd
    Attrs = Many(Attr)

    StartTag = (WS + LT) >> (StartName + Attrs) << (GT + WS)
    EndTag = (WS + LT + FS) >> EndName << (GT + WS)

    Directive = WS >> (Lift(directive_meaning) * PosMarker(Name) * Attrs) << WS  # <--- interpret the directive
    Stanza = Directive | Section | Comment | Many(WSChar | EOL, lower=1).map(lambda x: None)
    Section <= (Lift(section_meaning) * StartTag * Many(Stanza).map(skip_none)) << EndTag  # <--- interpret the section

    parser = Many(Stanza).map(skip_none) << WS << EOF

    return parser
