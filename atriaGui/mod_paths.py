"""Resolve ATRIA module directory when FreeCAD runs InitGui without __file__."""

from __future__ import annotations

import inspect
import os
import sys


def get_mod_dir() -> str:
  """Folder that contains InitGui.py (the ATRIA workbench root)."""
  try:
    import FreeCAD as App

    for path in getattr(App, "__ModDirs__", ()) or ():
      norm = os.path.normpath(path)
      if os.path.basename(norm).upper() == "ATRIA":
        return norm
  except Exception:
    pass

  try:
    return os.path.dirname(os.path.abspath(__file__))
  except NameError:
    pass

  try:
    frame = inspect.currentframe()
    if frame and frame.f_back:
      return os.path.dirname(os.path.abspath(inspect.getfile(frame.f_back)))
  except Exception:
    pass

  env_root = os.environ.get("ATRIA_MOD_ROOT", "").strip()
  if env_root and os.path.isdir(env_root):
    return os.path.normpath(env_root)

  try:
    import FreeCAD as App

    user_mod = os.path.join(App.getUserAppDataDir(), "Mod", "ATRIA")
    if os.path.isdir(user_mod):
      return user_mod
  except Exception:
    pass

  return ""


def ensure_mod_on_sys_path() -> str:
  mod_dir = get_mod_dir()
  if mod_dir and mod_dir not in sys.path:
    sys.path.insert(0, mod_dir)
  return mod_dir
