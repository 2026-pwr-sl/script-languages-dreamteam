import sys
import logging

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

def read_log():

    lines = sys.stdin.readlines()
    
    logging.debug(f"Successfully read {len(lines)} lines from standard input.")
    
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
        
    logging.debug(f"Successfully parsed and stored {len(entries)} valid log entries.")
    
    return entries

def run():
    """Main execution function."""
    log_entries = read_log()
    
   

if __name__ == "__main__":
    run()