import json
from django.views import View
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404

from .models import Score
from games.models import Game
from player.models import Player


class ScoreView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            data = json.loads(request.body)
            
            game_id = data.get('game')
            player_id = data.get('player')
            result = data.get('result')
            opponent_name = data.get('opponent_name', '')

            
            if not game_id or not player_id or not result:
                return JsonResponse({
                    "error": "game, player va result talab qilinadi"
                }, status=400)

            if result not in ['win', 'loss', 'draw']:
                return JsonResponse({
                    "error": "result faqat 'win', 'loss' yoki 'draw' bo'lishi mumkin"
                }, status=400)

            
            game = get_object_or_404(Game, pk=game_id)
            player = get_object_or_404(Player, pk=player_id)

            # hisoblash
            points_map = {
                'win': 10,
                'draw': 5,
                'loss': 0
            }
            points = points_map[result]

            # Score yaratish
            score = Score.objects.create(
                game=game,
                player=player,
                result=result,
                points=points,
                opponent_name=opponent_name
            )

            
            player.rating += points
            player.save()

            # Response
            return JsonResponse({
                "id": score.id,
                "game": {
                    "id": game.id,
                    "title": game.title
                },
                "player": {
                    "id": player.id,
                    "nickname": player.nickname
                },
                "result": score.result,
                "points": score.points,
                "opponent_name": score.opponent_name,
                "created_at": score.created_at.isoformat()
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    def get(self, request: HttpRequest) -> JsonResponse:
        scores = Score.objects.select_related('game', 'player').all().order_by('-created_at')

        score_list = []
        for score in scores:
            score_list.append({
                "id": score.id,
                "game": {
                "id": score.game.id,
                "title": score.game.title
            },
            "player": {
                "id": score.player.id,
                "nickname": score.player.nickname,
                "rating": score.player.rating
            },
            "result": score.result,
            "points": score.points,
            "opponent_name": score.opponent_name or "",
            "created_at": score.created_at.isoformat()
        })

        return JsonResponse(score_list, safe=False, status=200)
    

class ScoreDetailView(View):
    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        score = get_object_or_404(Score.objects.select_related('game', 'player'),pk=pk)

        data = {
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
        }

        return JsonResponse(data, status=200) 
    

    def delete(self,request:HttpRequest, pk:int) -> JsonResponse:
        try:
            score = get_object_or_404(Score, pk=pk)

            points_map = {'win':10, 'draw':4, 'loss':0}
            points_to_remove = points_map[score.result]

            player = score.player
            player.rating -= points_to_remove
            player.save()

            score.delete()

            return JsonResponse({
                "success":True,
                "message":"Score ochirildi",
                "remove_points":points_to_remove,
                "player_new_raiting":player.rating
            }, status=201
            )
        
        except Exception as s:
            return JsonResponse({"error":str(s)}, status=400)