from bs4 import BeautifulSoup as bs
from PIL import UnidentifiedImageError
from requests import get

from image.dataclass import MemeImage
from parsers.parser import ParserABC

DVCH_LINK = 'https://2ch.hk'
DVCH_KEYWORDS = [
    'засмеялся',
    'засмеявся'
]
NAME = '2ch'


class Thread:
    post_id = None
    images_count = None
    images_parsed = 0
    _soup = None
    _all_posts = None

    def __init__(self, post_id):
        self.post_id = post_id

        self._refresh()

    def _refresh(self):
        html = get(f'{DVCH_LINK}/b/res/{self.post_id}.html', timeout=3)

        if html.status_code != 200:
            raise EOFError

        self._soup = bs(html.text, "html.parser")

        self._all_posts = self._soup.find_all(class_='thread__post')
        self.images_count = len(self._soup.find_all(class_='post__image'))

        return self.images_count - self.images_parsed

    def is_alive(self):
        if self.images_count <= self.images_parsed:
            try:
                if self._refresh() <= 0:
                    return False
            except EOFError:
                return False

        return True

    def get_images(self, count):
        count = min(count, self.images_count - self.images_parsed)
        out = []

        if count <= 0:
            raise IndexError

        posts = self._all_posts[self.images_parsed:(self.images_parsed + count)]

        for post in posts:
            images = post.find_all(class_='post__image')

            for image in images:
                img = None
                href = image.find('a')['href']
                raw = get(f'{DVCH_LINK}{href}', stream=True)

                if raw.status_code != 200:
                    continue

                raw = raw.raw
                raw.decode_content = True

                try:
                    img = MemeImage(raw, NAME, href)
                except UnidentifiedImageError:
                    pass

                if img:
                    out.append(img)
                self.images_parsed += 1

        return count, out


class DvchParser(ParserABC):
    name = None
    _threads = []

    def __init__(self):
        self.name = NAME

        self._get_threads()

    def _recursive_get_images(self, count, out=None):
        if out is None:
            out = []

        thread = None

        for tr in self._threads:
            if not tr.is_alive():
                self._threads.remove(tr)
            else:
                thread = tr
                break

        if not thread:
            self._get_threads()
            self._recursive_get_images(count, out)

        cnt, out_tmp = thread.get_images(count)
        out += out_tmp

        if cnt < count:
            self._recursive_get_images(count - cnt, out)

        return out

    def get_images(self, count):
        return self._recursive_get_images(count)

    def get_all_images(self):
        count = sum(i.images_count - i.images_parsed for i in self._threads)

        return self.get_images(count)

    def check_status(self):
        self.status = self.OK if len([t for t in self._threads if t.is_alive()])\
                      else self.NO_SRC

        return self.status

    def fix_parser(self):
        self._threads = [t for t in self._threads if t.is_alive()]

        if len(self._threads) == 0:
            self._get_threads()

        return self.status

    def _get_threads(self):
        resp = get(f'{DVCH_LINK}/b/catalog_num.json')

        if resp.status_code != 200:
            raise PermissionError

        catalog = resp.json()['threads']

        for t in catalog:
            subject = t['subject'].lower()

            if any(word in subject for word in DVCH_KEYWORDS):
                self._threads.append(Thread(t['num']))

        if len(self._threads) == 0:
            self.status = self.NO_SRC
