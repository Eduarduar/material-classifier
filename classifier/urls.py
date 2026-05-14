from django.urls import path
from . import views

urlpatterns = [
    path('classify/', views.ClassifyView.as_view(), name='classify'),
    path('correct/', views.CorrectClassificationView.as_view(), name='correct'),
    path('health/', views.HealthView.as_view(), name='health'),
]