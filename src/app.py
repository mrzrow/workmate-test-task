from argparse import Namespace

from src.reports import AbstractReport, HandlersReport

class App:
    def __init__(self, args: Namespace):
        self.files = args.files
        self.report = self.get_report(args)

    def get_report(self, args: Namespace) -> AbstractReport:
        avaliable_reports = {
            'handlers': HandlersReport,
        }

        report_type = args.report
        if report_type not in avaliable_reports:
            raise ValueError('non-existent report type')
        
        report = avaliable_reports[report_type]
        return report(self.files)

    def generate_report(self) -> None:
        self.report.generate_report()
