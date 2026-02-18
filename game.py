import json
import os
SCORE_FILE = "score.json"
def load_score():
    if os.path.exists(SCORE_FILE):
        with open (SCORE_FILE, "r") as file:
            return json.load(file)
    return {"x": 0, "o": 0, "draw": 0}
def save_score(score): 
        with open(SCORE_FILE, "w") as file:
            json.dump(score, file)
score = load_score()

spielfeld = [[' ' for _ in range(3)] for _ in range(3)]
aktueller_spieler = 'x'


def reset_game():
    global spielfeld, aktueller_spieler
    spielfeld = [[' ' for _ in range(3)] for _ in range(3)]
    aktueller_spieler = 'x'


def make_move(row, col, mode="pvp"):
    global aktueller_spieler

    if spielfeld[row][col] != ' ':
        return {"status": "error"}


    symbol = aktueller_spieler
    spielfeld[row][col] = symbol


    winner, line = pruefe_gewinner()

    if winner:
        score[winner] +=1
        save_score(score)
        return {
            "status": "win",
            "winner": winner,
            "line": line,
            "symbol": symbol,
            "score": score
        }


    if pruefe_unentschieden():
        score["draw"] +=1
        save_score(score)
        return {
            "status": "draw",
            "symbol": symbol,
            "score": score
        }


    aktueller_spieler = "o" if aktueller_spieler == "x" else "x"

    if aktueller_spieler == "o" and mode== "ai":
         row, col = computer_move()
         computer_symbol = aktueller_spieler
         spielfeld[row][col] = computer_symbol
         winner, line = pruefe_gewinner()
         if winner:
             score[winner] +=1
             save_score(score)
             return{
                 "status": "win",
                 "winner": winner,
                 "line": line,
                 "symbol": computer_symbol,
                 "score": score,
                 "computer":True,
                 "row": row,
                 "col": col
             }
         if pruefe_unentschieden():
             score["draw"] +=1
             save_score(score)
             return{
                 "status": "draw",
                 "symbol": computer_symbol,
                 "computer":True,
                 "row": row,
                 "col": col,
                 "score": score
             }
         aktueller_spieler = "x"
         return{
             "status": "continue",
             "player": aktueller_spieler,
             "symbol": computer_symbol,
             "computer": True,
             "row": row,
             "col": col,
             "score": score
         }
    return {
        "status": "continue",
        "player": aktueller_spieler,
        "symbol": symbol,
        "score": score
    }
def pruefe_gewinner():
    for i in range(3):
        if spielfeld[i][0] == spielfeld[i][1] == spielfeld[i][2] != ' ':
            return spielfeld[i][0], [(i,0),(i,1),(i,2)]

    for j in range(3):
        if spielfeld[0][j] == spielfeld[1][j] == spielfeld[2][j] != ' ':
            return spielfeld[0][j], [(0,j),(1,j),(2,j)]

    if spielfeld[0][0] == spielfeld[1][1] == spielfeld[2][2] != ' ':
        return spielfeld[0][0], [(0,0),(1,1),(2,2)]

    if spielfeld[0][2] == spielfeld[1][1] == spielfeld[2][0] != ' ':
        return spielfeld[0][2], [(0,2),(1,1),(2,0)]

    return None, None


def pruefe_unentschieden():
    return all(cell != ' ' for row in spielfeld for cell in row)
 
import random
def computer_move():
    for r in range(3):
        for c in range(3):
            if spielfeld[r][c] == ' ':
                spielfeld[r][c] = "o"
                winner, _ = pruefe_gewinner()
                spielfeld[r][c] = ' '
                if winner == 'o':
                    return (r, c)
    for r in range(3):
        for c in range(3):
            if spielfeld[r][c] == ' ':
                spielfeld[r][c] = 'x'
                winner, _ = pruefe_gewinner()
                spielfeld[r][c] = ' '
                if winner == 'x':
                    return(r, c)
    empty = []
    for r in range(3):
        for c in range(3):
            if spielfeld[r][c] == ' ':
                empty.append((r, c))
    if empty:
        return random.choice(empty)
    return None