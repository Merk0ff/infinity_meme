from celery import shared_task

from post.models import Post
from storage.models import Storage

from . import general_parser


@shared_task
def download_memes(meme_count):
    storage = Storage.objects.last()

    imgs = general_parser.get_random_images(meme_count)
    saved_imgs = storage.upload_images(imgs)

    for i in saved_imgs:
        post = Post.objects.create()
        post.images.add(i)
        post.save()

    for i in imgs:
        i.close_image()

    return len(saved_imgs)

