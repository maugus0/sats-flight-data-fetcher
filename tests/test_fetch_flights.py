"""
Unit tests for fetch_flights.py
"""

import json
import os
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest
import requests

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestFetchFlightsForDate:
    """Tests for fetch_flights_for_date function"""

    def test_fetch_success(self, mock_api_key, mock_api_response, sample_date):
        """Test successful flight data fetch"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_api_response
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            from fetch_flights import fetch_flights_for_date

            result = fetch_flights_for_date(mock_api_key, "SQ", sample_date)

            assert result is not None
            assert "response" in result
            assert len(result["response"]) == 3

    def test_fetch_timeout(self, mock_api_key, sample_date):
        """Test handling of request timeout"""
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout("Connection timeout")

            from fetch_flights import fetch_flights_for_date

            result = fetch_flights_for_date(mock_api_key, "SQ", sample_date)
            assert result is None

    def test_fetch_http_error(self, mock_api_key, sample_date):
        """Test handling of HTTP errors"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Server error")
            mock_get.return_value = mock_response

            from fetch_flights import fetch_flights_for_date

            result = fetch_flights_for_date(mock_api_key, "SQ", sample_date)
            assert result is None

    def test_fetch_api_error_response(self, mock_api_key, sample_date):
        """Test handling of API error in response"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"error": {"message": "Invalid API key"}}
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            from fetch_flights import fetch_flights_for_date

            result = fetch_flights_for_date(mock_api_key, "SQ", sample_date)
            assert result is None


class TestExtractFlightData:
    """Tests for extract_flight_data function"""

    def test_extract_success(self, mock_api_response):
        """Test flight data extraction and normalization"""
        from fetch_flights import extract_flight_data

        flights = extract_flight_data(mock_api_response)

        assert len(flights) == 3
        assert flights[0]["flight_number"] == "SQ317"
        assert flights[0]["departure_airport"] == "SIN"
        assert flights[0]["arrival_airport"] == "LHR"
        assert flights[0]["delay_minutes"] == 12
        assert flights[0]["flight_status"] == "landed"

    def test_extract_empty_response(self):
        """Test extraction with empty response"""
        from fetch_flights import extract_flight_data

        flights = extract_flight_data({"response": []})
        assert flights == []

    def test_extract_missing_fields(self):
        """Test extraction handles missing fields gracefully"""
        from fetch_flights import extract_flight_data

        data = {
            "response": [
                {
                    "flight_iata": "SQ999",
                    # Missing most fields
                }
            ]
        }

        flights = extract_flight_data(data)

        assert len(flights) == 1
        assert flights[0]["flight_number"] == "SQ999"
        assert flights[0]["departure_airport"] == ""
        assert flights[0]["delay_minutes"] == 0
        assert flights[0]["flight_status"] == "unknown"


class TestGenerateSummary:
    """Tests for generate_summary function"""

    def test_summary_with_flights(self, mock_api_response):
        """Test summary generation with flight data"""
        from fetch_flights import extract_flight_data, generate_summary

        flights = extract_flight_data(mock_api_response)
        summary = generate_summary(flights)

        assert summary["total_flights"] == 3
        assert "average_delay_minutes" in summary
        assert "on_time_percentage" in summary
        assert "flights_by_status" in summary
        assert "top_routes" in summary

    def test_summary_empty_flights(self):
        """Test summary with no flights"""
        from fetch_flights import generate_summary

        summary = generate_summary([])

        assert summary["total_flights"] == 0


class TestExportFunctions:
    """Tests for export functions"""

    def test_export_to_csv(self, mock_api_response, temp_output_dir):
        """Test CSV export functionality"""
        import csv

        from fetch_flights import export_to_csv, extract_flight_data

        flights = extract_flight_data(mock_api_response)
        csv_file = os.path.join(temp_output_dir, "test_flights.csv")

        export_to_csv(flights, csv_file)

        assert os.path.exists(csv_file)

        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 3
            assert rows[0]["flight_number"] == "SQ317"

    def test_export_to_json(self, mock_api_response, temp_output_dir):
        """Test JSON export functionality"""
        from fetch_flights import export_to_json, extract_flight_data, generate_summary

        flights = extract_flight_data(mock_api_response)
        summary = generate_summary(flights)
        json_file = os.path.join(temp_output_dir, "test_flights.json")

        export_to_json(flights, summary, json_file)

        assert os.path.exists(json_file)

        with open(json_file, "r") as f:
            data = json.load(f)
            assert "flights" in data
            assert "summary" in data
            assert len(data["flights"]) == 3

    def test_export_to_excel(self, mock_api_response, temp_output_dir):
        """Test Excel export functionality"""
        from fetch_flights import export_to_excel, extract_flight_data, generate_summary

        flights = extract_flight_data(mock_api_response)
        summary = generate_summary(flights)
        excel_file = os.path.join(temp_output_dir, "test_flights.xlsx")

        export_to_excel(flights, summary, "Singapore Airlines", excel_file)

        assert os.path.exists(excel_file)


class TestValidation:
    """Tests for validation functions"""

    def test_validate_date_valid(self):
        """Test date validation with valid dates"""
        from fetch_flights import validate_date

        assert validate_date("2025-01-01") is True
        assert validate_date("2025-12-31") is True
        assert validate_date("2024-02-29") is True  # Leap year

    def test_validate_date_invalid(self):
        """Test date validation with invalid dates"""
        from fetch_flights import validate_date

        assert validate_date("2025-13-01") is False
        assert validate_date("01-01-2025") is False
        assert validate_date("2025/01/01") is False
        assert validate_date("invalid") is False
        assert validate_date("") is False

    def test_validate_api_key_valid(self):
        """Test API key validation with valid keys"""
        from fetch_flights import validate_api_key

        assert validate_api_key("a" * 25) is True
        assert validate_api_key("abc123def456ghi789jkl012") is True

    def test_validate_api_key_invalid(self):
        """Test API key validation with invalid keys"""
        from fetch_flights import validate_api_key

        assert validate_api_key("") is False
        assert validate_api_key("short") is False
        assert validate_api_key(None) is False


class TestAirlineConfig:
    """Tests for airline configuration functions"""

    def test_get_airline_info_by_iata(self, mock_airline_config):
        """Test getting airline info by IATA code"""
        from fetch_flights import get_airline_info

        info = get_airline_info("SQ", mock_airline_config)

        assert info is not None
        assert info["name"] == "Singapore Airlines"

    def test_get_airline_info_by_icao(self, mock_airline_config):
        """Test getting airline info by ICAO code"""
        from fetch_flights import get_airline_info

        info = get_airline_info("SIA", mock_airline_config)

        assert info is not None
        assert info["name"] == "Singapore Airlines"

    def test_get_airline_info_not_found(self, mock_airline_config):
        """Test getting info for unknown airline"""
        from fetch_flights import get_airline_info

        info = get_airline_info("XX", mock_airline_config)

        assert info is None

    def test_get_airline_info_case_insensitive(self, mock_airline_config):
        """Test airline lookup is case insensitive"""
        from fetch_flights import get_airline_info

        info_lower = get_airline_info("sq", mock_airline_config)
        info_upper = get_airline_info("SQ", mock_airline_config)

        assert info_lower is not None
        assert info_upper is not None
        assert info_lower["name"] == info_upper["name"]

