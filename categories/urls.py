from django.urls import path
from .views import CategoryListView, CategoryDetailView

app_name = 'categories'

urlpatterns = [
    path('list/', CategoryListView.as_view(), name='category-list'),
    path('list/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]
