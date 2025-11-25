from django.db import models
from games.models import Game
from player.models import Player   # agar Player boshqa appda bo‘lsa shu tarzda chaqiriladi


class Score(models.Model):
    RESULT_CHOICES = [
        ('win', 'Win'),
        ('loss', 'Loss'),
        ('draw', 'Draw'),
    ]

    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,
        related_name="scores"
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name="scores"
    )

    result = models.CharField(
        max_length=10,
        choices=RESULT_CHOICES
    )

    points = models.IntegerField()   # win=10, draw=5, loss=0 — API ichida set qilasan

    opponent_name = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.player.nickname} - {self.result} ({self.points})"
