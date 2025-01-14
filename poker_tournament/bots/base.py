from pypokerengine.players import BasePokerPlayer

class Base(BasePokerPlayer):
    
    def __init__(self):
        # Store the history of actions, community cards, and pot
        self.hole_cards=[]
        
    def declare_action(self, valid_actions, hole_card, round_state):
        pass
    
    def receive_game_start_message(self, game_info):
        pass
    
    def receive_round_start_message(self, round_count, hole_card, seats):
        self.hole_cards=hole_card

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, new_action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass
    