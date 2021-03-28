
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=60)

    def str(self):
        return self.name

    class Meta:
        db_table = 'genres'


class Instrument(models.Model):
    name = models.CharField(max_length=60)

    def str(self):
        return self.name

    class Meta:
        db_table = 'instruments'
