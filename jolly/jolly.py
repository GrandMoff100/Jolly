import inspect
from .importast import Importer
from .memzip import MemLoader
import types
import ast
import sys
import zipfile
import tarfile
import io
import typing as t
import functools


def init(requester: t.Callable = None) -> None:
    """
    Initialize the jolly importer.
    Use `import_url` to import modules from URLs, or use `mymodule @= "https://example.com/mymodule.py"`.
    Zips are supported.
    Currently, tarfiles are not supported.
    """
    backframe = inspect.currentframe().f_back
    source = inspect.getsource(backframe)
    source = "\n".join(source.split("\n")[backframe.f_lineno:])

    tree = ast.parse(source)
    Importer().visit(tree)
    ast.fix_missing_locations(tree)
    compiled = compile(tree, backframe.f_globals['__name__'], 'exec')
    exec(
        compiled,
        {"import_url": functools.partial(import_from_url, requester=requester or default_requester)},
    )
    sys.exit(0)


def default_requester(url: str) -> bytes:
    """Default requester for `import_from_url`/`import_url`."""
    import requests as __r
    return __r.get(url).content


def import_from_url(
        url: str,
        name: str,
        requester: t.Callable = default_requester,
        insecure_warn: bool = True
) -> types.ModuleType:
    """Import a module from a URL. Zips are supported."""
    if insecure_warn and url.startswith("http://"):
        print("WARNING: Insecure import from %s" % url)
    content = requester(url)
    try:
        contfile = io.BytesIO(content)
        if zipfile.is_zipfile(contfile) or tarfile.is_tarfile(contfile):
            importer = MemLoader(contfile)
            sys.meta_path.insert(0, importer)
            module = importer.load_module(name)
        else:
            module = types.ModuleType(name)
            exec(content.decode("utf-8"), module.__dict__)
    except Exception as e:
        print("***| Failed to load module from url:", url, "\n   |", type(e).__name__, e)
        sys.exit(1)
    return module


