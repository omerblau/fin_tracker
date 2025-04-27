# utils_file.py
from pathlib import Path
import shutil

def move_file(src: str | Path, dst_dir: str | Path, *, overwrite: bool = False) -> Path:
    """Move *src* into *dst_dir* (mkdir -p) and return the new Path."""
    src_path = Path(src).expanduser().resolve(strict=True)
    if not src_path.is_file():
        raise FileNotFoundError(f"{src_path} is not a regular file")

    dst_dir = Path(dst_dir).expanduser().resolve()
    dst_dir.mkdir(parents=True, exist_ok=True)

    dst_path = dst_dir / src_path.name
    if dst_path.exists() and not overwrite:
        raise FileExistsError(f"{dst_path} already exists (use overwrite=True)")

    shutil.move(str(src_path), str(dst_path))
    return dst_path
