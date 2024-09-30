from collections import defaultdict
from threading import Lock as Thread_Lock
from multiprocessing.managers import DictProxy
from multiprocessing.synchronize import Lock as Process_Lock
import re
from print_results import logging

def find_keywords(
    files:list[str],
    keywords:list[str],
    result_dict:defaultdict|DictProxy,
    thread_lock:Thread_Lock = None,
    proc_lock:Process_Lock|None=None
):
    """_summary_

    Args:
        files list[str): list of pathes to files
        keywords (list[str): list of keyword to be searched
        result_dict (defaultdict | DictProxy): dictionary that will contain results.
        thread_lock (Thread_Lock, optional): thread lock. Defaults to None.
        proc_lock (Process_Lock | None, optional): process lock. Defaults to None.
    """

    for file_path in files:
        try:
            with open(file_path, "r") as fh:
                text = fh.read()
            logging.info(f"Processing file: {file_path}")
            if (thread_lock):
                with thread_lock:  # Providing safe work with dictionary
                    run_search(keywords, text, file_path, result_dict)
            if (proc_lock):
                with proc_lock:
                    run_search(keywords, text, file_path, result_dict)
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {str(e)}")

def run_search(keywords:list[str], text:str, path:str, result_dict:defaultdict|DictProxy):
    for keyword in keywords:
        result = re.search(keyword, text, re.IGNORECASE)
        if result:
            result_dict[keyword].append(path)