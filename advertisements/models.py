from django.conf import settings
from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"

class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

class Favorite(models.Model):
    favorite = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )






    # favorites = GenericRelation('Favorite')

# class Favorite(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveBigIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')

#     class Meta:
#         verbose_name = 'Избраное'
#         verbose_name_plural = 'Избранные'
#         ordering = ['-id']
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'object_id', 'content_type'],
#                 name = 'unique_user_content_type_object_id'
#             )
#         ]


