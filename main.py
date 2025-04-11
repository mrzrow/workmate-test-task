import argparse

from src.app import App


def extract_arguments() -> argparse.Namespace:
    usage = 'python %(prog)s [file1 file2 ...] --report [report_name]'
    parser = argparse.ArgumentParser(prog='main.py', usage=usage)
    parser.add_argument('files', nargs='+', help='log files')
    parser.add_argument('--report', required=True, help='report type')
    return parser.parse_args()


if __name__ == '__main__':
    args = extract_arguments()

    app = App(args)
    app.generate_report()
