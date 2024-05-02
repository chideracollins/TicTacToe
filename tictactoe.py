import time
import random
import os


def middle_num(a, b, c):
    if a < b < c or c < b < a:
        return b, a, c
    if b < a < c or c < a < b:
        return a, b, c
    else:
        return c, a, b

class TicTacToe:
    def __init__(self, players) -> None:
        self.players:list = players
        self.state = {11 : "1", 12 : "2", 13 : "3", 21 : "4", 22 : "5", 23 : "6", 31 : "7", 32 : "8", 33 : "9"}
        self.plays = 0
        self.next_player = 0
        
    
    def play(self):
        curr_player:Player = self.players[self.next_player]
        curr_player.play(self.state, self)
        self.plays += 1
        if self.plays > 4 and self.check():
            if self.next_player == 0:
                self.players.reverse()
            return True
        self.next_player = self.plays % 2
        return False
    
    def award(self, winner=None):
        if winner == None:
            self.players[0].score += 1
            self.players[1].score += 1
            print("\n****************DRAW********************")
            print("This round ended in a tie!")
        else:
            winner.score += 3
            print("\n****************HURRAY********************")
            print(f"{winner.name}, won this round!")
        
    def check(self):
        for player in self.players:
            picks = player.picks.copy()
            if len(picks) < 3:
                continue
            elif len(picks) == 5:
                self.award()
                return True
            for a in picks:
                if picks[-2] == a:
                    break
                for b in picks[picks.index(a) + 1:]:
                    if picks[-1] == b:
                        break
                    for c in picks[picks.index(b) + 1:]:
                        mid_num, num_1, num_2 = middle_num(a, b, c)
                        if abs(mid_num - num_1) == abs(mid_num - num_2):
                            self.award(winner=player)
                            return True
        return False
        
    def board(self, state_values):
        for _ in range(13):
            print("-", end="")
        print(f"\n| {state_values[0]} | {state_values[1]} | {state_values[2]} |")
        print("|", end="")
        for _ in range(11):
            print("-", end="")
        print("|")
        print(f"| {state_values[3]} | {state_values[4]} | {state_values[5]} |")
        print("|", end="")
        for _ in range(11):
            print("-", end="")
        print("|")
        print(f"| {state_values[6]} | {state_values[7]} | {state_values[8]} |")
        for _ in range(13):
            print("-", end="")


class Player:
    def __init__(self, name:str, symbol:str, is_computer=False) -> None:
        self.name = name
        self.symbol = symbol
        self.is_computer = is_computer
        self.score = 0
        self.picks = []
        print(self)

    def play(self, state, game:TicTacToe):
        if self.is_computer:
            pick = self.computer(state.values())
            print(f"Computer just played, {pick}!")
            time.sleep(2)
        else:
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")
            print(f"\nYour turn, {self.name}\nNB: Your symbol - {self.symbol}\n")
            game.board(list(state.values()))
            pick = input("\n\nPlease only pick from the available options: ")
            if pick not in state.values() or pick.isalpha():
                print("Invalid option.\nTry again!")
                time.sleep(2)
                self.play(state, game)
        for key, value in state.items():
            if pick == value:
                self.picks.append(key)
                state[key] = self.symbol
        
    def computer(self, state_values):
        while True:
            pick = random.choice(list(state_values))
            if pick.isdigit():
                return pick
        
    def __str__(self) -> str:
        return f"Player, {self.name} has been activated with play symbol - {self.symbol}."
    
    
def game_play(game:TicTacToe):
    while True:
        if game.play():
            break
    return game.players
    
def game_setup():
    print("Welcome to this tictactoe game.")
    name = input("Enter your name: ")
    while True:
        symbol = input("Choose between 'X or O' as the symbol for your plays: ")
        if symbol.upper() in ("X", "O"):
            break
        print("Incorrect symbol!")
    player_1 = Player(name, symbol)
    opp_name = input("Let your opponent, enter their name or hit enter to continue play with a computer as your opponent:")
    sec_symbol = "X" if symbol == "O" else "O"
    
    if len(opp_name) < 1:
        player_2 = Player("Computer", sec_symbol, is_computer=True)
    else:
        player_2 = Player(opp_name, sec_symbol)
        
    players = [player_1, player_2]
    first_player = players.pop(random.randint(0, 1))
    second_player = players.pop(0)
    status = True
    while status:
        game = TicTacToe([first_player, second_player])
        first_player, second_player = game_play(game)
        first_player.picks.clear()
        second_player.picks.clear()
        print(f"The score of the game so far is: {first_player.name}- {first_player.score} : {second_player.score} -{second_player.name}")
        if input("\nDo you want to keep playing? (enter 'N' to quit or hit 'enter' to continue playing)").upper() == "N":
            status = False
        
    print("Thank you for playing!")
    
if __name__ == "__main__":
    game_setup()
