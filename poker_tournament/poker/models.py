from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    
    # Fix related_name conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="custom_user_permissions_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )


class Bot(models.Model):
    user = models.ForeignKey('poker.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='bots/')
    created_at = models.DateTimeField(auto_now_add=True)
    wins=models.IntegerField(default=0)
    total_games=models.IntegerField(default=0)
    chips_won = models.IntegerField(default=0)


class Match(models.Model):
    game_id = models.AutoField(primary_key=True)
    bot1 = models.ForeignKey(Bot, related_name='matches_as_bot1', on_delete=models.CASCADE)
    bot2 = models.ForeignKey(Bot, related_name='matches_as_bot2', on_delete=models.CASCADE)
    winner=models.CharField(max_length=50)
    chips_exchanged = models.IntegerField(default=0)
    match_number = models.PositiveIntegerField()
    played_at = models.DateTimeField(auto_now_add=True)
    replay_data = models.JSONField()
    hole_cards = models.JSONField()
