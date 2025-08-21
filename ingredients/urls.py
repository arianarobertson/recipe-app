from django.urls import path
from .views import IngredientListView, IngredientDetailView

app_name = 'ingredients'

urlpatterns = [
    path('list/', IngredientListView.as_view(), name='ingredient-list'),
    path('list/<int:pk>/', IngredientDetailView.as_view(), name='ingredient-detail'),
]
