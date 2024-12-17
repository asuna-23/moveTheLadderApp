// s_reference_cycle.py

@reference_cycle_router.route("/api/get-ref-cycle-time", methods=["GET"])
def get_ref_cycle_time():
    """Fetch only reference_cycle_time using the schema's 'only' parameter"""

    query = ReferenceCycleDb.query.all()

    # Serialize only the 'reference_cycle_time' field
    reference_cycle_data = reference_cycle_schema(many=True, only=["reference_cycle_time"]).dump(query)

    return {
        "success": True,
        "message_response": "REFERENCE CYCLE TIME FETCHED SUCCESSFULLY",
        "message_content": "Reference cycle times fetched successfully",
        "data": reference_cycle_data,
    }, 200


### pytest

import pytest
from unittest.mock import patch, MagicMock
from src.setup_db_example.app import create_app  # Import your Flask app factory
from src.setup_db_example.models.m_reference_cycle import ReferenceCycleDb

@pytest.fixture
def client():
    """Fixture to set up the Flask test client."""
    app = create_app()  # Replace with your Flask app initialization
    app.testing = True  # Enable test mode
    with app.test_client() as client:
        yield client

@patch("src.setup_db_example.models.m_reference_cycle.ReferenceCycleDb.query")
def test_get_ref_cycle_time(client, mock_query):
    """Test for /api/get-ref-cycle-time endpoint"""

    # Mock database data
    mock_data = [
        MagicMock(reference_cycle_time=100),
        MagicMock(reference_cycle_time=200),
        MagicMock(reference_cycle_time=300),
    ]

    # Set the return value of the query
    mock_query.all.return_value = mock_data

    # Perform the GET request
    response = client.get("/api/get-ref-cycle-time")

    # Parse the response JSON
    response_json = response.get_json()

    # Assertions
    assert response.status_code == 200
    assert response_json["success"] is True
    assert response_json["message_response"] == "REFERENCE CYCLE TIME FETCHED SUCCESSFULLY"
    assert response_json["message_content"] == "Reference cycle times fetched successfully"
    assert response_json["data"] == [100, 200, 300]



/////////