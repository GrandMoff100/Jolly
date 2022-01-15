import inspect
from .importast import Importer
from .memzip import ZipImporter
import types
import ast
import sys


def init():
    backframe = inspect.currentframe().f_back
    source = inspect.getsource(backframe)
    source = source[source.index("init()") + len("init()"):]

    tree = ast.parse(source)
    Importer().visit(tree)
    ast.fix_missing_locations(tree)
    compiled = compile(tree, backframe.f_globals['__name__'], 'exec')
    exec(compiled, {"__import_from_url": import_from_url} | globals())
    sys.exit(0)


def import_from_url(url: str, name: str):
    import requests as __r
    content = __r.get(url).content
    try:
        if url.endswith(".zip"):
            importer = ZipImporter(content)
            sys.meta_path.append(importer)
            module = importer.load_module(name)
        else:
            module = types.ModuleType(name)
            exec(content.decode("utf-8"), module.__dict__)
    except Exception as e:
        print("***| Failed to load module from url:", url, "\n   |", type(e).__name__, e)
        return None
    return module


