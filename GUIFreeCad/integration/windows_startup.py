"""Registro en la carpeta Inicio de Windows para ATRIA + FreeCAD + voz."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SHORTCUT_NAME = "ATRIA-FreeCAD.lnk"
_STARTUP_ARGS = "-StartVoice -SkipModels"


def _startup_dir() -> Path:
    if sys.platform != "win32":
        raise OSError("El arranque con Windows solo esta disponible en Windows.")
    appdata = os.environ.get("APPDATA", "").strip()
    if not appdata:
        raise OSError("Variable APPDATA no definida.")
    return (
        Path(appdata)
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs"
        / "Startup"
    )


def resolve_iniciar_atria_bat() -> Path | None:
    """Ruta a iniciar_atria.bat (raiz del repo ATRIA)."""
    try:
        from integration.atria_paths import atria_repo_root

        repo = atria_repo_root()
    except FileNotFoundError:
        return None

    for candidate in (
        repo / "iniciar_atria.bat",
        repo / "luigiIntegracionV1" / "iniciar_atria.bat",
    ):
        if candidate.is_file():
            return candidate.resolve()
    return None


def is_windows_startup_registered() -> bool:
    if sys.platform != "win32":
        return False
    try:
        return (_startup_dir() / SHORTCUT_NAME).is_file()
    except OSError:
        return False


def sync_windows_startup(enabled: bool) -> tuple[bool, str]:
    """
    Crea o quita el acceso directo en Inicio de Windows.

    Returns:
        (ok, mensaje para el usuario; vacio si no hubo cambios)
    """
    if sys.platform != "win32":
        return False, "Solo disponible en Windows."

    registered = is_windows_startup_registered()
    if enabled and registered:
        return True, ""
    if not enabled and not registered:
        return True, ""

    shortcut = _startup_dir() / SHORTCUT_NAME

    if not enabled:
        try:
            if shortcut.is_file():
                shortcut.unlink()
            return True, "Se quito ATRIA del inicio de Windows."
        except OSError as exc:
            return False, f"No se pudo quitar el acceso directo: {exc}"

    bat = resolve_iniciar_atria_bat()
    if bat is None:
        return False, "No se encontro iniciar_atria.bat en el repo ATRIA."

    bat_s = str(bat).replace("'", "''")
    shortcut_s = str(shortcut).replace("'", "''")
    workdir_s = str(bat.parent).replace("'", "''")
    args_s = _STARTUP_ARGS.replace("'", "''")

    ps = f"""
$ErrorActionPreference = 'Stop'
$ws = New-Object -ComObject WScript.Shell
$s = $ws.CreateShortcut('{shortcut_s}')
$s.TargetPath = '{bat_s}'
$s.Arguments = '{args_s}'
$s.WorkingDirectory = '{workdir_s}'
$s.WindowStyle = 7
$s.Description = 'ATRIA + FreeCAD con voz al iniciar Windows'
$s.Save()
"""
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        return True, "ATRIA se abrira con FreeCAD y voz al encender la PC."
    except (subprocess.CalledProcessError, OSError, subprocess.TimeoutExpired) as exc:
        detail = str(exc)
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            detail = exc.stderr.strip() or detail
        return False, f"No se pudo crear el acceso directo: {detail}"
