from django.db import models

class Judite(models.Model):
    code = models.CharField('Code', max_length=70, unique=True)
    passwd = models.CharField('Passwd', max_length=70, blank=True)
    description = models.CharField('Description', max_length=500, blank=True)

    def __str__(self):
        return f'{self.code}'    
    
class Paty(models.Model):
    name = models.CharField('Name', max_length=100)
    url = models.CharField('URL', max_length=100, blank=True)
    description = models.CharField('Description', max_length=500, blank=True)

    def __str__(self):
        return f'{self.name}'

class Joao(models.Model):

    WHO_CHOICES = (
        ('Italo', 'Italo'),
        ('Vivia', 'Vivia'),
        ('Angelica', 'Angelica'),
        ('Telia', 'Télia'),
        ('Valdir', 'Valdir'),
        ('Penha', 'Penha')
    )

    paty = models.ForeignKey(Paty, verbose_name='Paty', on_delete=models.CASCADE)
    who = models.CharField('Who', choices=WHO_CHOICES, max_length=50)
    login = models.CharField('Login', max_length=70)
    access = models.CharField('Access', max_length=500)
    description = models.CharField('Description', max_length=500, blank=True)

    def __str__(self):
        return f'{self.paty.name} - {self.login}'    