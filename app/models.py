from pydantic import BaseModel, Field
from typing import Dict, Optional, List


class MoveRequest(BaseModel):
    """Model for move piece request."""
    from_square: str = Field(..., pattern="^[a-h][1-8]$", description="Source square in algebraic notation (e.g. 'e2')")
    to_square: str = Field(..., pattern="^[a-h][1-8]$", description="Target square in algebraic notation (e.g. 'e4')")


class RemovePieceRequest(BaseModel):
    """Model for remove piece request."""
    square: str = Field(..., pattern="^[a-h][1-8]$", description="Square containing the piece to remove")


class PieceInfo(BaseModel):
    """Model for piece information."""
    piece_type: str  # pawn, knight, bishop, rook, queen, king
    color: str       # white or black


class BoardStateResponse(BaseModel):
    """Response model for board state."""
    board: Dict[str, Optional[PieceInfo]]  # Key is square, value is piece
    fen: str  # Forsyth-Edwards Notation representation
    turn: str  # Current player's turn (white or black)


class MoveResponse(BaseModel):
    """Response model after a move operation."""
    board: Dict[str, Optional[PieceInfo]]
    from_square: str
    to_square: str
    moved_piece: PieceInfo
    captured_piece: Optional[PieceInfo] = None
    fen: str
    turn: str


class RemoveResponse(BaseModel):
    """Response model after a remove operation."""
    board: Dict[str, Optional[PieceInfo]]
    removed_square: str
    removed_piece: Optional[PieceInfo]
    fen: str
    turn: str


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str