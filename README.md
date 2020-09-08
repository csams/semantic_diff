# Semantic Diff
This project includes a diff service for simple ini and httpd style
configuration. Instead of generating character or line based diffs, it compares
two configs by parsing them and comparing the trees. This eliminates noise like
whitespace and comments and also provides more meaningful differences. It falls
back to a line based unified diff if parsing fails.

The project is also an example of how grammars can be generically defined and
configured for different use cases.

The grammars in `semdiff.grammars` accept functions that convert recognized
parts into a nest of dictionaries, a queryable object, or a tree that can be
compared with other trees. See `semdiff.models` and `semdiff.differs`.

## Install
Create and activate a python 3 virtual env and then `pip install -r requirements.txt`.

## Run
`python -m wsgi`

## Test
`curl -F "kind=ini" -F 'left_file=@data/left.ini' -F 'right_file=@data/right.ini' http://127.0.0.1:5000/`
