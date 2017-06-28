from django.db import models


class Album(models.Model):
    artist = models.CharField(max_length=130)
    title = models.CharField(max_length=250)
    genre = models.CharField(max_length=70)
    logo = models.CharField(max_length=1000)

    def __str__(self):
        return " BY ".join((self.title, self.artist))

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return " FROM ".join((self.title, str(self.album)))
