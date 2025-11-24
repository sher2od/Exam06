from django.urls import path
from .views import GamesView, GameDetailView

urlpatterns = [
    path('games/', GamesView.as_view(), name='games-list'),  # GET va POST uchun
    path('games/<int:pk>/', GameDetailView.as_view(), name='game-detail'),  # ID bo‘yicha GET
]
