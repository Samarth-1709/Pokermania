from django.http import JsonResponse
from .models import Bot, Match
from .utils import play_match
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model,logout
from django.shortcuts import render,redirect

User = get_user_model()


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already taken'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    return JsonResponse({'message': 'User registered successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_bot(request):
    """
    Handles bot file upload and triggers matches with all existing bots.
    """
    user = request.user
    bot_name = request.data.get('name')
    bot_file = request.FILES['file']

    new_bot = Bot.objects.create(user=user, name=bot_name, file=bot_file, chips=10000)

    existing_bots = Bot.objects.exclude(id=new_bot.id)

    for existing_bot in existing_bots:
        for match_number in range(1, 4):
            winner, chips_exchanged, replay_data, hole_cards = play_match(new_bot.file.path, existing_bot.file.path, new_bot, existing_bot)

            # Save match details in the database
            Match.objects.create(
                bot1=new_bot,
                bot2=existing_bot,
                winner=winner,
                chips_exchanged=chips_exchanged,
                match_number=match_number,
                replay_data=replay_data,
                hole_cards=hole_cards
            )

    return JsonResponse({
        'message': 'Bot uploaded successfully',
    })

@api_view(['GET'])
def leaderboard(request):
    bots = Bot.objects.all().order_by('-wins')
    data = [{'name': bot.name, 'wins': bot.wins, 'chips_won': bot.chips_won , 'owner': bot.user.username} for bot in bots]
    return render(request, 'leaderboard.html', {'data': data})

def home(request):
    user_logged_in = request.user.is_authenticated
    return render(request, 'home.html', {'user_logged_in': user_logged_in})

def login(request):
    return render(request, 'login.html')

@permission_classes([IsAuthenticated])
def my_bots(request):
    bots = Bot.objects.filter(user=request.user)
    return render(request, 'bots.html',{'bots': bots})

def logout(request):
    logout(request)
    return redirect('home')

def replay(request, game_id):
    match = Match.objects.get(game_id=game_id)
    return render(request, 'game.html', {'match': match})

def deploy_bot(request):
    return render(request, 'deploy.html')
