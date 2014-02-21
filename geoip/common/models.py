from django.db import models


class Base(models.Model):

    class Meta:
        abstract = True

    def as_dict(self):
        return {field.name: getattr(self, field.name)
                for field in self._meta.fields
                }

    def __unicode__(self):
        return str(self.as_dict())
