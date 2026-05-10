import logging
import ipaddress
from datetime import datetime


class LogEntry:
    """Represent a single entry from a web server access log."""

    def __init__(self, log_line):
        """Initialize a LogEntry object by parsing a raw log line."""
        # 1. Split by double quotes to isolate the HTTP request
        parts = log_line.split('"')
        # parts[1] should contain request; be defensive
        self.request = parts[1] if len(parts) > 1 else ""

        # parse method/path/protocol from the quoted request
        try:
            req_parts = self.request.split()
            self.method = req_parts[0] if len(req_parts) >= 1 else None
            self.path = req_parts[1] if len(req_parts) >= 2 else None
            self.protocol = req_parts[2] if len(req_parts) >= 3 else None
        except Exception:
            self.method = None
            self.path = None
            self.protocol = None

        # 2. Split the left part by spaces to get the IP and timestamp
        left_parts = parts[0].split()
        # left_parts[0] is expected to be the IP address
        self.ip = ipaddress.IPv4Address(left_parts[0])

        # Strip the leading bracket from the timestamp string
        if len(left_parts) > 3:
            raw_timestamp = left_parts[3].lstrip('[')
        else:
            raw_timestamp = ""
        self.timestamp = (
            self._parse_timestamp(raw_timestamp)
            if raw_timestamp
            else None
        )

        # 3. Split the right part by spaces to get status and size
        right_parts = parts[2].split() if len(parts) > 2 else []
        try:
            self.status = int(right_parts[0]) if right_parts else None
        except Exception:
            self.status = None

        try:
            size_str = right_parts[1]
            self.size = int(size_str) if size_str != '-' else 0
        except Exception:
            self.size = None

    def _parse_timestamp(self, timestamp_str):
        """Parse timestamp string using split() to a datetime object."""
        months = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
            'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
            'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }

        try:
            time_parts = timestamp_str.split(':')
            date_string = time_parts[0]
            hour = int(time_parts[1])
            minute = int(time_parts[2])
            second = int(time_parts[3])

            date_parts = date_string.split('/')
            day = int(date_parts[0])
            month = months[date_parts[1]]
            year = int(date_parts[2])

            return datetime(year, month, day, hour, minute, second)
        except Exception:
            logging.warning("Failed to parse timestamp: %s", timestamp_str)
            return None

    def __str__(self):
        """Return a human-readable string representation of the entry."""
        return (
            f"[{self.timestamp}] {self.ip} -> "
            f"{self.request} ({self.status})"
        )

    def __repr__(self):
        """Return an unambiguous string representation of the instance."""
        return (
            f"LogEntry(ip='{self.ip}', "
            f"timestamp={repr(self.timestamp)}, "
            f"request='{self.request}', "
            f"status={self.status}, "
            f"size={self.size})"
        )


def parse_log_line(log_line):
    """Create a LogEntry object from a single raw log line."""
    return LogEntry(log_line)


def read_log_file(file_path):
    """Read a logfile and return a list of LogEntry objects."""
    entries = []
    with open(file_path, "r", encoding="utf-8") as log_file:
        for line in log_file:
            cleaned_line = line.strip()
            if not cleaned_line:
                continue
            try:
                entry = parse_log_line(cleaned_line)
            except Exception:
                msg = f"Skipping malformed log line: {cleaned_line}"
                logging.warning(msg)
                continue
            entries.append(entry)
    return entries


def display_requests_between(entries, start_time, end_time):
    """Print requests for entries between two datetime moments."""
    if end_time < start_time:
        print("Warning: second datetime is earlier than the first one.")
        return

    for entry in entries:
        if start_time <= entry.timestamp <= end_time:
            print(entry.request)


if __name__ == "__main__":
    raw_line = (
        '192.168.1.10 - - [18/Oct/2020:01:30:42 +0200] '
        '"GET /index.html HTTP/1.1" 200 1024\n'
    )
    print("Task 6 - parse_log_line:")
    parsed_entry = parse_log_line(raw_line)
    print(parsed_entry)
    print(repr(parsed_entry))

    print("\nTask 7 - read_log_file:")
    log_entries = read_log_file("data/server_log.txt")
    print(f"Loaded entries: {len(log_entries)}")
    print(f"First request: {log_entries[0].request}")

    print("\nTask 8 - display_requests_between (valid range):")
    range_start = datetime(2020, 10, 18, 1, 0, 0)
    range_end = datetime(2020, 10, 18, 2, 0, 0)
    display_requests_between(log_entries, range_start, range_end)

    print("\nTask 8 - display_requests_between (reversed range):")
    display_requests_between(
        log_entries,
        datetime(2020, 10, 19),
        datetime(2020, 10, 18),
    )
