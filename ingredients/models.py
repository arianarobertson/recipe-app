from django.db import models

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    is_allergen = models.BooleanField(default=False)

    def __str__(self):
        return self.name
