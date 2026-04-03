import logging
import sys


logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")


def read_log():

    lines = sys.stdin.readlines()

    logging.debug(
        f"Successfully read {len(lines)} lines from standard input."
    )

    entries = []

    for line in lines:
        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        parts = cleaned_line.split()

        path = str(parts[0])
        status_code = int(parts[1])
        bytes_sent = int(parts[2])
        processing_time = int(parts[3])

        entry_tuple = (path, status_code, bytes_sent, processing_time)
        entries.append(entry_tuple)

    logging.debug(
        f"Successfully parsed and stored {len(entries)} valid log entries."
    )

    return entries


def successful_reads(log_entries):
    """Return only entries with HTTP 2xx status codes."""
    successful_entries = [
        entry for entry in log_entries if 200 <= entry[1] < 300
    ]
    logging.info("Successful reads: %d entries.", len(successful_entries))
    return successful_entries


def failed_reads(log_entries):
    """Return entries with HTTP 4xx and 5xx status codes."""
    failed_4xx = [
        entry for entry in log_entries if 400 <= entry[1] < 500
    ]
    failed_5xx = [
        entry for entry in log_entries if 500 <= entry[1] < 600
    ]

    logging.info("Failed reads with 4xx codes: %d entries.", len(failed_4xx))
    logging.info("Failed reads with 5xx codes: %d entries.", len(failed_5xx))

    return failed_4xx + failed_5xx


def html_entries(log_entries):
    """Return successfully retrieved .html entries."""
    return [
        entry
        for entry in log_entries
        if 200 <= entry[1] < 300 and entry[0].lower().endswith(".html")
    ]


def print_html_entries(log_entries):
    """Print HTML entries retrieved successfully."""
    print(html_entries(log_entries))


def run():
    """Main execution function."""
    log_entries = read_log()

    successful_reads(log_entries)
    failed_reads(log_entries)
    print_html_entries(log_entries)


if __name__ == "__main__":
    run()
