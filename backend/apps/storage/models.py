import pathlib
from typing import List, Dict

from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

from image.dataclass import MemeImage


class WrongStorage(KeyError):
    pass


class Storage(PolymorphicModel):
    name = models.CharField(max_length=100)
    capacity = models.PositiveBigIntegerField(
        default=2*1024*1024*1024  # 2 GB as default size
    )
    last_upload = models.DateTimeField(auto_now=True)
    last_balanced = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)

    def _api_upload_images(self, images: List[MemeImage]) -> Dict:
        raise NotImplementedError

    def _get_image(self, image) -> MemeImage:
        raise NotImplementedError

    def get_image(self, image_id) -> MemeImage:
        image = self.images.filter(id=image_id).first()

        if not image:
            raise WrongStorage

        return self._get_image(image)

    def _duplicate_checker(self, images: List[MemeImage]) -> List[MemeImage]:
        out = []

        for i in images:
            if self.images.filter(src_url=i.src_url).exists():
                i.close_image()
            else:
                out.append(i)

        return out

    def upload_images(self, images: List[MemeImage]) -> List:
        out = []

        images = self._duplicate_checker(images)
        paths = self._api_upload_images(images)
        self.last_upload = timezone.now()

        for i in images:
            obj, created = self.images.get_or_create(
                storage=self,
                path=paths[i.name],
                name=i.name,
                ext=i.ext,
                size=i.size,
                src=i.src,
                src_url=i.src_url,
            )

            if created:
                out.append(obj)

        return out


class LocalStorage(Storage):
    base_path = models.CharField(max_length=100)

    @staticmethod
    def __create_path(path: str):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    def __get_name_path(self, img_name: str):
        path_name = img_name.split('-')
        name = path_name.pop()

        return name, '{base}/{img}'.format(
            base=self.base_path,
            img='/'.join(path_name)
        )

    def __get_f_name(self, img: MemeImage):
        name, path = self.__get_name_path(str(img.name))

        return '{path}/{name}.{ext}'.format(
            path=path,
            name=name,
            ext=img.ext,
        )

    def __save_file(self, image: MemeImage):
        f_name = self.__get_f_name(image)

        image.image.save(f_name)
        image.size = pathlib.Path(f_name).stat().st_size

        return f_name

    def _api_upload_images(self, images: List[MemeImage]) -> Dict:
        out = {}

        for i in images:
            name, path = self.__get_name_path(str(i.name))
            self.__create_path(path)
            f_name = self.__save_file(i)
            out.update({
                i.name: f_name,
            })

        return out

    def _get_image(self, image) -> MemeImage:
        return MemeImage(image.path, image.src, image.src_url)
