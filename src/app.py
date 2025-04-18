import os
from argparse import Namespace

from src.reports import AbstractReport, available_reports


class App:
    def __init__(self, args: Namespace):
        self.files = self.get_files(args)
        self.report = self.get_report(args)

    def get_files(self, args: Namespace) -> tuple[str, ...]:
        files = args.files
        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"file not found: {file}")
        return tuple(files)

    def get_report(self, args: Namespace) -> AbstractReport:
        report_type = args.report
        if report_type not in available_reports:
            raise ValueError(f'non-existent report type: {report_type}')

        report = available_reports[report_type]
        return report(self.files)

    def generate_report(self) -> None:
        self.report.generate_report()
