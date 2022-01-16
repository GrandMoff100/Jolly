# Jolly

Import Python code from modules straight from the internet.

```py
from jolly import init
init()  # Initialize the Jolly environment

mymodule = import_url('https://raw.githubusercontent.com/grandmoff/jolly/master/examples/helloworld.py')

# -> Hello, World!
# -> I am in helloworld.py!

# Or you can use @= to import a module from a file
# You can also import from zip files!

zipped.hello @= "https://raw.githubusercontent.com/grandmoff/jolly/master/examples/out.zip"

# Imports zipped.hello

# -> Inside zipped/__init__.py
# -> Inside zipped/hello/__init__.py, importing .hello
# -> Inside zipped/hello/hello.py
# -> Inside zipped/hello/__init__.py (after importing .hello)

```