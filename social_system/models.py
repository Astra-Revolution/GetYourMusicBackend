from django.db import models
from users_system.models import Profile, Musician


class Publication(models.Model):
    video_url = models.CharField(max_length=300)
    content = models.CharField(max_length=200)
    update_time = models.CharField(max_length=60)
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)

    def str(self):
        return self.content

    class Meta:
        db_table = 'publications'


class Comment(models.Model):
    text = models.CharField(max_length=200)
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    def str(self):
        return self.text

    class Meta:
        db_table = 'comments'