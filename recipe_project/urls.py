from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from recipes import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', RedirectView.as_view(url='/recipes/', permanent=False)),  # root → /recipes/
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),
    path('categories/', include('categories.urls')),
    path('ingredients/', include('ingredients.urls')),
    path('tags/', include('tags.urls')),
    path('ratings/', include('ratings.urls')),

    # 🔑 Auth (login/logout)
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_success'), name='logout'),
    path('logout_success/', TemplateView.as_view(template_name='recipes/success.html'), name='logout_success'),
]

# 👇 This serves media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
