import ipaddress
import logging
import os
import re
import sys


def read_config(filepath="lab.config"):
    if not os.path.exists(filepath):
        sys.exit("Config file not found.")

    config_data = {
        "Display": {"lines": 10, "separator": ",", "filter": "GET"},
        "LogFile": {"filename": "default.log"},
        "Config": {"level": "INFO"}
    }

    section_re = re.compile(r"^\[(.*?)\]$")
    kv_re = re.compile(r"^([^=]+)=(.*)$")
    current_section = None

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            sec_match = section_re.match(line)
            if sec_match:
                current_section = sec_match.group(1)
                if current_section not in config_data:
                    config_data[current_section] = {}
                continue

            kv_match = kv_re.match(line)
            if kv_match and current_section:
                key, val = kv_match.groups()
                config_data[current_section][key.strip()] = val.strip()

    display_settings = config_data.get("Display", {})
    log_filename = config_data.get("LogFile", {}).get("filename")

    config_level = config_data.get("Config", {}).get("level", "INFO")
    log_level = getattr(logging, config_level.upper(), logging.INFO)
    logging.basicConfig(level=log_level)

    return display_settings, log_filename


def read_log_file(filename):
    if not os.path.exists(filename):
        sys.exit(f"Log file {filename} does not exist.")
    with open(filename, 'r') as f:
        return f.readlines()


def parse_log_line(line):
    pattern = (
        r'^(\S+) \S+ \S+ \[([^\]]+)\] "(.*?)" '
        r'(\d+) (\d+)(?: "(.*?)" "(.*?)")?'
    )
    match = re.search(pattern, line)

    if match:
        return {
            "ip": match.group(1),
            "timestamp": match.group(2),
            "request_header": match.group(3),
            "status": int(match.group(4)),
            "size": int(match.group(5)),
            "user_agent": match.group(7) if match.group(7) else ""
        }
    return None


def parse_all_lines(lines):
    parsed_entries = []
    for line in lines:
        entry = parse_log_line(line)
        if entry:
            parsed_entries.append(entry)
    return parsed_entries


def is_in_subnet(ip_address, subnet):
    try:
        ip_obj = ipaddress.ip_address(ip_address)
        net_obj = ipaddress.ip_network(subnet, strict=False)
        return ip_obj in net_obj
    except ValueError:
        return False


def print_subnet_requests(entries, display_limit):
    student_index = 282636
    mask_length = (student_index % 16) + 8

    subnet = f"192.168.1.0/{mask_length}"

    count = 0
    for entry in entries:
        if is_in_subnet(entry['ip'], subnet):
            print(entry)
            count += 1
            if count % int(display_limit) == 0:
                input("Press Enter to continue...")


def print_bytes_for_request_type(entries, display_cfg):
    request_type = display_cfg.get("filter", "").strip().upper()
    separator = display_cfg.get("separator", ",")
    request_pattern = re.compile(r'^\s*([A-Z]+)\b', re.IGNORECASE)
    total_bytes = 0

    for entry in entries:
        request_header = entry.get('request_header', '')
        method_match = request_pattern.match(request_header)
        if not method_match:
            continue

        method = method_match.group(1).upper()
        if method == request_type:
            total_bytes += entry.get('size', 0)

    print(f"{request_type}{separator}{total_bytes}")


def print_browser_requests(entries, browser="Chrome"):
    for entry in entries:
        if browser.lower() in entry.get('user_agent', '').lower():
            print(entry)


if __name__ == "__main__":
    display_cfg, log_file = read_config("lab.config")
    raw_lines = read_log_file(log_file)
    log_entries = parse_all_lines(raw_lines)

    print("--- Subnet Requests ---")
    print_subnet_requests(log_entries, display_cfg.get("lines", 10))

    print("\n--- Request Type Byte Summary ---")
    print_bytes_for_request_type(log_entries, display_cfg)

    print("\n--- Browser Requests ---")
    print_browser_requests(log_entries, "Chrome")
