from abc import ABC, abstractmethod


class ParserABC(ABC):
    name = None

    OK = 'ok'
    NO_SRC = 'noSrc'

    status = OK

    @abstractmethod
    def get_images(self, count):
        raise NotImplementedError

    @abstractmethod
    def get_all_images(self):
        raise NotImplementedError

    @abstractmethod
    def fix_parser(self):
        raise NotImplementedError

    @abstractmethod
    def check_status(self):
        raise NotImplementedError
