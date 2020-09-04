# Semantic Diff
This project includes a "semantic diff" service for simple ini style files. It
ignores whitespace and ordering of key/value pairs, including sections. Comments
and hanging indents are not supported just to keep it simple.

It's also an example of how to define a single parser that can be configured to
make different representations for different use cases.

`iniparser.make_parser` accepts functions that convert recognized parts into a
nest of dictionaries, a queryable object, or a tree that can be compared with
other trees to generate diffs based on structure instead of syntax.

## Install
Create and activate a python 3 virtual env and then `pip install -r requirements.txt`.

## Run
`./service.py`

## Test
`curl -F 'left_file=@data/left.ini' -F 'right_file=@data/right.ini' http://127.0.0.1:5000/`
