# src/utils.py
import json
import logging

def setup_logging():
    """Sets up the logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("agent.log"),
            logging.StreamHandler()
        ]
    )

def load_config(config_path="config.json"):
    """Loads the configuration from a JSON file."""
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Configuration file not found at {config_path}")
        return None

def format_patient_name(first_name, last_name):
    """
    Formats the patient's name.
    """
    return f"{last_name}, {first_name}"
