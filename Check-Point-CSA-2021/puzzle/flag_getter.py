import json
from pprint import pprint
#FLAG - CSA{InTh3OrYwEtRuST} with '_' between
import requests

import algorithm

flag = ''
r = requests.get('https://puzzword.csa-challenge.com/puzzle')
done =False
bot = algorithm.Bot()
while not done:
    puzzle_id = json.loads(json.loads(r.content)["message"])["puzzle_id"]
    src_board = json.loads(json.loads(r.content)["message"])["source_board"]
    dst_board = json.loads(json.loads(r.content)["message"])["destination_board"]
    # pprint(dst_board)
    src = [[c for c in line] for line in src_board]
    dst = [[c for c in line] for line in dst_board]
    moves = bot.solvePegSolitaire(src,dst)
    sol = {'puzzle_id' : puzzle_id, 'solution' : moves }
    r = requests.post('https://puzzword.csa-challenge.com/solve',json=sol)
    t = r.text
    flag+=json.loads(json.loads(r.content)['message'])['message'][0]
    print(flag)
    if "Thank you for solving all the puzzles! Bye" in r.text:
        print(r.__dict__)
        done = True

# puzzle_id = json.loads(json.loads(r.content)["message"])["puzzle_id"]
# r = requests.get('https://puzzword.csa-challenge.com/puzzle')

# print(r.__) #returns byte string
