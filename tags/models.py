from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class ProduktTagManager(models.Model):
    def get_tags_for(self,obj_type,obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return ProduktTag.objects \
            .select_related('nazwa') \
            .filter(
            content_type=content_type,
            object_id =obj_id
        )

class Tag(models.Model):
    nazwa = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.nazwa

class ProduktTag(models.Model):
    obj = ProduktTagManager()
    nazwa = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    rzecz_kontent = GenericForeignKey()
