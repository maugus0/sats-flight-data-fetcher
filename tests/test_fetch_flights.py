"""
Unit tests for fetch_flights.py
"""

import json
import os
import sys
from unittest.mock import Mock, patch

import pytest
import requests

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestFetchFlightsForDate:
    """Tests for fetch_flights_for_date function (with pagination)"""

    def test_fetch_success_single_page(
        self, mock_api_key, mock_api_response, sample_date
    ):
        """Test successful flight data fetch (single page, < 100 results)"""
        with patch("fetch_flights.fetch_single_page") as mock_fetch:
            mock_fetch.return_value = mock_api_response

            from fetch_flights import fetch_flights_for_date

            result = fetch_flights_for_date(mock_api_key, "SQ", sample_date)

            assert result is not None
            assert "response" in result
            assert len(result["response"]) == 3
            assert result.get("pages_fetched") == 1

    def test_fetch_success_multiple_pages(self, mock_api_key, sample_date):
        """Test pagination - fetches multiple pages when 100+ results"""
        page1 = {"response": [{"flight_iata": f"SQ{i}"} for i in range(100)]}
        page2 = {"response": [{"flight_iata": f"SQ{i}"} for i in range(100, 150)]}

        with patch("fetch_flights.fetch_single_page") as mock_fetch:
            mock_fetch.side_effect = [page1, page2]

            from fetch_flights import fetch_flights_for_date

            with patch("time.sleep"):  # Skip pagination delay
                result = fetch_flights_for_date(mock_api_key, "SQ", sample_date)

            assert result is not None
            assert len(result["response"]) == 150  # 100 + 50
            assert result.get("pages_fetched") == 2
            assert mock_fetch.call_count == 2

    def test_fetch_timeout(self, mock_api_key, sample_date):
        """Test handling of request timeout"""
        with patch("fetch_flights.fetch_single_page") as mock_fetch:
            mock_fetch.return_value = None

            from fetch_flights import fetch_flights_for_date

            result = fetch_flights_for_date(mock_api_key, "SQ", sample_date)
            assert result is None

    def test_fetch_empty_response(self, mock_api_key, sample_date):
        """Test handling of empty response"""
        with patch("fetch_flights.fetch_single_page") as mock_fetch:
            mock_fetch.return_value = {"response": []}

            from fetch_flights import fetch_flights_for_date

            result = fetch_flights_for_date(mock_api_key, "SQ", sample_date)

            assert result is not None
            assert result["response"] == []


class TestFetchSinglePage:
    """Tests for fetch_single_page function (low-level API call)"""

    def test_fetch_single_page_success(
        self, mock_api_key, mock_api_response, sample_date
    ):
        """Test successful single page fetch"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_api_response
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            from fetch_flights import fetch_single_page

            result = fetch_single_page(mock_api_key, "SQ", sample_date, offset=0)

            assert result is not None
            assert "response" in result

    def test_fetch_single_page_with_offset(
        self, mock_api_key, mock_api_response, sample_date
    ):
        """Test fetch with offset parameter"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_api_response
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            from fetch_flights import fetch_single_page

            fetch_single_page(mock_api_key, "SQ", sample_date, offset=100)

            # Verify offset was passed to API
            call_args = mock_get.call_args
            assert call_args[1]["params"]["offset"] == 100
            assert call_args[1]["params"]["limit"] == 100

    def test_fetch_single_page_timeout(self, mock_api_key, sample_date):
        """Test handling of request timeout"""
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout("Connection timeout")

            from fetch_flights import fetch_single_page

            with patch("time.sleep"):  # Skip retry delays
                result = fetch_single_page(mock_api_key, "SQ", sample_date)

            assert result is None

    def test_fetch_single_page_http_error(self, mock_api_key, sample_date):
        """Test handling of HTTP errors"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
                "Server error"
            )
            mock_get.return_value = mock_response

            from fetch_flights import fetch_single_page

            result = fetch_single_page(mock_api_key, "SQ", sample_date)
            assert result is None

    def test_fetch_single_page_api_error_response(self, mock_api_key, sample_date):
        """Test handling of API error in response"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"error": {"message": "Invalid API key"}}
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            from fetch_flights import fetch_single_page

            result = fetch_single_page(mock_api_key, "SQ", sample_date)
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


