# Jolly

Import Python code from modules straight from the internet.

```py

# Single-Import Example

~flask @ "git://github.com/pallets/flask"

app = flask.Flask(__name__)


# Multi-Import Example
url = "https://somewhere.com/path/to/zip/mymodule.zip"

~ (a, b, c, foo) @ url


```