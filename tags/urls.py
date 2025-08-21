from django.urls import path
from .views import TagListView, TagDetailView

app_name = 'tags'

urlpatterns = [
    path('list/', TagListView.as_view(), name='tag-list'),
    path('list/<int:pk>/', TagDetailView.as_view(), name='tag-detail'),
]
