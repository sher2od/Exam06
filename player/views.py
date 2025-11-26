import json
from django.views import View
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404

from .models import Player


class PlayerView(View):


    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            data = json.loads(request.body)
            nickname = data.get('nickname')
            country = data.get('country')

            if not nickname or not country:
                return JsonResponse({"error": "nickname va country talab qilinadi"}, status=400)

         
            if Player.objects.filter(nickname=nickname).exists():
                return JsonResponse({"error": "Bu nickname allaqachon mavjud"}, status=400)

            player = Player.objects.create(
                nickname=nickname,
                country=country
            )

            return JsonResponse({
                "id": player.id,
                "nickname": player.nickname,
                "country": player.country,
                "rating": player.rating,
                "created_at": player.created_at.isoformat()
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        

    def get(self, request: HttpRequest) -> JsonResponse:
        players = Player.objects.all()

        users_list = []

        for user in players:
            users_list.append({
                "id": user.id,
                "nickname": user.nickname,
                "country": user.country,
                "rating": user.rating,
                "created_at": user.created_at.isoformat()
            })

   

        response_data = {
            "count":players.count(),
            "results":users_list
        }

        return JsonResponse(response_data,safe=False,status=201)
    


class PlayerDetailView(View):
    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        player_one = get_object_or_404(Player, pk=pk)

        data = {
            "id": player_one.id,
            "nickname": player_one.nickname,
            "country": player_one.country,
            "rating": player_one.rating,
            "created_at": player_one.created_at.isoformat()
        }

        return JsonResponse(data, status=200)
    
    def put(self,request:HttpRequest, pk: int) -> JsonResponse:
        player_one = get_object_or_404(Player,pk=pk)

        body = json.loads(request.body)

        nickname = body.get("nickname")
        country = body.get("country")
        rating = body.get("rating")

       

        if nickname:
            player_one.nickname = nickname
        if country:
            player_one.country = country
        if rating is not None:
            player_one.rating = rating

        player_one.save()

        data = {
                "id": player_one.id,
                "nickname": player_one.nickname,
                "country": player_one.country,
                "rating": player_one.rating,
                "created_at": player_one.created_at.isoformat()
                }
        
        return JsonResponse(data, status=200)
    
    def delete(self, request: HttpRequest, pk: int) -> JsonResponse:
        player_one = get_object_or_404(Player, pk=pk)
        player_one.delete()
        return JsonResponse({"message": "Player deleted successfully"}, status=204)


    