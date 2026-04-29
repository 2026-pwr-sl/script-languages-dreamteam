from ipaddress import *
import logging
import log_entry
    
def read_log(filename) -> dict[str, any]:
    """
    Reads a log file and returns it as a dictionary with the filename and entries.
    Each entry is a LogEntry object created by the log_entry module.
    """
    
    if not filename:
        logging.error("Filename is empty.")
        return {}
    
    object = {}
    
    object["filename"] = filename
    object["entries"] = log_entry.read_log_file(filename)
    
    object["ip_requests_number"] = {}
    
    for entry in object["entries"]:
        key = str(entry.ip)
        if key not in object["ip_requests_number"]:
            object["ip_requests_number"][key] = 0
        object["ip_requests_number"][key] += 1
    
    return object
    
def ip_requests_number(log : dict[str, any], ip_address : IPv4Address) -> int:
    """
    Returns the number of requests made by a specific IP address.
    """
    
    if not log["ip_requests_number"]:
        logging.warning("The log does not contain any IP address information.")
        return 0
    
    return log["ip_requests_number"].get(str(ip_address), 0)

def ip_find(log : dict[str, any], most_active = True) -> list[IPv4Address]:
    """
    Returns the most active IP address if most_active is True, otherwise returns the least active IP address.
    """
    if not log["ip_requests_number"]:
        logging.warning("The log does not contain any IP address information.")
        return None
    
    if most_active:
        max_number = max(log["ip_requests_number"].values())
        ip_addresses = [
            ip for ip, number in log["ip_requests_number"].items() if number == max_number
        ]    
    else:
        min_number = min(log["ip_requests_number"].values())
        ip_addresses = [
            ip for ip, number in log["ip_requests_number"].items() if number == min_number
        ] 
        
    return [ip_address(ip) for ip in ip_addresses]

def longest_request(log : dict[str, any]) -> str:
    """
    Returns the longest request in the log file.
    """
    if not log["entries"]:
        logging.warning("The log does not contain any entries.")
        return None
    
    entry = max(log["entries"], key = lambda entry: len(entry.request))
    return entry.request

def non_existent(log : dict[str, any]) -> list[str]:
    """
    Returns request strings for which result code was 404 (Page not found).
    """
    
    if not log["entries"]:
        logging.warning("The log does not contain any entries.")
        return []
    
    entries = [
        entry for entry in log["entries"] if entry.status == 404
    ]
    
    return [entry.request for entry in entries]

def run():
    log = read_log("data/server_log.txt")
    
    # Task 5 example usage:
    print(ip_requests_number(log, ip_address(IPv4Address("192.168.1.10"))))
    
    # Task 6 example usage:
    print(ip_find(log, most_active=True))
    
    # Task 7 example usage:
    print(longest_request(log))
    
    # Task 8 example usage:
    print(non_existent(log))

if __name__ == "__main__":
    run()