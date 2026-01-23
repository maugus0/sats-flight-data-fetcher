"""
Pytest configuration and fixtures
"""

import pytest


@pytest.fixture
def mock_api_key():
    """Provide a mock API key for testing"""
    return "test_api_key_1234567890abcdef"


@pytest.fixture
def mock_airline_config():
    """Provide mock airline configuration (matches actual structure)"""
    return {
        "airlines": {
            "SQ": {
                "name": "Singapore Airlines",
                "iata": "SQ",
                "icao": "SIA",
                "country": "Singapore",
            },
            "EK": {"name": "Emirates", "iata": "EK", "icao": "UAE", "country": "UAE"},
            "QR": {
                "name": "Qatar Airways",
                "iata": "QR",
                "icao": "QTR",
                "country": "Qatar",
            },
        }
    }


@pytest.fixture
def mock_api_response():
    """Provide mock AirLabs API response"""
    return {
        "response": [
            {
                "flight_iata": "SQ317",
                "flight_icao": "SIA317",
                "dep_iata": "SIN",
                "arr_iata": "LHR",
                "dep_time": "2025-01-01T23:30:00",
                "arr_time": "2025-01-02T06:15:00",
                "dep_actual": "2025-01-01T23:42:00",
                "arr_actual": "2025-01-02T06:25:00",
                "delayed": 12,
                "status": "landed",
            },
            {
                "flight_iata": "SQ322",
                "flight_icao": "SIA322",
                "dep_iata": "LHR",
                "arr_iata": "SIN",
                "dep_time": "2025-01-01T13:10:00",
                "arr_time": "2025-01-02T08:45:00",
                "dep_actual": "2025-01-01T13:05:00",
                "arr_actual": "2025-01-02T08:40:00",
                "delayed": 0,
                "status": "landed",
            },
            {
                "flight_iata": "SQ001",
                "flight_icao": "SIA001",
                "dep_iata": "SIN",
                "arr_iata": "HKG",
                "dep_time": "2025-01-01T08:00:00",
                "arr_time": "2025-01-01T12:00:00",
                "dep_actual": None,
                "arr_actual": None,
                "delayed": 30,
                "status": "delayed",
            },
        ]
    }


@pytest.fixture
def sample_date():
    """Provide a sample date for testing"""
    return "2025-01-01"


@pytest.fixture
def sample_date_range():
    """Provide a sample date range for testing"""
    return {"start": "2025-01-01", "end": "2025-01-07"}


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create temporary output directory for tests"""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    return str(output_dir)


@pytest.fixture
def mock_env_vars(monkeypatch, mock_api_key):
    """Set mock environment variables"""
    monkeypatch.setenv("AIRLABS_API_KEY", mock_api_key)
