from collections import defaultdict
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def print_results(time:float, result_dict:defaultdict, title="Time: "):
    print("-" * 80)
    print(f"{title} {time}")
    for key, value in sorted(result_dict.items()):
        print(f"{key}: {value}")
    print("-" * 80)