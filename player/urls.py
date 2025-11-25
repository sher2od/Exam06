from django.urls import path

from .views import PlayerView,PlayerDetailView
from .player_search import PlayerSearchView


urlpatterns = [
    path('players/', PlayerView.as_view(), name='player_use'),
    path('players/search/',PlayerSearchView.as_view(),name='plyer_search'),
    path('players/<int:pk>/',PlayerDetailView.as_view(),name='one_player')
    
]