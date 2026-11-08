# pathlib imports
from pathlib import Path

# shutil imports
import shutil

# pathspec imports
from pathspec import PathSpec, Pattern

# sys imports
import sys

def clean(save_env: bool) -> None:
    project_root: Path = Path('.')
    gitignore_path = project_root / '.gitignore'

    if not gitignore_path.exists():
        print('.gitignore not found !')
        return

    spec: PathSpec[Pattern]
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        spec = PathSpec.from_lines('gitwildmatch', f)

    for path in project_root.rglob('*'):
        relative_path: Path = path.relative_to(project_root)

        if (
            path.name == '.gitignore' or 
            '/.git/' in path.resolve().as_posix() or 
            (
                (
                    '/env/' in path.resolve().as_posix() or 
                    '/venv/' in path.resolve().as_posix() or 
                    '/.env/' in path.resolve().as_posix() or 
                    '/.venv/' in path.resolve().as_posix()
                ) 
                and save_env
            )
        ):
            continue

        if spec.match_file(relative_path.as_posix()):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path.resolve())
                if path.exists():
                    path.rmdir()

if __name__ == '__main__':
    clean('--save-env=false' not in sys.argv) 