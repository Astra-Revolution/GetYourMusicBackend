from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=60)

    def str(self):
        return self.name

    class Meta:
        db_table = 'regions'


class Province(models.Model):
    name = models.CharField(max_length=60)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def str(self):
        return self.name

    class Meta:
        db_table = 'provinces'


class District(models.Model):
    name = models.CharField(max_length=60)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def str(self):
        return self.name

    class Meta:
        db_table = 'districts'
