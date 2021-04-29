import io

from contextlib import contextmanager


@contextmanager
def get_raw_images(images):
    raw_images = [i.get_image() for i in images]
    yield [i.image for i in raw_images]
    [i.close_image for i in raw_images]


@contextmanager
def get_raw_image(image):
    raw_images = image.get_image()
    img_bytes = io.BytesIO()
    raw_images.image.save(img_bytes, format=raw_images.image.format)

    yield img_bytes.getvalue()

    raw_images.close_image()
    img_bytes.close()
