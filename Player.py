import abc
import random

from Deck import Deck
from Const import MESSAGES,NAMES


class AbstractPlayer(abc.ABC):

    def __init__(self):
        self.cards = []
        self.bet = 0
        self.full_points = 0
        self.money = 100

    def change_points(self):
        self.full_points = sum([card.points for card in self.cards])

    def take_card(self, card):
        self.cards.append(card)
        self.change_points()

    @abc.abstractmethod
    def change_bet(self,  max_bet, min_bet):
        pass

    @abc.abstractmethod
    def ask_card(self):
        pass

    def print_cards(self):
        print(self)
        for card in self.cards:
            print(card)
        print('Кількість очків: ', self.full_points)


class Player(AbstractPlayer):

    def __str__(self):
        return f"Гравець"

    def change_bet(self, max_bet, min_bet):
        while True:
            value = int(input('Зробіть ставку: '))
            if value < max_bet and value > min_bet:
                self.bet = value
                self.money -= self.bet
                break
        print('Ваша ставка така : ', self.bet)

    def ask_card(self):
        choice = input(MESSAGES.get('ask_card'))
        if choice == 'Так':
            return True
        else:
            return False


class Bot(AbstractPlayer):

    def __init__(self):
        super().__init__()
        self.max_points = random.randint(2, 21)

    def bot_name(self):
        self.lst_name =[]
        name = f"{random.choice(NAMES)}"
        while len(self.lst_name) <= 3:
            if name in lst_name:
                name = f"{random.choice(NAMES)}"
            else:
                self.lst_name.append(name)
        return self.lst_name


    def __str__(self):
        return f"Bot - {str(id(self))[-1]}"

    def change_bet(self, max_bet, min_bet):
        self.bet = random.randint(min_bet, max_bet)
        self.money -= self.bet
        print(self, 'поставив: ', self.bet)

    def ask_card(self):
        if self.full_points < self.max_points:
            return True
        else:
            return False


class Dealer(AbstractPlayer):

    max_points = 21

    def __str__(self):
        return f"Дилєр"

    def change_bet(self, max_bet, min_bet):
        """
        NOTE: This type is Dealer so it has no bets
        """""
        raise Exception('Цей гравець є дилером, тому у нього немає ставок')

    def ask_card(self):
        if self.full_points < self.max_points:
            return True
        else:
            return False