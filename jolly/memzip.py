import os
import types
import zipfile
import sys
import tarfile


class MemFinder:
    """Class to find a module in a memory zip file"""
    def __init__(self, file):
        self.z = file
        if zipfile.is_zipfile(self.z):
            self.file = zipfile.ZipFile(self.z)
            self._paths = [x.filename for x in self.file.infolist()]
            self._reader = self.file.open
        elif tarfile.is_tarfile(self.z):
            self.file = tarfile.open(fileobj=self.z, mode="r")
            self._paths = self.file.getnames()
            self._reader = self.file.extractfile
        else:
            raise ValueError("Not a valid zip or tar file")

        self.loader = self
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

    def find_spec(self, fullname, path, *args) -> "MemFinder" | None:
        """Called when an import is attempted"""
        if self._mod_to_paths(fullname) is not None:
            self.name = fullname
            return self
        return None


class MemLoader(MemFinder):
    """Class to load a module from a memory zip file"""
    def load_module(self, fullname) -> None:
        """Load a module from a memory zip file"""
        current = ""
        for pkgname in fullname.split("."):
            current += ("." if current else "") + pkgname
            name = current
            if name not in sys.modules:
                sys.modules[name] = self.construct_module(name)

    def construct_module(self, fullname) -> types.ModuleType:
        """Constructs modules and submodules"""
        filename = self._mod_to_paths(fullname)
        if filename not in self._paths:
            raise ImportError(fullname)

        new_module = types.ModuleType(fullname)

        new_module.__file__ = filename
        new_module.__loader__ = self
        new_module.__name__ = fullname
        new_module.__path__ = [
            i for i in self._paths if i.startswith(
                fullname.replace(".py", "").rsplit(".", 1)[0].replace(".", os.sep).strip(".")
            )
        ]
        if filename.endswith("__init__.py"):
            new_module.__package__ = fullname
        else:
            new_module.__package__ = fullname.rpartition('.')[0]

        sys.modules[new_module.__name__] = new_module
        exec(self._reader(filename).read(), new_module.__dict__)

        return new_module
