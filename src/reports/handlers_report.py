import re
import os
import multiprocessing
from collections import defaultdict, Counter

from src.reports.abstract_report import AbstractReport

class HandlersReport(AbstractReport):
    def __init__(self, files: tuple[str, ...]):
        self.files = files

    def parse_endpoint(self, information: str) -> str | None:
        reg_expr = r'(/\w[\w/\-._]*/)'

        for token in information.strip().split():
            if re.fullmatch(reg_expr, token):
                return token
        
        return None


    def parse_file(self, filename: str) -> defaultdict[Counter, int]:
        result = defaultdict(Counter)

        with open(filename, 'r') as file:
            for line in file:
                _, _, log_status, log_type, log_information = line.strip().split(maxsplit=4)

                if log_type == 'django.request:':
                    endpoint = self.parse_endpoint(log_information)
                    if endpoint is not None:
                        result[endpoint][log_status] += 1

        return result
    
    def merge_results(self, results: list[defaultdict[Counter, int]]) -> defaultdict[Counter, int]:
        merged = defaultdict(Counter)

        for result in results:
            for endpoint, counter in result.items():
                merged[endpoint].update(counter)
        
        return merged

    def show_results(self, results: defaultdict[Counter, int]) -> None:
        header = 'HANDLERS'
        statuses = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        handler_len = len(max(results.keys(), key=len)) + 2
        statuses_len = 12

        print(f'\n{header:<{handler_len}}', end='')
        for header in statuses:
            print(f'{header:<{statuses_len}}', end='')
        print()

        total = Counter()
        for endpoint, counter in results.items():
            print(f'{endpoint:<{handler_len}}', end='')
            for status in statuses:
                count = counter.get(status, 0)
                total[status] += count
                print(f'{count:<{statuses_len}}', end='')
            print()

        print(f'{"":<{handler_len}}', end='')
        for status in statuses:
            print(f'{total[status]:<{statuses_len}}', end='')
        print(f'\n\nTotal requests: {sum(total.values())}\n')

    def generate_report(self):
        with multiprocessing.Pool(processes=os.cpu_count()) as pool:
            results = pool.map(self.parse_file, self.files)

        merged = self.merge_results(results)
        self.show_results(merged)
