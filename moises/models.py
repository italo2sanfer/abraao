from django.db import models


class Davi(models.Model):
    ROLE_OWN = 'Own'
    ROLE_CHOICES = (
        ("admin", "Admin"),
        (ROLE_OWN, ROLE_OWN),
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    role = models.CharField("Role", choices=ROLE_CHOICES, max_length=50)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Group(models.Model):
    davi = models.ForeignKey(Davi, verbose_name="Davi", on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=100, unique=True)
    description = models.CharField("Description", max_length=500)

    def __str__(self):
        return f"{self.name}"

class Judite(models.Model):
    davi = models.ForeignKey(Davi, verbose_name="Davi", on_delete=models.CASCADE)
    code = models.CharField("Code", max_length=70, unique=True)
    passwd = models.CharField("Passwd", max_length=300, unique=True)
    description = models.CharField("Description", max_length=500, blank=True)

    def __str__(self):
        return f"{self.code}"

    def set_passwd(self, password=None):
        from .utils import encrypt_password

        if not password:
            password = self.code
        self.passwd = encrypt_password(self.code, password)
        self.save()


class Paty(models.Model):
    davi = models.ForeignKey(Davi, verbose_name="Davi", on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=100)
    url = models.CharField("URL", max_length=100, blank=True)
    description = models.CharField("Description", max_length=500, blank=True)

    def __str__(self):
        return f"{self.name}"


class Joao(models.Model):
    davi = models.ForeignKey(Davi, verbose_name="Davi", on_delete=models.CASCADE)
    group = models.ForeignKey(Group, verbose_name="Group", on_delete=models.CASCADE)
    paty = models.ForeignKey(Paty, verbose_name="Paty", on_delete=models.CASCADE)
    login = models.CharField("Login", max_length=70)
    access = models.CharField("Access", max_length=500)
    description = models.CharField("Description", max_length=500, blank=True)

    def __str__(self):
        return f"{self.paty.name} - {self.login}"
