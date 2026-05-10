import json
import logging
from ipaddress import ip_address, IPv4Address
from typing import Any

import log_entry
from config import DEFAULT_CONFIG, CONFIG_FILE, load_config, save_config


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
        "log_file": get_input(
            "Log file path", DEFAULT_CONFIG["log_file"]
        ),
        "ip_address": get_input(
            "IP address to display (empty shows all)",
            DEFAULT_CONFIG["ip_address"],
        ),
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
        "request_method": get_input(
            "Request method filter (GET, POST, PUT, DELETE) - empty for all",
            DEFAULT_CONFIG.get("request_method", ""),
        ),
    }


# Configuration load/save are provided by src/config.py (DEFAULT_CONFIG,
# load_config, save_config).

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


def filter_entries_by_method(entries: list, method_raw: str | None) -> list:
    if not method_raw:
        return entries

    method_upper = method_raw.strip().upper()

    def keep(entry):
        m = getattr(entry, "method", None)
        if not m:
            return False
        return m.upper() == method_upper

    return [entry for entry in entries if keep(entry)]


def display_entries(
    entries: list, lines_per_page: int, show_timestamps: bool
) -> None:
    if not entries:
        print("No log entries to display.")
        return
    if lines_per_page <= 0:
        logging.warning("Invalid lines_per_page value. Showing all.")
        lines_per_page = len(entries)

    printed = 0
    for index, entry in enumerate(entries, start=1):
        printed += 1
        ts = getattr(entry, "timestamp", None)
        timestamp = f"[{ts}] " if show_timestamps and ts else ""
        method = getattr(entry, "method", None) or "-"
        path = getattr(entry, "path", None) or "-"
        status = getattr(entry, "status", None) or "-"
        size = getattr(entry, "size", None)
        size_display = size if size is not None else "-"
        msg = f"{index}. {timestamp}{entry.ip} {method} {path}"
        print(f"{msg} {status} {size_display}")

        if printed % lines_per_page == 0 and index != len(entries):
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
        chosen_ip = (
            ip_address(chosen_ip_raw) if chosen_ip_raw else None
        )
    except ValueError:
        logging.error(
            f"Invalid IP address in configuration: {chosen_ip_raw}"
        )
        raise SystemExit(
            f"Error: invalid IP address '{chosen_ip_raw}'."
        )

    # apply IP filter first
    filtered_entries = filter_entries_by_ip(log["entries"], chosen_ip)

    # validate and normalise lines_per_page
    try:
        lines_per_page = int(
            config.get(
                "lines_per_page", DEFAULT_CONFIG["lines_per_page"]
            )
        )
    except Exception:
        msg = "lines_per_page is not an integer. Using default."
        logging.warning(msg)
        lines_per_page = DEFAULT_CONFIG["lines_per_page"]

    if lines_per_page <= 0:
        default_lpp = DEFAULT_CONFIG["lines_per_page"]
        logging.warning(
            "Invalid lines_per_page. Using default value: %s.",
            default_lpp,
        )
        lines_per_page = default_lpp

    # Sanity-check to catch internal bugs. Validate first, then assert.
    assert lines_per_page > 0, (
        "lines_per_page must be > 0"
    )  # Ensures pagination fallback worked; bugs in validation break this.

    # filter by HTTP method (case-insensitive)
    filtered_entries = filter_entries_by_method(
        filtered_entries, config.get("request_method")
    )

    print("\nConfiguration:")
    print(json.dumps(config, indent=4, ensure_ascii=False))

    print("\nLog entries:")
    if chosen_ip:
        print(f"Showing only IP address: {chosen_ip}")
    else:
        print("Showing all IP addresses")

    display_entries(
        filtered_entries,
        lines_per_page,
        config["show_timestamps"],
    )


if __name__ == "__main__":
    run()
