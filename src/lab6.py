import json
import logging
from pathlib import Path
from ipaddress import ip_address, IPv4Address
from typing import Any

import log_entry


CONFIG_FILE = Path("data/config.json")
ENCODING = "utf-8"


# CONFIG OPERATIONS

def ask_config() -> dict:
    print("Application configuration\n")

    return {
        "log_file": input("Log file path: ").strip(),
        "ip_address": input("IP address to display (leave empty to show all): ").strip(),
        "logging_level": input(
            "Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL): "
        ).strip().upper(),
        "lines_per_page": int(input("Lines per page: ").strip()),
        "show_timestamps": input("Show timestamps? (yes/no): ").strip().lower()
        in ("yes", "y"),
    }


def save_config(config: dict, filename: Path = CONFIG_FILE) -> None:
    with filename.open("w", encoding=ENCODING) as file:
        json.dump(config, file, indent=4, ensure_ascii=False)


def load_config(filename: Path = CONFIG_FILE) -> dict:
    with filename.open("r", encoding=ENCODING) as file:
        return json.load(file)


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
        return {}

    return {
        "filename": filename,
        "entries": log_entry.read_log_file(filename),
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
        print(f"\nConfig saved to {CONFIG_FILE}")
    else:
        config = load_config()
        print(f"\nLoaded config from {CONFIG_FILE}")

    setup_logging(config["logging_level"])

    log = read_log(config["log_file"])

    chosen_ip_raw = config["ip_address"].strip()
    chosen_ip = ip_address(chosen_ip_raw) if chosen_ip_raw else None

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