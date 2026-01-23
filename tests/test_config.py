"""
Tests for configuration validation
"""

import json
import os


class TestAirlinesConfig:
    """Tests for airlines_config.json"""

    def test_config_file_exists(self):
        """Test that airlines_config.json exists"""
        assert os.path.exists("airlines_config.json")

    def test_config_valid_json(self):
        """Test that airlines_config.json is valid JSON"""
        with open("airlines_config.json", "r") as f:
            config = json.load(f)
            assert isinstance(config, dict)

    def test_config_has_airlines_key(self):
        """Test that config has airlines key"""
        with open("airlines_config.json", "r") as f:
            config = json.load(f)
            assert "airlines" in config

    def test_config_has_minimum_airlines(self):
        """Test that config has at least 10 airlines"""
        with open("airlines_config.json", "r") as f:
            config = json.load(f)
            airlines = config.get("airlines", {})
            assert len(airlines) >= 10

    def test_config_airline_structure(self):
        """Test each airline has required fields"""
        with open("airlines_config.json", "r") as f:
            config = json.load(f)
            airlines = config.get("airlines", {})

            for code, info in airlines.items():
                assert isinstance(info, dict), f"Airline {code} must be a dict"
                assert "name" in info, f"Airline {code} missing 'name'"
                assert "iata" in info or "icao" in info, f"Airline {code} missing code"

    def test_config_has_singapore_airlines(self):
        """Test that Singapore Airlines (SQ) is in config"""
        with open("airlines_config.json", "r") as f:
            config = json.load(f)
            airlines = config.get("airlines", {})
            assert "SQ" in airlines
            assert airlines["SQ"]["name"] == "Singapore Airlines"


class TestEnvExample:
    """Tests for .env.example file"""

    def test_env_example_exists(self):
        """Test that .env.example exists"""
        assert os.path.exists(".env.example")

    def test_env_example_has_api_key(self):
        """Test .env.example has API key placeholder"""
        with open(".env.example", "r") as f:
            content = f.read()
            assert "AIRLABS_API_KEY" in content

    def test_env_example_no_real_key(self):
        """Test .env.example doesn't contain a real API key"""
        with open(".env.example", "r") as f:
            content = f.read()
            # Check it's a placeholder, not a real key
            assert "your_api_key_here" in content.lower() or "your" in content.lower()


class TestRequirements:
    """Tests for requirements files"""

    def test_requirements_exists(self):
        """Test that requirements.txt exists"""
        assert os.path.exists("requirements.txt")

    def test_requirements_has_core_deps(self):
        """Test requirements has core dependencies"""
        with open("requirements.txt", "r") as f:
            content = f.read().lower()
            assert "requests" in content
            assert "python-dotenv" in content
            assert "openpyxl" in content
            assert "tqdm" in content

    def test_requirements_dev_exists(self):
        """Test that requirements-dev.txt exists"""
        assert os.path.exists("requirements-dev.txt")

    def test_requirements_dev_has_test_deps(self):
        """Test requirements-dev has testing dependencies"""
        with open("requirements-dev.txt", "r") as f:
            content = f.read().lower()
            assert "pytest" in content
            assert "black" in content
            assert "flake8" in content
