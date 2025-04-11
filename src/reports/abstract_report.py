from abc import ABC, abstractmethod

class AbstractReport(ABC):
    @abstractmethod
    def generate_report(self):
        raise NotImplementedError