class TestLoadAirlinesConfig:
    """Tests for load_airlines_config function"""

    def test_load_config_success(self):
        """Test successful config loading"""
        from fetch_flights import load_airlines_config

        config = load_airlines_config()

        assert isinstance(config, dict)
        assert "airlines" in config
        assert "SQ" in config["airlines"]

    @patch("builtins.open")
    def test_load_config_file_not_found(self, mock_open):
        """Test handling of missing config file"""
        from fetch_flights import load_airlines_config

        mock_open.side_effect = FileNotFoundError()

        with patch("builtins.print"):
            with pytest.raises(SystemExit):
                load_airlines_config()

    @patch("builtins.open")
    @patch("json.load")
    def test_load_config_invalid_json(self, mock_json_load, mock_open):
        """Test handling of invalid JSON in config"""
        from fetch_flights import load_airlines_config

        mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

        with patch("builtins.print"):
            with pytest.raises(SystemExit):
                load_airlines_config()


class TestListAirlines:
    """Tests for list_airlines function"""

    def test_list_airlines(self, mock_airline_config, capsys):
        """Test listing airlines"""
        from fetch_flights import list_airlines

        list_airlines(mock_airline_config)

        output = capsys.readouterr().out
        assert "AVAILABLE AIRLINES" in output
        assert "Singapore Airlines" in output
        assert "Emirates" in output
        assert "Total: 3 airlines" in output


class TestGetApiKey:
    """Tests for get_api_key function"""

    def test_get_api_key_from_env(self, mock_env_vars, capsys):
        """Test getting API key from environment"""
        from fetch_flights import get_api_key

        api_key = get_api_key()

        assert api_key == "test_api_key_1234567890abcdef"
        output = capsys.readouterr().out
        assert "[INFO] Using API key from .env file" in output

    @patch("builtins.input")
    def test_get_api_key_from_input(self, mock_input, monkeypatch, capsys):
        """Test getting API key from user input"""
        from fetch_flights import get_api_key

        monkeypatch.delenv("AIRLABS_API_KEY", raising=False)
        mock_input.return_value = "user_entered_key_12345"

        api_key = get_api_key()

        assert api_key == "user_entered_key_12345"
        output = capsys.readouterr().out
        assert "[WARN] No API key found" in output

    @patch("builtins.input")
    def test_get_api_key_empty_input(self, mock_input, monkeypatch):
        """Test handling of empty API key input"""
        from fetch_flights import get_api_key

        monkeypatch.delenv("AIRLABS_API_KEY", raising=False)
        mock_input.return_value = ""

        with patch("builtins.print"):
            with pytest.raises(SystemExit):
                get_api_key()


class TestFetchFlightsRetry:
    """Tests for fetch_single_page retry logic"""

    def test_fetch_retry_on_timeout(self, mock_api_key, sample_date):
        """Test retry logic on timeout"""
        from fetch_flights import fetch_single_page

        with patch("requests.get") as mock_get:
            # First two attempts timeout, third succeeds
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"response": []}
            mock_response.raise_for_status = Mock()

            mock_get.side_effect = [
                requests.exceptions.Timeout("Timeout 1"),
                requests.exceptions.Timeout("Timeout 2"),
                mock_response,
            ]

            with patch("time.sleep"):
                result = fetch_single_page(mock_api_key, "SQ", sample_date)

            assert result is not None
            assert mock_get.call_count == 3

    def test_fetch_retry_on_rate_limit(self, mock_api_key, sample_date):
        """Test retry logic on rate limiting"""
        from fetch_flights import fetch_single_page

        with patch("requests.get") as mock_get:
            mock_response_429 = Mock()
            mock_response_429.status_code = 429
            mock_response_429.raise_for_status.side_effect = (
                requests.exceptions.HTTPError("Rate limited")
            )

            mock_response_200 = Mock()
            mock_response_200.status_code = 200
            mock_response_200.json.return_value = {"response": []}
            mock_response_200.raise_for_status = Mock()

            mock_get.side_effect = [mock_response_429, mock_response_200]

            with patch("time.sleep"):
                result = fetch_single_page(mock_api_key, "SQ", sample_date)

            assert result is not None
            assert mock_get.call_count == 2


