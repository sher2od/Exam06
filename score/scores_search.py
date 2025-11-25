from django.views import View
from django.http import JsonResponse,HttpRequest
from django.db.models import Q


from .models import Score

class ScoreSearchView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        queryset = Score.objects.select_related('game', 'player').all()

        game_id = request.GET.get('game_id')
        player_id = request.GET.get('player_id')
        result = request.GET.get('result')

        if game_id:
            queryset = queryset.filter(game_id=game_id)
        if player_id:
            queryset = queryset.filter(player_id=player_id)
        if result:
            if result not in ['win', 'loss', 'draw']:
                return JsonResponse({
                "error": "result faqat 'win', 'loss' yoki 'draw' bo'lishi mumkin"
                }, status=400)
            queryset = queryset.filter(result=result)


        queryset = queryset.order_by('-created_at')


        results = []
        for score in queryset:
            results.append({
                "id": score.id,
                "game": {
                    "id": score.game.id,
                    "title": score.game.title
            },
            "player": {
                "id": score.player.id,
                "nickname": score.player.nickname
            },
            "result": score.result,
            "points": score.points,
            "opponent_name": score.opponent_name or "",
            "created_at": score.created_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        })


        response = {
            "count": len(results),
            "results": results
        }

        return JsonResponse(response, safe=False, status=200)