import sys
import io
from .memimporter import MemImporter
import time
from .dirimporter import DirImporter

try:
    import requests
except ImportError:
    import browser as requests


class Files:
    @classmethod
    def request(cls, url: str, *args, **kwargs) -> io.BytesIO:
        requester = cls._requesters.get(
            sys.implementation.name,
            cls.default_requester
        )
        return requester(url, *args, **kwargs)

    @staticmethod
    def rustpython_requester(url: str, *args, **kwargs) -> io.BytesIO:
        result = None

        def finished(res):
            nonlocal result
            result = res

        requests.fetch(
            url,
            *args,
            **kwargs
        ).then(finished)
        while not result:
            time.sleep(0.1)
        return io.BytesIO(result)

    _requesters = {
        "rustpython": rustpython_requester,
    }

    @staticmethod
    def default_requester(url: str, *args, **kwargs) -> io.BytesIO:
        content = requests.get(url, *args, **kwargs).content
        return io.BytesIO(content)


def register_url(
        url: str,
        *args,
        **kwargs
) -> None:
    """Register a URL to be imported from. Zips are supported."""
    if "." not in url.split("/")[-1]:  # Only files should have a suffix, not directories
        importer = DirImporter(url)
    else:
        target_file = Files.request(url, *args, **kwargs)
        importer = MemImporter(target_file)
    sys.meta_path.append(importer)