class TestSaveCheckpoint:
    """Tests for save_checkpoint function"""

    def test_save_checkpoint(self, mock_api_response, temp_output_dir, monkeypatch):
        """Test checkpoint file creation"""
        import fetch_flights
        from fetch_flights import save_checkpoint

        # Temporarily change OUTPUT_DIR for test
        original_dir = fetch_flights.OUTPUT_DIR
        fetch_flights.OUTPUT_DIR = temp_output_dir

        try:
            filepath = save_checkpoint(mock_api_response, "SQ", "2025-01-01")

            assert "checkpoint_SQ_2025-01-01.json" in filepath
            assert os.path.exists(filepath)

            with open(filepath, "r") as f:
                data = json.load(f)
                assert data == mock_api_response
        finally:
            fetch_flights.OUTPUT_DIR = original_dir


class TestGenerateOutputFilename:
    """Tests for generate_output_filename function"""

    def test_generate_output_filename_csv(self):
        """Test filename generation for CSV"""
        from fetch_flights import generate_output_filename

        filename = generate_output_filename("SQ", "csv")

        assert "SQ_" in filename
        assert filename.endswith(".csv")
        assert "outputs" in filename

    def test_generate_output_filename_excel(self):
        """Test filename generation for Excel"""
        from fetch_flights import generate_output_filename

        filename = generate_output_filename("EK", "excel")

        assert "EK_" in filename
        assert filename.endswith(".xlsx")
        assert "outputs" in filename

    def test_generate_output_filename_json(self):
        """Test filename generation for JSON"""
        from fetch_flights import generate_output_filename

        filename = generate_output_filename("QR", "json")

        assert "QR_" in filename
        assert filename.endswith(".json")
        assert "outputs" in filename


class TestInteractiveMode:
    """Tests for interactive_mode function"""

    @patch("builtins.input")
    def test_interactive_mode_defaults(self, mock_input, mock_airline_config):
        """Test interactive mode with default values"""
        from fetch_flights import interactive_mode

        mock_input.side_effect = ["", "", "", ""]  # All defaults

        airline, start_date, end_date, output_format = interactive_mode(
            mock_airline_config
        )

        from fetch_flights import validate_date

        assert airline == "SQ"
        assert output_format == "excel"
        assert validate_date(start_date)
        assert validate_date(end_date)

    @patch("builtins.input")
    def test_interactive_mode_custom_values(self, mock_input, mock_airline_config):
        """Test interactive mode with custom values"""
        from fetch_flights import interactive_mode

        mock_input.side_effect = ["EK", "2025-01-01", "2025-01-07", "csv"]

        airline, start_date, end_date, output_format = interactive_mode(
            mock_airline_config
        )

        assert airline == "EK"
        assert start_date == "2025-01-01"
        assert end_date == "2025-01-07"
        assert output_format == "csv"

    @patch("builtins.input")
    def test_interactive_mode_list_airlines(
        self, mock_input, mock_airline_config, capsys
    ):
        """Test interactive mode with list command"""
        from fetch_flights import interactive_mode

        mock_input.side_effect = ["list", "SQ", "", "", ""]

        airline, start_date, end_date, output_format = interactive_mode(
            mock_airline_config
        )

        assert airline == "SQ"
        output = capsys.readouterr().out
        assert "AVAILABLE AIRLINES" in output


