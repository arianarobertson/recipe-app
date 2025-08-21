from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_allergen = models.BooleanField(default=False)

    def __str__(self):
        return self.name