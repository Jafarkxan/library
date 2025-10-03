from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField()
    price = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.title
