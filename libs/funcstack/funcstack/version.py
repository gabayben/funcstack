from importlib import metadata

try:
    __version__ = str(metadata.version('funcstack'))
except metadata.PackageNotFoundError:
    __version__ = 'main'