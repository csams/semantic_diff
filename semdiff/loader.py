"""
Module loader that recursively imports a package and all of its subpackages
and modules.
"""
import importlib
import pkgutil


def load(path):
    mod = importlib.import_module(path)
    if not hasattr(mod, "__path__"):
        return

    path = mod.__path__
    prefix = mod.__name__ + "."
    for loader, name, ispkg in pkgutil.iter_modules(path=path, prefix=prefix):
        if not name.startswith(prefix):
            name = prefix + name
        load(name)
