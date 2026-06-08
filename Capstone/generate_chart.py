import csv
import os

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Matplotlib package missing. Installing automatically via system pip command...")
    os.system("pip install matplotlib")
    import matplotlib.pyplot as plt

def parse_csv_metrics(target_file):
    if not os.path.exists(target_file):
        print(f"Required spreadsheet source file '{target_file}' not found. Run test_client.py first.")
        return []
    
    numerical_values = []
    with open(target_file, mode="r") as file:
        file_reader = csv.DictReader(file)
        for line in file_reader:
            numerical_values.append(float(line["LatencyMS"]))
    return numerical_values

def main():
    # Read the data arrays generated during your execution client sweeps
    unindexed_line = parse_csv_metrics("baseline_results.csv")
    indexed_line = parse_csv_metrics("indexed_results.csv")
    
    if not unindexed_line or not indexed_line:
        print("Aborting chart compilation due to missing spreadsheet records.")
        return

    # Initialize a clean canvas plot configuration layout
    plt.figure(figsize=(10, 5.5))
    
    # Construct the tracking performance lines
    plt.plot(unindexed_line, label="Phase 1: Unindexed Linear Scan O(n)", color="#e74c3c", alpha=0.75, linewidth=1.2)
    plt.plot(indexed_line, label="Phase 2: Indexed B-Tree Lookup O(log n)", color="#2ecc71", alpha=0.90, linewidth=1.2)
    
    # Standard academic title schema and axis definitions
    plt.title("Fountainhead Electronics: Point-of-Sale Subsystem Benchmarking Results", fontsize=13, weight="bold", pad=15)
    plt.xlabel("Sequential Query Sample ID (1 to 1,000)", fontsize=11)
    plt.ylabel("Query Execution Latency Time Parameters (Milliseconds)", fontsize=11)
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.legend(loc="upper right", frameon=True, fontsize=10)
    
    # Save chart artifact as high-density asset for document injection
    output_filename = "latency_comparison_chart.png"
    plt.savefig(output_filename, dpi=300, bbox_inches="tight")
    print(f"\nVisual Artifact Successfully Compiled! Saved file to disk: '{output_filename}'")
    print("You can now open this image and insert it directly into your Capstone report.")

if __name__ == "__main__":
    main()
