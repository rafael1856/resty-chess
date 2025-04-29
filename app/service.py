import chess
import logging
from functools import lru_cache
from typing import Dict, Optional, Tuple

from app.models import PieceInfo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Piece type mapping: python-chess piece symbols to human-readable names
PIECE_TYPE_NAMES = {
    chess.PAWN: "pawn",
    chess.KNIGHT: "knight",
    chess.BISHOP: "bishop",
    chess.ROOK: "rook", 
    chess.QUEEN: "queen",
    chess.KING: "king"
}

# Color mapping: python-chess colors to human-readable names
COLOR_NAMES = {
    chess.WHITE: "white",
    chess.BLACK: "black"
}


class ChessBoardService:
    """Service to manage chess board state."""
    
    def __init__(self):
        """Initialize a new chess board with standard setup."""
        self._board = chess.Board()
        logger.info("Chess board initialized with standard setup")

    def get_board_state(self) -> Dict:
        """
        Get the current state of the chess board.
        
        Returns:
            Dict containing the board state with pieces and their positions
        """
        board_state = {}
        
        # Iterate through all squares on the board
        for square in chess.SQUARES:
            square_name = chess.square_name(square)
            piece = self._board.piece_at(square)
            
            if piece:
                board_state[square_name] = PieceInfo(
                    piece_type=PIECE_TYPE_NAMES[piece.piece_type],
                    color=COLOR_NAMES[piece.color]
                )
            else:
                board_state[square_name] = None
        
        return {
            "board": board_state,
            "fen": self._board.fen(),
            "turn": COLOR_NAMES[self._board.turn]
        }

    def move_piece(self, from_square: str, to_square: str) -> Tuple[Dict, Optional[PieceInfo]]:
        """
        Move a piece from one square to another.
        
        Args:
            from_square: Source square in algebraic notation (e.g. 'e2')
            to_square: Target square in algebraic notation (e.g. 'e4')
            
        Returns:
            Tuple containing board state and captured piece info (if any)
            
        Raises:
            ValueError: If move is invalid or out of board boundaries
        """
        try:
            # Convert algebraic notation to square indexes
            from_sq = chess.parse_square(from_square)
            to_sq = chess.parse_square(to_square)
            
            # Check if source square has a piece
            piece = self._board.piece_at(from_sq)
            if not piece:
                raise ValueError(f"No piece found at {from_square}")
            
            # Store piece information before move
            moved_piece = PieceInfo(
                piece_type=PIECE_TYPE_NAMES[piece.piece_type],
                color=COLOR_NAMES[piece.color]
            )
            
            # Check if there's a piece at the target square (capture)
            captured_piece = None
            target_piece = self._board.piece_at(to_sq)
            if target_piece:
                captured_piece = PieceInfo(
                    piece_type=PIECE_TYPE_NAMES[target_piece.piece_type],
                    color=COLOR_NAMES[target_piece.color]
                )
            
            # Create and execute move
            move = chess.Move(from_sq, to_sq)
            
            # We're not validating chess rules, just ensuring move is within board
            if move not in self._board.pseudo_legal_moves:
                # Check if the move is only invalid because of chess rules
                if from_sq > 63 or to_sq > 63:
                    raise ValueError("Move is outside the board boundaries")
                
            # Make the move (only checking board boundaries, not chess rules)
            self._board.set_piece_at(to_sq, piece)
            self._board.remove_piece_at(from_sq)
            
            # Toggle turn (white to black or black to white)
            self._board.turn = not self._board.turn
            
            logger.info(f"Moved {moved_piece.color} {moved_piece.piece_type} from {from_square} to {to_square}")
            if captured_piece:
                logger.info(f"Captured {captured_piece.color} {captured_piece.piece_type} at {to_square}")
                
            return self.get_board_state(), moved_piece, captured_piece
            
        except ValueError as e:
            logger.error(f"Invalid move: {str(e)}")
            raise
    
    def remove_piece(self, square: str) -> Tuple[Dict, Optional[PieceInfo]]:
        """
        Remove a piece from the specified square.
        
        Args:
            square: Square in algebraic notation (e.g. 'e4')
            
        Returns:
            Tuple containing board state and removed piece info (if any)
            
        Raises:
            ValueError: If square is invalid or empty
        """
        try:
            sq = chess.parse_square(square)
            
            # Check if there's a piece at the square
            piece = self._board.piece_at(sq)
            if not piece:
                raise ValueError(f"No piece found at {square}")
            
            # Store piece information before removal
            removed_piece = PieceInfo(
                piece_type=PIECE_TYPE_NAMES[piece.piece_type],
                color=COLOR_NAMES[piece.color]
            )
            
            # Remove the piece
            self._board.remove_piece_at(sq)
            
            logger.info(f"Removed {removed_piece.color} {removed_piece.piece_type} from {square}")
            return self.get_board_state(), removed_piece
            
        except ValueError as e:
            logger.error(f"Invalid remove operation: {str(e)}")
            raise


@lru_cache(maxsize=1)
def get_chess_service() -> ChessBoardService:
    """
    Get the chess service singleton instance.
    
    Returns:
        ChessBoardService instance
    """
    return ChessBoardService()