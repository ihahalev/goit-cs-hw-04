from collections import defaultdict
from threading import Lock as Thread_Lock
from multiprocessing.queues import Queue
from multiprocessing.synchronize import Lock as Process_Lock
import re
from print_results import logging

def find_keywords(
    files:list[str],
    keywords:list[str],
    result_dict:defaultdict|None = None,
    thread_lock:Thread_Lock = None,
    queue:Queue|None = None,
    proc_lock:Process_Lock|None=None
):
    """_summary_

    Args:
        files list[str): list of pathes to files
        keywords (list[str): list of keyword to be searched
        result_dict (defaultdict | None, optional): dictionary that will contain results. Defaults to None.
        thread_lock (Thread_Lock, optional): thread lock. Defaults to None.
        queue (Queue | None, optional): queue that will contain results. Defaults to None.
        proc_lock (Process_Lock | None, optional): process lock. Defaults to None.
    """

    for file_path in files:
        try:
            with open(file_path, "r") as fh:
                text = fh.read()
            logging.info(f"Processing file: {file_path}")
            if (thread_lock):
                with thread_lock:  # Providing safe work with dictionary
                    for keyword in keywords:
                        result = re.search(keyword, text, re.IGNORECASE)
                        if result:
                            result_dict[keyword].append(file_path)
            if (proc_lock):
                results = defaultdict(list)
                for keyword in keywords:
                    result = re.search(keyword, text, re.IGNORECASE)
                    if result:
                        results[keyword].append(file_path)
                        with proc_lock:
                            queue.put(results)
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {str(e)}")
