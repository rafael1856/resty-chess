import sys
import json

if len(sys.argv) < 2:
    print("Usage: python show_board.py <board.json>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    data = json.load(f)

symbols = {
    ('pawn', 'white'): '♙', ('knight', 'white'): '♘', ('bishop', 'white'): '♗',
    ('rook', 'white'): '♖', ('queen', 'white'): '♕', ('king', 'white'): '♔',
    ('pawn', 'black'): '♟', ('knight', 'black'): '♞', ('bishop', 'black'): '♝',
    ('rook', 'black'): '♜', ('queen', 'black'): '♛', ('king', 'black'): '♚',
    None: '.'
}

board = data['board']
ranks = '87654321'
files = 'abcdefgh'

for rank in ranks:
    row = []
    for file in files:
        sq = file + rank
        piece = board[sq]
        if piece:
            row.append(symbols[(piece['piece_type'], piece['color'])])
        else:
            row.append('.')
    print(rank, ' '.join(row))
print('  a b c d e f g h')
print(f"Turn: {data['turn']}")
print(f"FEN: {data['fen']}")