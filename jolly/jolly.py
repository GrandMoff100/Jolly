import sys
import io
from .memimporter import MemImporter
import time
from .dirimporter import DirImporter
import typing as t

try:
    import urllib.request as requests
    from urllib.error import HTTPError
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
        return result

    _requesters = {
        "rustpython": rustpython_requester,
    }

    @staticmethod
    def default_requester(url: str, *args, **kwargs) -> t.Tuple[io.BytesIO | None, int]:
        try:
            with requests.urlopen(url, *args, **kwargs) as resp:
                return resp.read(), 200
        except HTTPError as e:
            return None, e.code


def register_url(
        url: str,
        subdir: str = None,  # For zips and tars
        *args,
        **kwargs
) -> None:
    """Register a URL to be imported from. Zips and tars are supported."""
    if "." not in url.split("/")[-1]:  # Only files should have a suffix, not directories
        importer = DirImporter(url, Files)
    else:
        target_file, code = Files.request(url, *args, **kwargs)
        if code != 200:
            raise ValueError(f"Could not fetch {url}")
        importer = MemImporter(target_file, subdir=subdir)
    sys.meta_path.append(importer)
