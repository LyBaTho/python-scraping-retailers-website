import os
from datetime import datetime
from pathlib import Path

def get_data_folder():
    try:
        code_dir = Path(__file__).parent
    except NameError:
        code_dir = Path.cwd()

    # 'sources' directory is one level up from code_dir
    sources_dir = code_dir.parent
    # 'data' root under sources
    data_root = sources_dir / 'data'

    # New folder naming with YYYY-MM for proper sorting
    month_folder = datetime.now().strftime("%Y-%m %B").lower()
    
    # Full path to the monthly folder
    month_dir = data_root / month_folder
    month_dir.mkdir(parents=True, exist_ok=True)
    return month_dir

if __name__ == "__main__":
    folder = get_data_folder()
    print(f"Data will be stored in: {folder}")