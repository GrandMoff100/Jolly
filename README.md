# Jolly

Import Python code from modules straight from the internet.

```py
from jolly import register_url

# Register a URL of a directory of Python modules, or from single files.
register_url("https://raw.githubusercontent.com/grandmoff100/jolly/master/examples/zipped")

# Import from that URL
import hello

# -> Inside zipped/hello/__init__.py, importing .hello
# -> Inside zipped/hello/hello.py
# -> Hello, world!
# -> Inside zipped/hello/__init__.py (after importing .hello)

# You can also import from zip files!
register_url("https://raw.githubusercontent.com/grandmoff/jolly/master/examples/out.zip")

import zipped.hello

# -> Inside zipped/__init__.py
# -> Inside zipped/hello/__init__.py, importing .hello
# -> Inside zipped/hello/hello.py
# -> Inside zipped/hello/__init__.py (after importing .hello)

```