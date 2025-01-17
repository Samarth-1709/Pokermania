from pypokerengine.api.game import setup_config, start_poker
import importlib.util
import sys
import json
import re
import io
from typing import final

def load_bot(filepath):
    spec = importlib.util.spec_from_file_location("Bot", filepath)
    bot = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bot)
    return bot.Bot()

def parse_poker_output_to_json(input_text):
    # Initialize the structure for the JSON data
    poker_data = {
        "street": [],
        "actions": {},
        "communitycards": []
    }

    lines = input_text.strip().splitlines()
    current_street = None
    community_cards = []

    for line in lines:
        line = line.strip()

        # Parse street start
        street_match = re.match(r'Street "(.*?)" started\. \(community card = (.*?)\)', line)
        if street_match:
            current_street = street_match.group(1)
            poker_data["street"].append(current_street)
            poker_data["actions"][current_street] = {
                "name": [],
                "action": [],
                "amount": []
            }
            # Parse and store community cards
            community_cards = eval(street_match.group(2))  # Converts string list to Python list
            poker_data["communitycards"].append(community_cards)
            continue

        # Parse player actions
        action_match = re.match(r'"(.*?)" declared "(.*?):(\d+)"', line)
        if action_match:
            player_name = action_match.group(1)
            action = action_match.group(2)
            amount = int(action_match.group(3))

            # Add to current street actions
            poker_data["actions"][current_street]["name"].append(player_name)
            poker_data["actions"][current_street]["action"].append(action)
            poker_data["actions"][current_street]["amount"].append(amount)
            continue

    return poker_data
    

def redirect_stdout_to_file(config, output_file):
    with open(output_file, "w") as file:
        original_stdout = sys.stdout
        try:
            sys.stdout = file
            result=start_poker(config, verbose=1)
        finally:
            sys.stdout = original_stdout
            return result

def read_output_file_and_parse(input_file):
    with open(input_file, "r") as file:
        content = file.read()

    poker_json = parse_poker_output_to_json(content)
    return poker_json

def load_bot(filepath):
    spec = importlib.util.spec_from_file_location("Bot", filepath)
    bot = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bot)
    return bot.Bot()


def play_match(bot1_path, bot2_path, bot1, bot2):
    """
    Simulates a match between two bots and updates their chips based on the outcome.
    """
    bot1_instance = load_bot(bot1_path)
    bot2_instance = load_bot(bot2_path)

    config = setup_config(max_round=1, initial_stack=1000, small_blind_amount=50)
    config.register_player(name=bot1.name, algorithm=bot1_instance)
    config.register_player(name=bot2.name, algorithm=bot2_instance)

    output_file = "poker_output.txt"
    result = redirect_stdout_to_file(config,output_file)
    replay_data = read_output_file_and_parse(output_file)
    
    bot1_stack = result["players"][0]["stack"]
    bot2_stack = result["players"][1]["stack"]

    chips_exchanged = abs(bot1_stack - bot2_stack)
    if bot1_stack > bot2_stack:
        bot1.chips_won += chips_exchanged
        bot2.chips_won -= chips_exchanged
        bot1.wins += 1
        winner = bot1.name
    else:
        bot1.chips_won -= chips_exchanged
        bot2.chips_won += chips_exchanged
        bot2.wins += 1
        winner = bot2.name
    
    bot1.total_games += 1
    bot2.total_games += 1

    bot1.save()
    bot2.save()
    hole_cards = [bot1_instance.hole_cards,bot2_instance.hole_cards]

    return winner, chips_exchanged, replay_data, hole_cards

# {
#     "street": ["preflop", "flop", "turn", "river"],
#     "actions": {
#         "preflop": {
#             "name": ["player1", "player2"],
#             "action": ["call", "call"],
#             "amount": [50, 50]
#         },
#         "flop": {
#             "name": ["player1", "player2"],
#             "action": ["raise", "call"],
#             "amount": [100, 100]
#         },
#         "turn": {
#             "name": ["player1", "player2"],
#             "action": ["raise", "call"],
#             "amount": [100, 100]
#         },
#         "river": {
#             "name": ["player1", "player2"],
#             "action": ["call", "call"],
#             "amount": [0, 0]
#         }
#     },
#     "communitycards": ["SA","HT","D4","D9","CK"]
# }