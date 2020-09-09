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
```
└> curl -F "kind=ini" -F 'left_file=@data/left.ini' -F 'right_file=@data/right.ini' http://127.0.0.1:5000/ | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   964  100   386  100   578  22705  34000 --:--:-- --:--:-- --:--:-- 56705
{
  "result": [
    {
      "left": {
        "col": 1,
        "end": 37,
        "lineno": 1,
        "start": 0,
        "value": "heading1"
      },
      "right": null
    },
    {
      "left": null,
      "right": {
        "col": 1,
        "end": 59,
        "lineno": 4,
        "start": 20,
        "value": "heading3"
      }
    }
  ],
  "type": "structural"
}
```
```
└> curl -F "kind=httpd" -F 'left_file=@data/left_httpd.conf' -F 'right_file=@data/right_httpd.conf' http://127.0.0.1:5000/ | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 24676  100   401  100 24275   2155   127k --:--:-- --:--:-- --:--:--  130k
{
  "result": [
    {
      "left": {
        "col": 2,
        "end": 4575,
        "lineno": 127,
        "start": 4470,
        "value": "Directory"
      },
      "right": null
    },
    {
      "left": null,
      "right": {
        "col": 2,
        "end": 4574,
        "lineno": 127,
        "start": 4470,
        "value": "Directory"
      }
    }
  ],
  "type": "structural"
}
```