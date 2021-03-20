import logging
import shutil
from datetime import datetime, timedelta
from itertools import chain
from pathlib import Path
from zipfile import ZipFile


logger = logging.getLogger(__name__)

MAX_STORAGE_DAYS = 90
FREE_SPACE_PERCENT = 10


def get_file_datetime(path):
    year, month, day = path.parent.parts[-3:]
    return datetime(int(year), int(month), int(day))


def free_storage_memory():
    total, used, free = shutil.disk_usage('./storage')
    if free / total * 100 >= FREE_SPACE_PERCENT:
        logger.info("You don't need to archive and move files. Space of storage is more than 10%")
        return

    patterns = ("*.wav", "*.mp3")
    current_date = datetime.now()
    iterable = chain.from_iterable(Path("./storage").rglob(pattern) for pattern in patterns)

    storage_dir = None
    with ZipFile("archive.zip", mode="w") as archive:
        for path in sorted(iterable, key=get_file_datetime):
            file_date = get_file_datetime(path)

            if not storage_dir:
                storage_dir = path.parent
            if storage_dir != path.parent:
                break

            if file_date + timedelta(days=MAX_STORAGE_DAYS) < current_date:
                archive.write(path, path.name)
                logger.info(f"Added {path} file to {archive.filename}")

    if not storage_dir:
        logger.warning("Storage is empty. Exit")
        return

    if archive.namelist():
        year, month, day = storage_dir.parts[-3:]
        archive_path = Path("./archive") / year / month / day
        archive_path.mkdir(parents=True, exist_ok=True)

        shutil.move(archive.filename, archive_path)
        logger.info(f"Moved {archive.filename} to {archive_path}")

        shutil.rmtree(storage_dir)
        logger.info(f"Removed {storage_dir} directory")

        free_storage_memory()


def main():
    # noinspection PyArgumentList
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("all.log", mode="a"),
            logging.StreamHandler()
        ]
    )

    try:
        free_storage_memory()
    except Exception as exc:
        logger.exception(exc)


if __name__ == '__main__':
    main()