class TestFetchDateRange:
    """Tests for fetch_date_range function (with pagination support)"""

    @patch("fetch_flights.tqdm")
    @patch("fetch_flights.fetch_flights_for_date")
    @patch("fetch_flights.save_checkpoint")
    @patch("time.sleep")
    def test_fetch_date_range_single_day(
        self,
        mock_sleep,
        mock_save,
        mock_fetch,
        mock_tqdm,
        mock_api_key,
        mock_api_response,
    ):
        """Test fetching single day"""
        from fetch_flights import fetch_date_range

        # Add pages_fetched to mock response (pagination metadata)
        mock_response = {**mock_api_response, "pages_fetched": 1}
        mock_fetch.return_value = mock_response
        mock_tqdm.return_value.__enter__.return_value = Mock()

        flights = fetch_date_range(mock_api_key, "SQ", "2025-01-01", "2025-01-01")

        assert len(flights) == 3
        assert mock_fetch.call_count == 1
        assert mock_save.call_count == 1

    @patch("fetch_flights.tqdm")
    @patch("fetch_flights.fetch_flights_for_date")
    @patch("fetch_flights.save_checkpoint")
    @patch("time.sleep")
    def test_fetch_date_range_multiple_days(
        self,
        mock_sleep,
        mock_save,
        mock_fetch,
        mock_tqdm,
        mock_api_key,
        mock_api_response,
    ):
        """Test fetching multiple days"""
        from fetch_flights import fetch_date_range

        # Add pages_fetched to mock response (pagination metadata)
        mock_response = {**mock_api_response, "pages_fetched": 1}
        mock_fetch.return_value = mock_response
        mock_tqdm.return_value.__enter__.return_value = Mock()

        flights = fetch_date_range(mock_api_key, "SQ", "2025-01-01", "2025-01-03")

        assert len(flights) == 9  # 3 days * 3 flights
        assert mock_fetch.call_count == 3
        assert mock_save.call_count == 3

    @patch("fetch_flights.tqdm")
    @patch("fetch_flights.fetch_flights_for_date")
    @patch("time.sleep")
    def test_fetch_date_range_no_data(
        self, mock_sleep, mock_fetch, mock_tqdm, mock_api_key
    ):
        """Test fetching when no data returned"""
        from fetch_flights import fetch_date_range

        mock_fetch.return_value = None
        mock_tqdm.return_value.__enter__.return_value = Mock()

        flights = fetch_date_range(mock_api_key, "SQ", "2025-01-01", "2025-01-01")

        assert flights == []


