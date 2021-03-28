from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from locations.models import District
from media_system.models import Genre, Instrument


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField('active', default=True)
    is_confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'


class Profile(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60, null=True)
    birth_date = models.CharField(max_length=60, null=True)
    phone = models.CharField(max_length=60, null=True)
    type = models.CharField(max_length=60, null=True)
    register_date = models.CharField(max_length=60, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'profiles'


class Musician(Profile):
    musicians = models.OneToOneField(Profile, auto_created=True, on_delete=models.CASCADE, parent_link=True,
                                     primary_key=True, serialize=False)
    artistic_name = models.CharField(max_length=100, null=True)
    rating = models.FloatField(default=0)
    genres = models.ManyToManyField(Genre, related_name='musicians')
    instruments = models.ManyToManyField(Instrument, related_name='musicians')

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'musicians'


class Organizer(Profile):
    organizers = models.OneToOneField(Profile, auto_created=True, on_delete=models.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False)

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'organizers'


class Following(models.Model):
    follower = models.ForeignKey(Musician, on_delete=models.CASCADE)
    followed = models.ForeignKey(Musician, on_delete=models.CASCADE, related_name='followed')
    follow_date = models.CharField(max_length=60)

    class Meta:
        db_table = 'following'
