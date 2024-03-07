from django.db import models
from django.contrib.auth.models import User


# tabulka pojištění
class Pojisteni(models.Model):
  title = models.CharField(max_length=200)

  def __str__(self):
    return self.title

# Tabulka pojištěnců
class Pojistenec(models.Model):
  name = models.CharField(max_length=20)
  surname = models.CharField(max_length=20)
  email = models.EmailField()
  phone = models.CharField(max_length=20)
  street = models.CharField(max_length=100)
  city = models.CharField(max_length=50)
  psc = models.CharField(max_length=20)
  isPaid = models.BooleanField(default=False)
  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  pojisteni = models.ManyToManyField(Pojisteni)

  def __str__(self):
    return self.name



