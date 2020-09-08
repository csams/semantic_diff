"""
Make interpreters of ini style files. Doesn't support hanging indent
continuations or comments.
"""
from parsr import EOF, EOL, WS, Char, Many, Number, PosMarker, StringUntil, Wrapper


def make_parser(doc_meaning, section_meaning):
    line_end = Wrapper(EOL | EOF)
    sep = WS >> Char("=") << WS
    key = WS >> PosMarker(StringUntil(sep | line_end)) << sep
    value = PosMarker(Number | StringUntil(line_end).map(str.strip))
    body = PosMarker(Many(key + value).map(section_meaning))
    header_value = StringUntil(Char("]") | line_end).map(str.strip)
    header = WS >> PosMarker(Char("[") >> header_value << Char("]")) << WS
    parser = Many(PosMarker(header + body)).map(doc_meaning) << WS << EOF

    return parser
