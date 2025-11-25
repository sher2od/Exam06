from django.urls import path

from .views import ScoreView,ScoreDetailView
from .scores_search import ScoreSearchView


urlpatterns = [
    path('scores/', ScoreView.as_view(), name='score'), 
    path('scores/search/',ScoreSearchView.as_view(), name='search'),
    path('scores/<int:pk>/',ScoreDetailView.as_view(),name='search')


]