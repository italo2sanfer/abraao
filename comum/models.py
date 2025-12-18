from django.db import models

class Country(models.Model):
    name = models.CharField('Name', max_length=70, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return f"{self.name}"