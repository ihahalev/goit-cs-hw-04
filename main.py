from pathlib import Path
import logging
from find_keywords import find_keywords
from multithreading_search import start_threds
from multiprocessing_search import start_processes

def get_files_list(dir: Path) -> list[str]:
    """Getting list of pathes to files from directory that will be read and searched

    Args:
        dir (Path): directory from where to get files

    Returns:
        list[str]: list of pathes to files
    """
    try:
        files = [f for f in dir.iterdir() if f.is_file]
        logging.info(f"Found {len(files)} files in directory {dir}")
        return [str(f) for f in files]
    except FileNotFoundError:
        logging.error(f"Directory not found: {str(dir)}")
        return []
    except Exception as e:
        logging.error(f"Error reading directory {dir}: {str(e)}")
        return []

def main():
    try:
        dir = Path.cwd()/'texts'

        # get the list of all files inside root folder and all it's child folders
        file_list = get_files_list(dir)

        # the list of key words for search in files
        keywords = ["somebody", "court", "economy", "dog", "owner"]

        # multithreading search
        start_threds(file_list, keywords, 4)

        # multiprocessing search with all processes
        start_processes(file_list, keywords)

        # multiprocessing search with same as threads
        start_processes(file_list, keywords, 4)
    except Exception as e:
        print(f"Oops. Error happend! {e}")

if __name__ == "__main__":
    main()
