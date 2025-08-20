from django.db import models
from recipes.models import Recipe
from django.contrib.auth.models import User

# Create your models here.


class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # assuming you want user ratings
    rating = models.PositiveSmallIntegerField()  # e.g. 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.rating} for {self.recipe.name} by {self.user.username}"
