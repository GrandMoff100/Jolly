import requests as r
from .baseimporter import BaseImporter


class DirImporter(BaseImporter):
    """Class to import a module from a URL directory."""
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.files = {}
        self.name = url.split("/")[-1]

    def _mod_to_paths(self, fullname) -> str | None:
        """Converts a module name to path"""
        py_filename = fullname.replace(".", "/") + ".py"
        py_package = fullname.replace(".", "/") + "/__init__.py"
        if py_filename in self.files:
            file = self.files[py_filename]
        else:
            file = r.get(self.url + py_filename)  # TODO: Add RustPython support
        if py_package in self.files:
            package = self.files[py_package]
        else:
            package = r.get(self.url + py_package)
        if file.status_code == 200:
            self.files[py_filename] = file
            return py_filename
        elif package.status_code == 200:
            self.files[py_package] = package
            return py_package
        else:
            return None

    def run_module(self, module, filename):
        exec(self.files[filename].content, module.__dict__)

    def get_file_list(self):
        return [self.name, *self.files.keys()]
