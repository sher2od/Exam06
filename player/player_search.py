from django.views import View
from django.http import JsonResponse,HttpRequest
from django.db.models import Q


from .models import Player

from django.views import View
from django.http import JsonResponse
from django.db.models import Q

from .models import Player

class PlayerSearchView(View):
    def get(self, request):
        country = request.GET.get('country')
        nickname = request.GET.get('nickname')
        min_rating = request.GET.get('min_rating')

        players = Player.objects.all()

        if country:
            players = players.filter(country__icontains=country)

        if nickname:
            players = players.filter(nickname__icontains=nickname)

        if min_rating:
            players = players.filter(rating__gte=min_rating)

        results = []
        for p in players:
            results.append({
                "id": p.id,
                "nickname": p.nickname,
                "country": p.country,
                "rating": p.rating,
                "created_at": p.created_at.isoformat()
            })

        return JsonResponse({
            "count": players.count(),
            "results": results
        }, status=200)
