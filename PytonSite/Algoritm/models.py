from django.db import models

class People(models.Model):
    Id = models.BigAutoField('ID', primary_key=True)
    FIO = models.CharField("FIO", max_length=50)
    Encodings = models.JSONField("Encodings")

class Image(models.Model):
    Id = models.BigAutoField('ID', primary_key=True)
    IdUser = models.ForeignKey(People, on_delete = models.CASCADE)
    Image = models.CharField("Image", max_length=255)

