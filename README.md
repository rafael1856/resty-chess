```markdown
# Resty Chess API

A RESTful API for managing a chess board using FastAPI.

## Features

- Initialize a standard chess board setup
- Get the current state of the board
- Move pieces on the board
- Remove pieces from the board
- In-memory state management



```

## Folder and Files:

```
    chess-api/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py         # FastAPI application entry point
    │   ├── models.py       # Pydantic models for request/response validation
    │   ├── service.py      # Chess game logic and board management
    │   └── utils.py        # Utility functions
    ├── tests/
    │   └── test_api.py     # API tests
    ├── .dockerignore
    ├── Dockerfile          # Docker configuration
    ├── requirements.txt    # Application libraries required
    └── README.md           # This file
```


## Running with Docker

1. Build the Docker image:

```shellscript

    docker build -t resty-chess-api  .

```

2. Run the Docker container:

```shellscript
docker run -p 8000:8000 resty-chess-api
```

The API will be available at http://localhost:8000. 


You should see a message like:

- "message":"Resty Chess API is running"
    

OpenAPI documentation can be accessed at  http://localhost:8000/docs.



## API Endpoints

### GET /v1/board

Get the current state of the chess board.

```shellscript
curl http://localhost:8000/v1/board
```

### POST /v1/move

Move a piece from one square to another.

```shellscript
curl -X POST http://localhost:8000/v1/move \
  -H "Content-Type: application/json" \
  -d '{"from_square": "e2", "to_square": "e4"}'
```

```shellscript
curl -X POST http://localhost:8000/v1/move \
  -H "Content-Type: application/json" \
  -d '{"from_square": "d7", "to_square": "d5"}'
```

### POST /v1/remove

Remove a piece from a specified square.

```shellscript
curl -X POST http://localhost:8000/v1/remove \
  -H "Content-Type: application/json" \
  -d '{"square": "e4"}'
```

## Example: Simulating "Taking a Piece"

To simulate taking a piece (for example, a white pawn at d5 capturing a black pawn at e4):

Move the white pawn from d5 to e4

```shellscript

curl -X POST http://localhost:8000/v1/move \
  -H "Content-Type: application/json" \
  -d '{"from_square": "d5", "to_square": "e4"}'


```

Response will include both the moved piece and the captured piece

The move operation automatically handles captures - when you move a piece to a square occupied by another piece, the API records the capture in the response.

## Run the application locally

1. Create a virtual environment and install dependencies:

```shellscript
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

```

2. Run the FastAPI application:

```shellscript
uvicorn app.main:app --reload

```

# Visualization tool

To visualize the current board status in a Linux terminal, run the tool print_json_board.py:

1. Get current board json file

```shellscript
curl http://localhost:8000/v1/board > tools/current-board.json
```

2. Print the current board

```shellscript
python3 tools/print_json_board.py current-board.json 

```

```

    8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
    7 ♟ ♟ ♟ . ♟ ♟ ♟ ♟
    6 . . . . . . . .
    5 . . . ♟ . . . .
    4 . . . . ♙ . . .
    3 . . . . . . . .
    2 ♙ ♙ ♙ ♙ . ♙ ♙ ♙
    1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
    a b c d e f g h

```