import os
import zipfile
import tarfile
import io
from .baseimporter import BaseImporter


class MemImporter(BaseImporter):
    """Class to find a module in a memory zip file"""
    def __init__(self, file: bytes, subdir: str = None):
        super().__init__()
        self._subdir = subdir
        file = io.BytesIO(file)

        # ZipFiles
        if zipfile.is_zipfile(file):
            file = zipfile.ZipFile(file)
            self._paths = [self.subdir + x.filename for x in file.infolist()]
            self._reader = file.open

        # TarFiles
        elif tarfile.is_tarfile(file):
            file.seek(0)
            tar = tarfile.open(fileobj=file)
            self._paths = [i for i in tar.getnames() if not self._subdir or i.startswith(self._subdir)]
            self._reader = tar.extractfile

        # Other (presumably standalone python files)
        else:
            self._paths = [file]
            self._reader = file.read

        self.name = self._paths[0].split(os.sep)[0]

    def _mod_to_path(self, fullname) -> str | None:
        """Converts a module name to path"""
        py_filename = self.subdir + fullname.replace(".", os.sep) + ".py"
        py_package = self.subdir + fullname.replace(".", os.sep) + "/__init__.py"
        if py_filename in self._paths:
            return py_filename
        elif py_package in self._paths:
            return py_package
        else:
            return None

    def run_module(self, module, filename):
        """Runs a module in the archive/file"""
        exec(self._reader(filename).read(), module.__dict__)

    def get_file_list(self):
        """Returns a list of all files in the archive/file"""
        return self._paths

    @property
    def subdir(self):
        """Returns the prefix for the subdirectory"""
        return self._subdir + os.sep if self._subdir else ""
