# This file implements three main API endpoints:

# 1. `GET /v1/board` - Returns the current board state
# 2. `POST /v1/move` - Moves a piece from one square to another
# 3. `POST /v1/remove` - Removes a piece from a specified square

# The API automatically validates request data using Pydantic models and returns appropriate HTTP status codes for errors. FastAPI will also generate OpenAPI documentation (Swagger UI) accessible at `/docs` when the application is running.




import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.models import (
    MoveRequest,
    RemovePieceRequest,
    BoardStateResponse,
    MoveResponse,
    RemoveResponse,
    PieceInfo
)
from app.service import get_chess_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Resty Chess API",
    description="A RESTful API to manage a chess board",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint to verify API is running."""
    return {"message": "Resty Chess API is running"}


@app.get("/v1/board", response_model=BoardStateResponse, tags=["Chess"])
async def get_board():
    """
    Get the current state of the chess board.
    
    Returns:
        Current board state with all pieces and their positions
    """
    logger.info("Getting board state")
    chess_service = get_chess_service()
    return chess_service.get_board_state()


@app.post("/v1/move", response_model=MoveResponse, tags=["Chess"])
async def move_piece(move_request: MoveRequest):
    """
    Move a chess piece from one square to another.
    
    Args:
        move_request: Contains source and target squares in algebraic notation
        
    Returns:
        Updated board state after the move
        
    Raises:
        HTTPException: If the move is invalid
    """
    logger.info(f"Move request: {move_request.from_square} to {move_request.to_square}")
    chess_service = get_chess_service()
    
    try:
        board_state, moved_piece, captured_piece = chess_service.move_piece(
            move_request.from_square, 
            move_request.to_square
        )
        
        return MoveResponse(
            board=board_state["board"],
            from_square=move_request.from_square,
            to_square=move_request.to_square,
            moved_piece=moved_piece,
            captured_piece=captured_piece,
            fen=board_state["fen"],
            turn=board_state["turn"]
        )
        
    except ValueError as e:
        logger.error(f"Move error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/v1/remove", response_model=RemoveResponse, tags=["Chess"])
async def remove_piece(remove_request: RemovePieceRequest):
    """
    Remove a chess piece from the specified square.
    
    Args:
        remove_request: Contains the square to remove the piece from
        
    Returns:
        Updated board state after the removal
        
    Raises:
        HTTPException: If the removal is invalid (e.g., empty square)
    """
    logger.info(f"Remove piece request at square: {remove_request.square}")
    chess_service = get_chess_service()
    
    try:
        board_state, removed_piece = chess_service.remove_piece(remove_request.square)
        
        return RemoveResponse(
            board=board_state["board"],
            removed_square=remove_request.square,
            removed_piece=removed_piece,
            fen=board_state["fen"],
            turn=board_state["turn"]
        )
        
    except ValueError as e:
        logger.error(f"Remove error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


if __name__ == "__main__":
    # This block is executed when running the file directly
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)