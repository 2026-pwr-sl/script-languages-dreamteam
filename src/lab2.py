import sys


def main():
    largest_path = ""
    largest_bytes = -1
    largest_time = 0
    failed_requests = 0
    total_bytes = 0
    total_time = 0
    request_count = 0

    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        parts = line.split()
        path = parts[0]
        status_code = int(parts[1])
        bytes_sent = int(parts[2])
        processing_time = int(parts[3])

        if status_code == 404:
            print(f"!{path}")
            failed_requests += 1
        else:
            print(path)

        if bytes_sent > largest_bytes:
            largest_bytes = bytes_sent
            largest_path = path
            largest_time = processing_time

        total_bytes += bytes_sent
        total_time += processing_time
        request_count += 1

    total_kilobytes = total_bytes / 1024
    average_time = 0

    if request_count > 0:
        average_time = total_time / request_count

    print(f"Largest resource: {largest_path} {largest_time} ms")
    print(f"Failed requests: {failed_requests}")
    print(f"Total bytes: {total_bytes}")
    print(f"Total kilobytes: {total_kilobytes:.2f}")
    print(f"Average processing time: {average_time:.2f} ms")


if __name__ == "__main__":
    main()