class TestMainFunction:
    """Tests for main() function"""

    @patch("fetch_flights.list_airlines")
    def test_main_list_airlines(self, mock_list, mock_airline_config):
        """Test --list-airlines command"""
        from fetch_flights import main

        with patch("sys.argv", ["fetch_flights.py", "--list-airlines"]):
            with patch(
                "fetch_flights.load_airlines_config", return_value=mock_airline_config
            ):
                with patch("sys.exit") as mock_exit:
                    mock_exit.side_effect = SystemExit(0)
                    with pytest.raises(SystemExit):
                        main()

        mock_list.assert_called_once()
        mock_exit.assert_called_once_with(0)

    @patch("fetch_flights.fetch_date_range")
    @patch("fetch_flights.get_api_key")
    @patch("builtins.input")
    @patch("fetch_flights.validate_api_key")
    @patch("fetch_flights.export_to_excel")
    @patch("fetch_flights.generate_output_filename")
    @patch("fetch_flights.generate_summary")
    def test_main_yesterday_flag(
        self,
        mock_summary,
        mock_filename,
        mock_export,
        mock_validate,
        mock_input,
        mock_get_key,
        mock_fetch,
        mock_airline_config,
        mock_api_response,
    ):
        """Test main with --yesterday flag"""
        from fetch_flights import extract_flight_data, main

        mock_get_key.return_value = "test_key"
        mock_validate.return_value = True
        mock_input.return_value = "y"
        mock_fetch.return_value = extract_flight_data(mock_api_response)
        mock_filename.return_value = "outputs/test.xlsx"
        mock_summary.return_value = {
            "total_flights": 3,
            "average_delay_minutes": 5.0,
            "on_time_percentage": 80.0,
            "cancelled_flights": 0,
        }

        with patch("sys.argv", ["fetch_flights.py", "--airline", "SQ", "--yesterday"]):
            with patch(
                "fetch_flights.load_airlines_config", return_value=mock_airline_config
            ):
                with patch("builtins.print"):
                    main()

        mock_fetch.assert_called_once()
        mock_export.assert_called_once()

    @patch("sys.exit")
    @patch("builtins.input")
    def test_main_invalid_airline(self, mock_input, mock_exit, mock_airline_config):
        """Test main with invalid airline"""
        from fetch_flights import main

        def side_effect(*args):
            raise SystemExit(1)

        mock_exit.side_effect = side_effect

        with patch("sys.argv", ["fetch_flights.py", "--airline", "XX", "--yesterday"]):
            with patch(
                "fetch_flights.load_airlines_config", return_value=mock_airline_config
            ):
                with patch("builtins.print"):
                    with pytest.raises(SystemExit):
                        main()

        mock_exit.assert_called_once_with(1)

    @patch("sys.exit")
    def test_main_missing_start_date(self, mock_exit, mock_airline_config):
        """Test main with missing start date"""
        from fetch_flights import main

        def side_effect(*args):
            raise SystemExit(1)

        mock_exit.side_effect = side_effect

        with patch("sys.argv", ["fetch_flights.py", "--airline", "SQ"]):
            with patch(
                "fetch_flights.load_airlines_config", return_value=mock_airline_config
            ):
                with patch("builtins.print"):
                    with pytest.raises(SystemExit):
                        main()

        mock_exit.assert_called_once_with(1)

    @patch("sys.exit")
    def test_main_invalid_date(self, mock_exit, mock_airline_config):
        """Test main with invalid date format"""
        from fetch_flights import main

        def side_effect(*args):
            raise SystemExit(1)

        mock_exit.side_effect = side_effect

        with patch(
            "sys.argv",
            ["fetch_flights.py", "--airline", "SQ", "--start-date", "invalid-date"],
        ):
            with patch(
                "fetch_flights.load_airlines_config", return_value=mock_airline_config
            ):
                with patch("builtins.print"):
                    with pytest.raises(SystemExit):
                        main()

        mock_exit.assert_called_once_with(1)

    @patch("fetch_flights.fetch_date_range")
    @patch("fetch_flights.get_api_key")
    @patch("builtins.input")
    @patch("sys.exit")
    def test_main_no_flights_found(
        self, mock_exit, mock_input, mock_get_key, mock_fetch, mock_airline_config
    ):
        """Test main when no flights are found"""
        from fetch_flights import main

        def side_effect(*args):
            raise SystemExit(0)

        mock_exit.side_effect = side_effect
        mock_get_key.return_value = "test_key"
        mock_input.return_value = "y"
        mock_fetch.return_value = []

        with patch("sys.argv", ["fetch_flights.py", "--airline", "SQ", "--yesterday"]):
            with patch(
                "fetch_flights.load_airlines_config", return_value=mock_airline_config
            ):
                with patch("builtins.print"):
                    with pytest.raises(SystemExit):
                        main()

        mock_exit.assert_called_once_with(0)

    @patch("fetch_flights.fetch_date_range")
    @patch("fetch_flights.get_api_key")
    @patch("builtins.input")
    @patch("sys.exit")
    def test_main_user_cancels(
        self, mock_exit, mock_input, mock_get_key, mock_fetch, mock_airline_config
    ):
        """Test main when user cancels"""
        from fetch_flights import main

        mock_get_key.return_value = "test_key"
        mock_input.return_value = "n"

        with patch("sys.argv", ["fetch_flights.py", "--airline", "SQ", "--yesterday"]):
            with patch(
                "fetch_flights.load_airlines_config", return_value=mock_airline_config
            ):
                with patch("builtins.print"):
                    main()

        mock_exit.assert_called_once_with(0)
