import os
import types
import sys
import typing as t


class BaseImporter:
    """Base finder class."""
    def __init__(self):
        """Initializes the importer. Must be overridden"""
        self.name = ""
        self.loader = self

    def find_spec(self, fullname, path, *args) -> t.Optional[None]:
        """Called when an import is attempted"""
        if self._mod_to_path(fullname) is not None:
            self.name = fullname
            return self
        return None

    def load_module(self, fullname) -> types.ModuleType:
        """Load a module from a directory in the internet"""
        current = ""
        for pkgname in fullname.split("."):
            current += ("." if current else "") + pkgname
            name = current
            if name not in sys.modules:
                sys.modules[name] = self.construct_module(name)
        return sys.modules[fullname]

    def construct_module(self, fullname) -> types.ModuleType:
        """Constructs modules and submodules"""
        filename = self._mod_to_path(fullname)
        if filename is None:
            raise ImportError(fullname)

        new_module = types.ModuleType(fullname)

        new_module.__file__ = filename
        new_module.__loader__ = self
        new_module.__name__ = fullname
        new_module.__path__ = [
            i for i in self.get_file_list() if i.startswith(
                fullname.replace(".py", "").rsplit(".", 1)[0].replace(".", os.sep).strip(".")
            )
        ]
        if filename.endswith("__init__.py"):
            new_module.__package__ = fullname
        else:
            new_module.__package__ = fullname.rpartition('.')[0]

        sys.modules[new_module.__name__] = new_module
        self.run_module(new_module, filename)

        return new_module

    def run_module(self, module, filename):
        """Runs the module. Must be overridden"""
        ...

    def _mod_to_path(self, fullname):
        """Returns the path to the module. Must be overridden"""
        pass

    def get_file_list(self):
        """Returns a list of all files in the directory. Must be overridden"""
        pass
