"""Extract a fresh copy of the supplied research handoff without overwriting.

This helper validates paths and copies files; it does not execute their contents.
"""
from pathlib import Path
import stat
import zipfile

base = Path(__file__).resolve().parent
archive = base / 'originals/erdos1060_complete_handoff.zip'
destination = (base / 'inputs').resolve()
with zipfile.ZipFile(archive) as z:
    for item in z.infolist():
        target = (destination / item.filename).resolve()
        if not target.is_relative_to(destination):
            raise ValueError('Unsafe archive path')
        if stat.S_ISLNK(item.external_attr >> 16):
            raise ValueError('Archive symlink is not supported')
        if target.exists():
            raise FileExistsError(f'Refusing to overwrite {target}')
    z.extractall(destination)
print('Extracted a new copy. No archive content was executed.')
