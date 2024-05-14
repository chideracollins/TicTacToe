# the python code the html template
from django.shortcuts import render

import json

def tictactoe(request):
    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    context = {
        'board': board,
        'board_json': json.dumps(board),
        'current_player': current_player
    }
    return render(request, 'engine/base.html', context)
