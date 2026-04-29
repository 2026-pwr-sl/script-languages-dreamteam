import log_entry

def run():
    log = read_log("data/server_log.txt")
    
def read_log(filename) -> dict[str, any]:
    """
    Reads a log file and returns it as a dictionary with the filename and entries.
    Each entry is a LogEntry object created by the log_entry module.
    """
    object = {}
    
    object["filename"] = filename
    object["entries"] = log_entry.read_log_file(filename)
    
    return object
    
if __name__ == "__main__":
    run()