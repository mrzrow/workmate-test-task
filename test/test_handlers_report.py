import pytest
from collections import defaultdict, Counter

from src.reports.handlers_report import HandlersReport

@pytest.fixture
def log_file():
    return './test/test1.log'


@pytest.fixture
def report(log_file):
    return HandlersReport((log_file))


def test_parse_endpoint(report):
    tests = (
        ('/api/', '/api/'),
        ('not /api/v1/admin/', '/api/v1/admin/'),
        ('/api/v1/admin/ not', '/api/v1/admin/'),
        ('not endpoint /api/v1/ not', '/api/v1/'),
        ('not endpoint', None),
        ('', None),
        ('    ', None),
    )

    for value, expected in tests:
        result = report.parse_endpoint(value)
        assert result == expected, f'Expected {expected}, but got {result}'


def test_parse_file(report, log_file):
    result = report.parse_file(log_file)

    expected = defaultdict(
        Counter,
        {
            '/api/v1/reviews/': Counter({
                'INFO': 1,
                'WARNING': 2,
            }),
            '/admin/dashboard/': Counter({
                'ERROR': 1,
            }),
        }
    )

    assert result == expected, f'Expected {expected}, but got {result}'


def test_merge_results(report):
    result1 = defaultdict(
        Counter, 
        {
            '/api/v1/test/1/': Counter({
                'INFO': 1,
                'WARNING': 2,
            }),
            '/api/v1/test/2/': Counter({
                'INFO': 3,
                'DEBUG': 3,
            }),
        }
    )
    result2 = defaultdict(
        Counter,
        {
            '/api/v1/test/1/': Counter({
                'INFO': 3,
                'DEBUG': 2,
            }),
            '/api/v1/test/3/': Counter({
                'ERROR': 4,
            }),
        }
    )
    merged = report.merge_results([result1, result2])
    
    expected = defaultdict(
        Counter,
        {
            '/api/v1/test/1/': Counter({
                'DEBUG': 2,
                'INFO': 4,
                'WARNING': 2,
            }),
            '/api/v1/test/2/': Counter({
                'INFO': 3,
                'DEBUG': 3,
            }),
            '/api/v1/test/3/': Counter({
                'ERROR': 4,
            }),
        }
    )

    assert merged == expected, f'Expected {expected}, but got {merged}'
