
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test that the root endpoint returns a success message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Resty Chess API is running"}


def test_get_board():
    """Test getting the initial board state."""
    response = client.get("/v1/board")
    assert response.status_code == 200
    data = response.json()
    
    # Check that the board has 64 squares
    assert len(data["board"]) == 64
    
    # Verify some specific pieces are in their initial positions
    assert data["board"]["e1"]["piece_type"] == "king"
    assert data["board"]["e1"]["color"] == "white"
    assert data["board"]["d8"]["piece_type"] == "queen"
    assert data["board"]["d8"]["color"] == "black"


def test_move_piece():
    """Test moving a piece on the board."""
    # Move white pawn from e2 to e4
    response = client.post(
        "/v1/move",
        json={"from_square": "e2", "to_square": "e4"}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify the move happened
    assert data["from_square"] == "e2"
    assert data["to_square"] == "e4"
    assert data["moved_piece"]["piece_type"] == "pawn"
    assert data["moved_piece"]["color"] == "white"
    
    # Check that e2 is now empty and e4 has the pawn
    assert data["board"]["e2"] is None
    assert data["board"]["e4"]["piece_type"] == "pawn"
    assert data["board"]["e4"]["color"] == "white"


def test_remove_piece():
    """Test removing a piece from the board."""
    # First move a piece to a known position
    client.post("/v1/move", json={"from_square": "e2", "to_square": "e4"})
    
    # Then remove it
    response = client.post("/v1/remove", json={"square": "e4"})
    assert response.status_code == 200
    data = response.json()
    
    # Verify the removal happened
    assert data["removed_square"] == "e4"
    assert data["removed_piece"]["piece_type"] == "pawn"
    assert data["removed_piece"]["color"] == "white"
    
    # Check that e4 is now empty
    assert data["board"]["e4"] is None


def test_invalid_move():
    """Test attempting an invalid move."""
    # Try to move from an empty square
    response = client.post(
        "/v1/move",
        json={"from_square": "e3", "to_square": "e4"}
    )
    assert response.status_code == 400
    assert "No piece found" in response.json()["detail"]