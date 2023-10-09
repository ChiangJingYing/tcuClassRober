import sys

from pathlib import Path


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent.as_posix())
    return f'{base_path}/{relative_path}'