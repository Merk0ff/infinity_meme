from random import choice

from utils.singleton import Singleton

from .integrations.dvch import DvchParser
from .parser import ParserABC


class ParserManager(metaclass=Singleton):
    list_of_parsers = []

    def __init__(self):
        self.list_of_parsers.append(DvchParser())

    def _check_status_and_fix(self, src_name='ALL'):
        if src_name == 'ALL':
            self.fix_all_parsers()

        src = next(i for i in self.list_of_parsers if i.name == src_name)
        status = src.check_status()

        if status == ParserABC.OK:
            return True
        elif status == ParserABC.NO_SRC:
            return src.fix_parser() == ParserABC.OK

        return False

    def get_random_images(self, count=30):
        src = choice(self.list_of_parsers)
        self._check_status_and_fix(src.name)

        return src.get_images(count) if src.status == ParserABC.OK else []

    def get_images_from_src(self, src_name, count=30):
        src = next(i for i in self.list_of_parsers if i.name == src_name)
        self._check_status_and_fix(src.name)

        return src.get_images(count) if src.status == ParserABC.OK else []

    def get_all_images_from_src(self, src_name):
        src = next(i for i in self.list_of_parsers if i.name == src_name)
        self._check_status_and_fix(src.name)

        return src.get_all_images() if src.status == ParserABC.OK else []

    def fix_all_parsers(self):
        status = {p.name: p.fix_parser() for p in self.list_of_parsers}

        return status
