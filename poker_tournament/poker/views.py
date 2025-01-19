from django.http import JsonResponse
from .models import Bot, Match
from .utils import play_match
from django.contrib import messages
from django.contrib.auth import get_user_model,logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
import re

User = get_user_model()


# @api_view(['POST'])
# @permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        # Check if passwords match
        if password != confirmPassword:
            messages.error(request, "Passwords do not match!")
            return redirect('/login/')

        # # Check if password meets strength requirements
        # if len(password) < 8:
        #     messages.error(request, "Password must be at least 8 characters long.")
        #     return redirect('/login/')
        # if not re.search(r'\d', password):
        #     messages.error(request, "Password must contain at least one number.")
        #     return redirect('/login/')
        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        #     messages.error(request, "Password must contain at least one special character.")
        #     return redirect('/login/')
        # if not re.search(r'[A-Z]', password):
        #     messages.error(request, "Password must contain at least one uppercase letter.")
        #     return redirect('/login/')
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken!")
            return redirect('/login/')
        
        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        
        messages.info(request, "Account created Successfully!")
        return redirect('/login/')
    
    return render(request, 'login.html')



@login_required
def upload_bot(request):

    user = request.user
    bot_name = request.POST.get('name')
    bot_file = request.FILES['file']
    # if Bot.objects.filter(user=user).count() >= 3:
    #     return render(request, 'deploy.html', {'message': "You can only upload a maximum of 3 bots."})

    new_bot = Bot.objects.create(user=user, name=bot_name, file=bot_file)

    existing_bots = Bot.objects.exclude(user=user)

    for existing_bot in existing_bots:
        for match_number in range(1, 4):
            winner, chips_exchanged, replay_data, hole_cards = play_match(new_bot.file.path, existing_bot.file.path, new_bot, existing_bot)

            Match.objects.create(
                bot1=new_bot,
                bot2=existing_bot,
                winner=winner,
                chips_exchanged=chips_exchanged,
                match_number=match_number,
                replay_data=replay_data,
                hole_cards=hole_cards
            )

    return redirect('/my_bots/')
    


def leaderboard(request):
    bots = Bot.objects.all().order_by('-wins')
    data = []
    for idx, bot in enumerate(bots, start=1):
        win_rate = (bot.wins / bot.total_games * 100) if bot.total_games else 0
        earnings = f"${bot.chips_won:,.0f}"
        
        data.append({
            'rank': idx,
            'botName': bot.name,
            'owner': bot.user.username,
            'wins': bot.wins,
            'winRate': f"{win_rate:.1f}%",
            'earnings': earnings
        })
    
    return render(request, 'leaderboard.html', {'data': data})


def home(request):
    user_logged_in = request.user.is_authenticated
    return render(request, 'home.html', {'user_logged_in': user_logged_in})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        user = authenticate(username=username, password=password)
        
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/')
    
    return render(request, 'login.html')


@login_required
def my_bots(request):
    bots = Bot.objects.filter(user=request.user)
    selected_bot = request.GET.get('bot', 'all')
    
    bot_matches = {}

    if selected_bot != 'all':
        # Filter matches for the selected bot only
        selected_bot_instance = Bot.objects.get(name=selected_bot, user=request.user)
        matches_as_bot1 = Match.objects.filter(bot1=selected_bot_instance)
        matches_as_bot2 = Match.objects.filter(bot2=selected_bot_instance)
        matches = []
        for match in matches_as_bot1:
            matches.append({
                'bot_name': selected_bot_instance.name,
                'opponent': match.bot2.name,
                'result': match.winner,
                'date': match.played_at,
                'chips_exchanged': match.chips_exchanged,
                'game_id': match.game_id,
            })
        for match in matches_as_bot2:
            matches.append({
                'bot_name': selected_bot_instance.name,
                'opponent': match.bot1.name,
                'result': match.winner,
                'date': match.played_at,
                'chips_exchanged': match.chips_exchanged,
                'game_id': match.game_id,
            })
        bot_matches[selected_bot_instance.name] = matches
    else:
        for bot in bots:
            matches_as_bot1 = Match.objects.filter(bot1=bot)
            matches_as_bot2 = Match.objects.filter(bot2=bot)
            matches = []
            for match in matches_as_bot1:
                matches.append({
                    'bot_name': bot.name,
                    'opponent': match.bot2.name,
                    'result': match.winner,
                    'date': match.played_at,
                    'chips_exchanged': match.chips_exchanged,
                    'game_id': match.game_id,
                })
            for match in matches_as_bot2:
                matches.append({
                    'bot_name': bot.name,
                    'opponent': match.bot1.name,
                    'result': match.winner,
                    'date': match.played_at,
                    'chips_exchanged': match.chips_exchanged,
                    'game_id': match.game_id,
                })
            bot_matches[bot.name] = matches

    return render(request, 'bots.html', {
        'bots': bots,
        'bot_matches': bot_matches,
        'selected_bot': selected_bot,
    })


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def deploy_bot(request):
    return render(request, 'deploy.html')

def replay(request, game_id):
    match = Match.objects.get(game_id=game_id)
    player=""
    if(match.bot1.user == request.user):
        player="L"
    elif(match.bot2.user == request.user):
        player="R"
    else:
        return redirect('/my_bots/')   

    return render(request, 'game.html', {
        'match': match,
        "player":player
    })
    
def contact_us(request):
    return render(request, 'contact.html')

def documentation(request):
    return render(request, 'documentation.html')