import random

from flask import Flask, request, render_template, Response

app = Flask(__name__)

games = []
max_players = 2

@app.route("/", methods=['GET'])
def landing():
        return f"<h1 style='color:blue'>Hello there!</h1>"

# @app.route("/<test>", methods=['GET', 'POST'])
# def hello(test=None):
#     if request.method =='POST':
#         return f"<h1 style='color:blue'>Hello {test}!</h1>"
#     else:
#         return f"<h1 style='color:blue'>Hello there!</h1>"

@app.route("/<game>", methods=['GET', 'POST'])
def game_lobby(game):
    player_list = {}
    for i in games:
        print(i.id)
        print(game)
        if str(i.id) == str(game):
            player_num = 1
            for player in i.players:
                player_list[f"player{player_num}"] = player.name
                player_num += 1
    return player_list

@app.route("/generate", methods=['POST', 'GET'])
def make_game():
    name = request.form['player_name']
    joined = False
    if not games:
        games.append(Game(game_id()))
    for i in games:
        if len(i.players) < max_players:
            i.players.append(Player(name))
            print(f"{name} was added to game {i.id}")
            joined = True
    if not joined:
        id = game_id()
        while id is not None:
            if id not in games:
                current = Game(id)
                current.players.append(Player(name))
                games.append(current)
                print(f"Made a new game and {name} was added to game {current.id}")
                id = None

    return "Game was made."

@app.route("/list_games", methods=['GET'])
def list_games():
    string = ""
    for i in games:
        string = string + str(i.id) + " "
    return string

@app.route("/register", methods=['GET'])
def register():
    return render_template('register.html')


def game_id():
    number = random.randint(1, 1000)
    return number


class Player:

    def __init__(self, name):
        self.name = name
        self.team = ""


class Game:
    def __init__(self, id):
        self.id = id
        self.players = []
        self.teams = []
        pass

    def add_player(self, port_id):
        player = Player(port_id)
        self.players.append(player)

    def set_team(self, player, color):
        player.team = color
        if player.team not in self.teams:
            self.teams.append(player.team)


if __name__ == "__main__":
    app.run(host="localhost", port=8080)
