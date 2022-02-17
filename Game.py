import time

import Player
from Deck import Deck
from Const import MESSAGES

import random


class Game:
    max_pl_count = 4

    def __init__(self):
        self.players = []
        self.player = None
        self.player_pos = None
        self.dealer = Player.Dealer()
        self.all_players_count = 1
        self.deck = Deck()
        self.max_bet, self.min_bet = 20, 0

    @staticmethod
    def _ask_starting(message):
        while True:
            choice = input(message)
            if choice == 'Ні':
                return False
            elif choice == 'Так':
                return True

    def _launching(self):
        while True:
            bots_count = int(input('Привіт, скільки ботів створити?'))
            if bots_count <= self.max_pl_count - 1:
                break
        self.all_players_count = bots_count + 1

        for _ in range(bots_count):
            b = Player.Bot()
            self.players.append(b)
            print(b, ' створено ')

        self.player = Player.Player()
        self.player_pos = random.randint(0, self.all_players_count)
        print('Ваша позиція: ', self.player_pos)
        self.players.insert(self.player_pos, self.player)

    def ask_bet(self):
        for player in self.players:
            player.change_bet(self.max_bet, self.min_bet)

    def first_descr(self):
        for player in self.players:
            for _ in range(2):
                card = self.deck.get_card()
                player.take_card(card)

        card = self.deck.get_card()
        self.dealer.take_card(card)
        self.dealer.print_cards()

    def check_stop(self, player):
        if player.full_points >= 21:
            return True
        else:
            return False

    def remove_player(self, player):
        player.print_cards()
        if isinstance(player, Player.Player):
            print('Ти програв!')
        elif isinstance(player, Player.Bot):
            print(player, 'програв!')
        self.players.remove(player)

    def ask_cards(self):
        for player in self.players:

            while player.ask_card():
                card = self.deck.get_card()
                player.take_card(card)

                is_stop = self.check_stop(player)
                if is_stop:
                    if player.full_points > 21 or isinstance(player, Player.Player):
                        self.remove_player(player)
                    break

                if isinstance(player, Player.Player):
                    player.print_cards()

    def check_winner(self):
        if self.dealer.full_points > 21:
            # all win
            print('Дилер програв! Всі гравці виграють! ')
            for winner in self.players:
                winner.money += winner.bet * 2

        else:
            for player in self.players:
                if player.full_points == self.dealer.full_points:
                    player.money += player.bet
                    print(MESSAGES.get('eq').format(player=player,
                                                    points=player.full_points))
                elif player.full_points > self.dealer.full_points:
                    player.money += player.bet * 2
                    if isinstance(player, Player.Bot):
                        print(MESSAGES.get('win').format(player))
                    elif isinstance(player, Player.Player):
                        print('Ви виграли! ')

                elif player.full_points < self.dealer.full_points:
                    if isinstance(player, Player.Bot):
                        print(MESSAGES.get('lose').format(player))
                    elif isinstance(player, Player.Player):
                        print('Ви програли! ')

    def play_with_dealer(self):
        while self.dealer.ask_card():
            card = self.deck.get_card()
            self.dealer.take_card(card)
        self.dealer.print_cards()

    def start_game(self):
        message = MESSAGES.get('ask_start')
        # todo: max players count?
        if not self._ask_starting(message=message):
            exit(1)

        # generating data for starting
        self._launching()

        while True:
            # ask about bet
            self.ask_bet()
            time.sleep(2)

            # give first cards to the players
            self.first_descr()
            time.sleep(2)

            # print player cards after first deal
            self.player.print_cards()
            time.sleep(2)

            # ask players about cards
            self.ask_cards()
            time.sleep(2)

            self.play_with_dealer()
            time.sleep(2)

            self.check_winner()

            if not self._ask_starting(MESSAGES.get('rerun')):
                break

            # todo: change players pos
            # todo: check all players for money

Game.asd = 10