from django.contrib import admin
from .models import User, Bot, Match

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'wins', 'chips_won')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at',)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'bot1', 'bot2', 'winner', 'chips_exchanged', 'played_at')
    search_fields = ('bot1__name', 'bot2__name', 'winner')
    list_filter = ('played_at',)
    readonly_fields = ('game_id', 'played_at')
