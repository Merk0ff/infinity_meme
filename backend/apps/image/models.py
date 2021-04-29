from django.db import models
from .dataclass import MemeImage


class Image(models.Model):
    storage = models.ForeignKey(
        'storage.Storage',
        on_delete=models.CASCADE,
        related_name='images',
    )
    path = models.CharField(max_length=100)
    name = models.UUIDField()
    ext = models.CharField(max_length=10)
    size = models.PositiveIntegerField()
    src = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)
    src_url = models.CharField(max_length=100)

    def get_image(self) -> MemeImage:
        return self.storage.get_image(self.id)
