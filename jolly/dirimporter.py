from .baseimporter import BaseImporter


class DirImporter(BaseImporter):
    """Class to import a module from a URL directory."""
    def __init__(self, url, requester):
        super().__init__()
        self.r = requester
        self.url = url
        self.files = {}
        self.name = url.split("/")[-1]

    def _mod_to_path(self, fullname) -> str | None:
        """Converts a module name to path"""
        py_filename = fullname.replace(".", "/") + ".py"
        py_package = fullname.replace(".", "/") + "/__init__.py"
        if py_filename in self.files:
            file = self.files[py_filename]
            f_code = 200
        else:
            file, f_code = self.r.request(self.url + py_filename)
        if py_package in self.files:
            package = self.files[py_package]
            p_code = 200
        else:
            package, p_code = self.r.request(self.url + py_package)
        if f_code == 200:
            self.files[py_filename] = file
            return py_filename
        elif p_code == 200:
            self.files[py_package] = package
            return py_package
        else:
            return None

    def run_module(self, module, filename):
        print(f"Running {module} from {filename}")
        exec(self.files[filename], module.__dict__)

    def get_file_list(self):
        return [self.name, *self.files.keys()]
