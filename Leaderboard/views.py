from django.views import View
from django.http import JsonResponse, HttpRequest
from django.db.models import Count, Q
from player.models import Player
from score.models import Score


class LeaderboardView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        game_id = request.GET.get("game_id")

        if not game_id:
            return JsonResponse({"error": "game_id is required"}, status=400)

        # O‘sha turnirdagi barcha score’lar
        scores = Score.objects.filter(game_id=game_id)

        # Natijalar player bo‘yicha guruhlanadi
        leaderboard = {}

        for s in scores:
            p = s.player_id

            if p not in leaderboard:
                leaderboard[p] = {
                    "player": s.player.nickname,
                    "player_id": s.player.id,
                    "country": s.player.country,
                    "rating": s.player.rating,
                    "wins": 0,
                    "draws": 0,
                    "losses": 0,
                    "points": 0,
                }

            # Result bo‘yicha ball qo‘shiladi
            if s.result == "win":
                leaderboard[p]["wins"] += 1
                leaderboard[p]["points"] += 10
            elif s.result == "draw":
                leaderboard[p]["draws"] += 1
                leaderboard[p]["points"] += 5
            elif s.result == "loss":
                leaderboard[p]["losses"] += 1

        # Lug‘atni listga aylantiramiz
        data = list(leaderboard.values())

        # Points bo‘yicha sort qilamiz
        data.sort(key=lambda x: x["points"], reverse=True)

        # Rank va rating_change qo‘shamiz
        for i, item in enumerate(data, start=1):
            item["rank"] = i
            item["rating_change"] = item["points"]

        return JsonResponse(data, safe=False, status=200)
