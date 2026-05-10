import json
import logging
from pathlib import Path
from ipaddress import ip_address, IPv4Address
from typing import Any

import log_entry


CONFIG_FILE = Path("data/config.json")
ENCODING = "utf-8"

DEFAULT_CONFIG = {

    "log_file": "data/server_log.txt",

    "ip_address": "",

    "logging_level": "INFO",

    "lines_per_page": 10,

    "show_timestamps": True,

    "request_method": "GET",

}

# CONFIG OPERATIONS

def ask_config() -> dict:
    print("Application configuration (press Enter to use default)\n")

    def get_input(prompt: str, default: Any, cast_func=None):
        user_input = input(f"{prompt} [{default}]: ").strip()
        if not user_input:
            return default
        if cast_func:
            try:
                return cast_func(user_input)
            except ValueError:
                print(f"Invalid value. Using default: {default}")
                return default
        return user_input

    return {
        "log_file": get_input("Log file path", DEFAULT_CONFIG["log_file"]),
        "ip_address": get_input("IP address to display (leave empty to show all)", DEFAULT_CONFIG["ip_address"]),
        "logging_level": get_input(
            "Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
            DEFAULT_CONFIG["logging_level"]
        ).upper(),
        "lines_per_page": get_input(
            "Lines per page",
            DEFAULT_CONFIG["lines_per_page"],
            int
        ),
        "show_timestamps": get_input(
            "Show timestamps? (yes/no)",
            DEFAULT_CONFIG["show_timestamps"],
            lambda x: x.lower() in ("yes", "y")
        ),
    }


def save_config(config: dict, filename: Path = CONFIG_FILE) -> None:
    with filename.open("w", encoding=ENCODING) as file:
        json.dump(config, file, indent=4, ensure_ascii=False)


def load_config(filename: Path = CONFIG_FILE) -> dict:

    if not filename.exists():

        logging.info("Configuration file does not exist. Using default values.")

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

        if key != "ip_address" and (value is None or value == ""):

            logging.info(f"Using default for '{key}'")

            final_config[key] = default_value

        else:

            final_config[key] = value

    return final_config

# LOG OPERATIONS

def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True,
    )




def read_log(filename: str) -> dict[str, Any]:

    if not filename:

        logging.error("Filename is empty.")

        raise SystemExit("Error: log file name is empty.")

    try:

        entries = log_entry.read_log_file(filename)

    except FileNotFoundError:

        logging.error(f"Log file does not exist: {filename}")

        raise SystemExit(f"Error: log file '{filename}' not found.")

    return {

        "filename": filename,

        "entries": entries,

    }


def filter_entries_by_ip(entries: list, ip: IPv4Address | None) -> list:
    if ip is None:
        return entries

    return [
        entry for entry in entries
        if entry.ip == ip
    ]


def display_entries(entries: list, lines_per_page: int, show_timestamps: bool) -> None:
    if not entries:
        print("No log entries to display.")
        return

    if lines_per_page <= 0:
        logging.warning("Invalid lines_per_page value. Showing all entries.")
        lines_per_page = len(entries)

    for index, entry in enumerate(entries, start=1):
        if show_timestamps:
            print(f"{index}. [{entry.timestamp}] {entry.ip}")
        else:
            print(f"{index}. {entry.ip}")

        if index % lines_per_page == 0 and index != len(entries):
            input("\nPress Enter to continue...\n")


def run() -> None:
    if not CONFIG_FILE.exists():

        config = ask_config()

        save_config(config)

    else:

        config = load_config()

    setup_logging(config["logging_level"])

    log = read_log(config["log_file"])

    chosen_ip_raw = config["ip_address"].strip()
    
    try:
        chosen_ip = ip_address(chosen_ip_raw) if chosen_ip_raw else None
    except ValueError:
        logging.error(f"Invalid IP address in configuration: {chosen_ip_raw}")
        raise SystemExit(f"Error: invalid IP address '{chosen_ip_raw}'.")
    
    filtered_entries = filter_entries_by_ip(log["entries"], chosen_ip)

    print("\nConfiguration:")
    print(json.dumps(config, indent=4, ensure_ascii=False))

    print("\nLog entries:")
    if chosen_ip:
        print(f"Showing only IP address: {chosen_ip}")
    else:
        print("Showing all IP addresses")

    display_entries(
        filtered_entries,
        config["lines_per_page"],
        config["show_timestamps"],
    )


if __name__ == "__main__":
    run()