import os
import types
import zipfile
import io


class ZipImporter(object):
    def __init__(self, zip_file):
        self.z = io.BytesIO(zip_file)
        self.zfile = zipfile.ZipFile(self.z)
        self._paths = [x.filename for x in self.zfile.filelist]

    def _mod_to_paths(self, fullname):
        # get the python module name
        py_filename = fullname.replace(".", os.sep) + ".py"
        # get the filename if it is a package/subpackage
        py_package = fullname.replace(".", os.sep, fullname.count(".") - 1) + "/__init__.py"
        if py_filename in self._paths:
            return py_filename
        elif py_package in self._paths:
            return py_package
        else:
            return None

    def find_module(self, fullname, path):
        if self._mod_to_paths(fullname) is not None:
            return self
        return None

    def load_module(self, fullname):
        filename = self._mod_to_paths(fullname)
        if filename not in self._paths:
            raise ImportError(fullname)
        new_module = types.ModuleType(fullname)
        exec(self.zfile.open(filename, 'r').read(), new_module.__dict__)
        new_module.__file__ = filename
        new_module.__loader__ = self
        if filename.endswith("__init__.py"):
            new_module.__path__ = []
            new_module.__package__ = fullname
        else:
            new_module.__package__ = fullname.rpartition('.')[0]
        return new_module
