import os
import zipfile
import tarfile
from .baseimporter import BaseImporter


class MemImporter(BaseImporter):
    """Class to find a module in a memory zip file"""
    def __init__(self, file):
        super().__init__()
        if zipfile.is_zipfile(file):
            file = zipfile.ZipFile(file)
            self._paths = [x.filename for x in file.infolist()]
            self._reader = file.open
        elif tarfile.is_tarfile(file):
            file = tarfile.open(fileobj=file, mode="r")
            self._paths = file.getnames()
            self._reader = file.extractfile
        else:
            self._paths = [file]
            self._reader = file.read
        self.name = self._paths[0].split(os.sep)[0]

    def _mod_to_paths(self, fullname) -> str | None:
        """Converts a module name to path"""
        py_filename = fullname.replace(".", os.sep) + ".py"
        py_package = fullname.replace(".", os.sep) + "/__init__.py"
        if py_filename in self._paths:
            return py_filename
        elif py_package in self._paths:
            return py_package
        else:
            return None

    def run_module(self, module, filename):
        exec(self._reader(filename).read(), module.__dict__)

    def get_file_list(self):
        return self._paths
