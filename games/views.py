from django.views import View
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from .models import Game
import json

from datetime import datetime

class GamesView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        games_list = []
        for game in Game.objects.all():
            games_list.append({
                "id": game.id,
                "title": game.title,
                "location": game.location,
                "start_date": game.start_date.isoformat(),
                "description": game.description,
                "created_at": game.created_at.isoformat()
            })
        return JsonResponse(games_list, safe=False)

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            data = json.loads(request.body)
            title = data.get("title")
            location = data.get("location")
            start_date = data.get("start_date")
            description = data.get("description", "")

            if not title or not location or not start_date:
                return JsonResponse({"error": "Title, location and start_date are required."}, status=400)

            game = Game.objects.create(
                title=title,
                location=location,
                start_date=start_date,
                description=description
            )

            return JsonResponse({
                "id": game.id,
                "title": game.title,
                "location": game.location,
                "start_date": game.start_date,
                "description": game.description,
                "created_at": game.created_at.isoformat()
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)


class GameDetailView(View):
    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        game = get_object_or_404(Game, pk=pk)
        return JsonResponse({
            "id": game.id,
            "title": game.title,
            "location": game.location,
            "start_date": game.start_date.isoformat(),
            "description": game.description,
            "created_at": game.created_at.isoformat()
        })
    

    def put(self, request: HttpRequest, pk:int) -> JsonResponse:
        game = get_object_or_404(Game, pk=pk)
        data = json.loads(request.body)
        
     
        game.title = data.get("title", game.title)
        game.location = data.get("location", game.location)
            
        if "start_date" in data:
            game.start_date = datetime.fromisoformat(data["start_date"]).date()
        
        game.description = data.get("description", game.description)
        
        game.save()
        
        return JsonResponse({
            "id": game.id,
            "title": game.title,
            "location": game.location,
            "start_date": game.start_date.isoformat(),
            "description": game.description,
            "created_at": game.created_at.isoformat()
            }, status=200)   # ← status bu yerda bo‘lishi kerak
    

    def delete(self, request, pk: int) -> JsonResponse:
        game = get_object_or_404(Game, pk=pk)
        game.delete()
        
        return JsonResponse(
            {"message": "Game deleted successfully"},
            status=204  # 204 = muvaffaqiyatli o‘chirildi (body bo‘lishi shart emas)
        )


