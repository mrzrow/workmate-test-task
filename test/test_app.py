import pytest
from argparse import Namespace

from src.app import App
from src.reports import HandlersReport


@pytest.fixture
def args():
    return Namespace(files=('./test/test1.log',), report='handlers')


def test_invalid_report_type(args):
    report_type = 'non-existent'
    bad_args = Namespace(files=args.files, report=report_type)
    with pytest.raises(ValueError, match=f'non-existent report type: {report_type}'):
        App(bad_args)


def test_valid_report_type(args):
    app = App(args)
    assert isinstance(app.report, HandlersReport), f'Expected {HandlersReport}, but got {type(app.report)}'


def test_invalid_log_filenames():
    file = 'non-existent.log'
    bad_args = Namespace(files=(file,), report='handlers')
    with pytest.raises(FileNotFoundError, match=f'file not found: {file}'):
        App(bad_args)


def test_valid_log_filenames(args):
    app = App(args)
    assert app.files == tuple(args.files)
