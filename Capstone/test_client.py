import time
import csv
import random
import json
import urllib.request

SERVER_URL = "http://127.0.0.1:8000"

def send_http_request(part_number):
    """Executes a standard point-lookup network fetch against the active server."""
    url = f"{SERVER_URL}/search/{part_number}"
    try:
        with urllib.request.urlopen(url) as response:
            payload = json.loads(response.read().decode())
            # Capture the exact internal database query lookup time reported by the server
            return payload["server_latency_ms"]
    except Exception as e:
        print(f"Network error targeting part {part_number}: {e}")
        return None

def trigger_index_state(is_enabled):
    """Communicates with the administrative endpoint to toggle the schema state."""
    url = f"{SERVER_URL}/admin/index?enabled={str(is_enabled).lower()}"
    request_object = urllib.request.Request(url, method="POST")
    try:
        with urllib.request.urlopen(request_object) as response:
            status_text = json.loads(response.read().decode())["status"]
            print(f"Server Confirmation: {status_text}")
    except Exception as e:
        print(f"Failed to communicate with administrative endpoints: {e}")

def execute_simulation_phase(output_filename):
    """Fires exactly 1,000 randomized lookups and saves the results to a CSV."""
    print(f"Running batch simulation loop... Exporting variables to {output_filename}")
    latencies = []
    
    # Construct an array of 1,000 randomly selected items across the 40,000 target rows
    target_pool = [f"PART-{str(random.randint(1, 40000)).zfill(5)}" for _ in range(1000)]
    
    for target_part in target_pool:
        elapsed_time = send_http_request(target_part)
        if elapsed_time is not None:
            latencies.append(elapsed_time)
        # Small delay to mimic a human transaction pacing threshold
        time.sleep(0.002)
        
    # Open context spreadsheet writer to drop physical file records onto local disk
    with open(output_filename, mode="w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["QueryIteration", "LatencyMS"])
        for iteration_num, value in enumerate(latencies, 1):
            csv_writer.writerow([iteration_num, value])
            
    avg = sum(latencies) / len(latencies)
    print(f"Completed Phase! Logged {len(latencies)} results. Observed Mean Latency: {round(avg, 4)} ms")

def main():
    print("=== STARTING CAPSTONE EXPERIMENTAL EXECUTION PIPELINE ===")
    
    # 1. RUN UNINDEXED BASELINE
    trigger_index_state(is_enabled=False)
    execute_simulation_phase("baseline_results.csv")
    
    # 2. RUN INDEXED EVALUATION
    trigger_index_state(is_enabled=True)
    execute_simulation_phase("indexed_results.csv")
    
    print("\n=== DATA COLLECTION COMPLETE! RESULTS EXPORTED TO CSV SPreadsHEETS ===")

if __name__ == "__main__":
    main()
