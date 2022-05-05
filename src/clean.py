import json
import shutil
from operator import imod
from pathlib import Path

from loguru import logger

from src.data import DATA_DIR


class CleanDirectory:
    """This class is used to organize files in a directory,
    by moving files into directories based on extensions
    """
    def __init__(self, directory) -> None:
        self.directory = Path(directory)
        if not self.directory.exists():
            raise FileNotFoundError(f"{self.directory} does not exist")


        with open(DATA_DIR / 'ext.json') as f:
            ext_dir = json.load(f)

        self.extensions_destination = {}
        for key, values in ext_dir.items():
            for value in values:
                self.extensions_destination[value] = key

    def __call__(self,):
        """Organizing files in a directory by moving them based on extensions.
        """
        logger.info(f'Organizing files in {self.directory}...')
        extensions = []
        for file_path in self.directory.iterdir():
            if file_path.is_dir():
                continue

            # get all files
            extensions.append(file_path.suffix)

            if file_path.suffix in self.extensions_destination:
                DEST_DIR = self.directory / self.extensions_destination[file_path.suffix]
            else:
                DEST_DIR = self.directory / 'other'

            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f'Moving {file_path} to {DEST_DIR}...')
            shutil.move(str(file_path), str(DEST_DIR))


if __name__ == '__main__':
    org_files = CleanDirectory(directory='/Users/amir/Downloads')
    org_files()
    logger.info('Done')
