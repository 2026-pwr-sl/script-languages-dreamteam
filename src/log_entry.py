import ipaddress
from datetime import datetime


class LogEntry:
    """Represent a single entry from a web server access log."""

    def __init__(self, log_line):
        """Initialize a LogEntry object by parsing a raw log line."""
        # 1. Split by double quotes to isolate the HTTP request
        parts = log_line.split('"')
        self.request = parts[1]

        # 2. Split the left part by spaces to get the IP and timestamp
        left_parts = parts[0].split()
        self.ip = ipaddress.IPv4Address(left_parts[0])

        # Strip the leading bracket from the timestamp string
        raw_timestamp = left_parts[3].lstrip('[')
        self.timestamp = self._parse_timestamp(raw_timestamp)

        # 3. Split the right part by spaces to get status and size
        right_parts = parts[2].split()
        self.status = int(right_parts[0])

        size_str = right_parts[1]
        self.size = int(size_str) if size_str != '-' else 0

    def _parse_timestamp(self, timestamp_str):
        """Parse timestamp string using split() to a datetime object."""
        months = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
            'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
            'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }

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

    def __str__(self):
        """Return a human-readable string representation of the entry."""
        return f"[{self.timestamp}] {self.ip} -> {self.request} ({self.status})"

    def __repr__(self):
        """Return an unambiguous string representation of the instance."""
        return (
            f"LogEntry(ip='{self.ip}', "
            f"timestamp={repr(self.timestamp)}, "
            f"request='{self.request}', "
            f"status={self.status}, "
            f"size={self.size})"
        )


if __name__ == "__main__":
    raw_line = (
        '192.168.1.10 - - [18/Oct/2020:01:30:42 +0200] '
        '"GET /index.html HTTP/1.1" 200 1024\n'
    )
    entry = LogEntry(raw_line)

    print("Testing __str__:")
    print(entry)
    print("\nTesting __repr__:")
    print(repr(entry))