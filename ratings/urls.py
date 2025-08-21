from django.urls import path
from .views import RatingListView, RatingDetailView

app_name = 'ratings'

urlpatterns = [
    path('list/', RatingListView.as_view(), name='rating-list'),
    path('list/<int:pk>/', RatingDetailView.as_view(), name='rating-detail'),
]
