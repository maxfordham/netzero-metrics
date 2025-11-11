import pathlib

fdir_pkg = pathlib.Path(__file__).parent  # HACK: to get pkg dir for docs... think of better way

__all__ = ["fdir_pkg"]