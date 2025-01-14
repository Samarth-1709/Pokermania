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
    return render(request,'home.html')


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
    


def leaderboard(request):
    # Fetch bots and order by wins
    bots = Bot.objects.all().order_by('-wins')
    
    # Prepare the leaderboard data
    data = []
    for idx, bot in enumerate(bots, start=1):
        win_rate = (bot.wins / bot.total_games * 100) if bot.total_games else 0  # Avoid division by zero
        earnings = f"${bot.chips_won:,.0f}"
        
        data.append({
            'rank': idx,
            'botName': bot.name,
            'owner': bot.user.username,
            'wins': bot.wins,
            'totalGames': bot.total_games,
            'winRate': f"{win_rate:.1f}%",
            'earnings': earnings
        })
    
    return render(request, 'leaderboard.html', {'data': data})


def home(request):
    user_logged_in = request.user.is_authenticated
    return render(request, 'home.html', {'user_logged_in': user_logged_in})

def login(request):
    return render(request, 'login.html')

@permission_classes([IsAuthenticated])
def my_bots(request):
    bots = Bot.objects.filter(user=request.user)
    return render(request, 'bots.html', {'bots': bots})

def bot_replays(request):
    bot_name = request.GET.get('bot_name', 'all')

    # Get bot matches based on the selected bot filter
    if bot_name == 'all':
        matches = Match.objects.all()
    else:
        bot = Bot.objects.get(name=bot_name)
        matches = Match.objects.filter(bot1=bot) | Match.objects.filter(bot2=bot)

    replay_data = []
    for match in matches:
        opponent = match.bot2 if match.bot1.name == bot_name else match.bot1
        replay_data.append({
            'replay_id': match.game_id,
            'bot_name': bot_name,
            'opponent': opponent.name,
            'date': match.played_at.strftime('%Y-%m-%d'),
            'result': match.winner,
            'earnings': f"${match.chips_exchanged}",
        })

    return JsonResponse(replay_data, safe=False)



def logout_view(request):
    logout(request)
    return redirect('home')

def replay(request, game_id):
    match = Match.objects.get(game_id=game_id)
    return render(request, 'game.html', {'match': match})

def deploy_bot(request):
    return render(request, 'deploy.html')
