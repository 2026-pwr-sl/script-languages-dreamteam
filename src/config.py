import json
import logging
from pathlib import Path


ENCODING = "utf-8"
CONFIG_FILE = Path("data/config.json")

DEFAULT_CONFIG = {
    "log_file": "data/server_log.txt",
    "ip_address": "",
    "logging_level": "INFO",
    "lines_per_page": 10,
    "show_timestamps": True,
    "request_method": "",
}


def save_config(config: dict, filename: Path = CONFIG_FILE) -> None:
    with filename.open("w", encoding=ENCODING) as file:
        json.dump(config, file, indent=4, ensure_ascii=False)


def load_config(filename: Path = CONFIG_FILE) -> dict:
    """Load config from JSON, merge with defaults, validate.

    - If file missing: log info and return defaults copy.
    - If JSON invalid: log error and exit via SystemExit.
    - Missing keys fall back to defaults with an info log.
    """
    if not filename.exists():
        msg = "Configuration file does not exist. Using defaults."
        logging.info(msg)
        return DEFAULT_CONFIG.copy()

    try:
        with filename.open("r", encoding=ENCODING) as file:
            config = json.load(file)
    except json.JSONDecodeError:
        logging.error("Configuration file is not a correct JSON file.")
        raise SystemExit("Invalid configuration file. Application stopped.")

    final_config = DEFAULT_CONFIG.copy()

    for key, default_value in DEFAULT_CONFIG.items():
        value = config.get(key)
        # Allow empty ip_address (show all); require other keys
        if key != "ip_address" and (value is None or value == ""):
            logging.info(f"Using default for '{key}'")
            final_config[key] = default_value
        else:
            if key == "ip_address" and (value is None or value == ""):
                # ip_address allows empty string to show all; normalize None to ""
                final_config[key] = ""
            elif key != "ip_address" and (value is None or value == ""):
                logging.info(f"Using default for '{key}'")
                final_config[key] = default_value
            else:
                final_config[key] = value

    return final_config
