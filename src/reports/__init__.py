from src.reports.abstract_report import AbstractReport
from src.reports.handlers_report import HandlersReport

available_reports = {
    'handlers': HandlersReport
}

__all__ = [AbstractReport, HandlersReport, available_reports]
