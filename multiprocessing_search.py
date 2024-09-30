from multiprocessing import Process, Lock, cpu_count, Manager
import time
from collections import defaultdict
from typing import Callable
from find_keywords import find_keywords
from print_results import print_results, logging

def worker(callback:Callable, *args):
    """worker that will call provided function

    Args:
        callback (Callable): function to call
    """
    callback(args[0], args[1], args[2], proc_lock=args[3])

def start_processes(files:list[str], keywords:list[str], num_processes:int | None = None):
    """starts processes that will process search function

    Args:
        files list[str): list of pathes to files
        keywords (list[str): list of keyword to be searched
        num_processes (int | None, optiona): number of processes to start. Default is None
    """
    start_time = time.time()

    if num_processes is None:
        num_processes = cpu_count()
    logging.info(f"Number on cpu: {num_processes}")

    chunk_size = len(files) // num_processes
    processes = []
    result_dict = defaultdict(list)
    lock = Lock()

    with Manager() as manager:
        shared_dict = manager.dict({word: manager.list([]) for word in keywords})
        for i in range(num_processes):
            start_index = i * chunk_size
            end_index = (i + 1) * chunk_size if i != num_processes - 1 else len(files)
            process_files = files[start_index:end_index]
            process = Process(target=worker, args=(find_keywords, process_files, keywords, shared_dict, lock))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        for key, value in shared_dict.items():
            result_dict[key] = list(value)

    time_multiprocessing_manager = time.time() - start_time

    print_results(time_multiprocessing_manager, result_dict, f"Time Multiprocessing with {num_processes} processes: ")