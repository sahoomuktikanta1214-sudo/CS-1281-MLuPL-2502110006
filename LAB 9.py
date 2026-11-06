IT 12
import os

# Create the data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Create test records, including three deliberately faulty ones
records = [
    "WO01 | Machine A | Normal operation",
    "WO02 | Machine B | Completed successfully",
    "WO03 | Machine C | Temperature stable",
    "WO04 | Machine D | Maintenance completed",
    "WO05 | Machine A | No issues reported",
    "WO06 | Machine B | Oil level checked",
    "WO07 | Machine C | Running normally",

    # Three deliberately filthy records
    "WO08 | Machine X | ERROR: Temperature = -9999",
    "WO08 | ??? | NULL | !!! | BROKEN DATA",
    "WO08 | Machine Z | Pressure = HIGHHIGHHIGH",

    "WO09 | Machine D | Inspection passed",
    "WO10 | Machine A | Operating normally",
    "WO11 | Machine B | Filter replaced",
    "WO12 | Machine C | Maintenance required",
    "WO13 | Machine D | Shift completed"
]


# Write records to the file
with open("data/shift_log.txt", "w") as file:
    for record in records:
        file.write(record + "\n")

# Read the file back
with open("data/shift_log.txt", "r") as file:
    lines = file.readlines()

# Print the records and line count
print("SHIFT LOG:")
for line in lines:
    print(line.strip())
  
  IT 10
  
import os
import csv

# File paths
input_file = "data/shift_log.txt"
report_file = "data/report.txt"
rejects_file = "data/rejects.csv"

# Storage
valid_records = []
rejected_records = []

# Step 1: Read input file
with open(input_file, "r") as file:
    lines = file.readlines()

# Step 2: Parse and validate
for line_number, line in enumerate(lines, start=1):
    line = line.strip()

    if not line:
        rejected_records.append(
            (line_number, line, "Empty record")
        )
        continue

    parts = [part.strip() for part in line.split("|")]

    if len(parts) != 3:
        rejected_records.append(
            (line_number, line, "Incorrect number of fields")
        )
        continue

    work_order, machine, status = parts

    if not work_order.startswith("WO"):
        rejected_records.append(
            (line_number, line, "Invalid work order")
        )
        continue

    if not machine or machine == "???":
        rejected_records.append(
            (line_number, line, "Invalid machine name")
        )
        continue

    if not status or status == "NULL" or "ERROR" in status:
        rejected_records.append(
            (line_number, line, "Invalid status")
        )
        continue

    if "HIGHHIGHHIGH" in status:
        rejected_records.append(
            (line_number, line, "Invalid pressure value")
        )
        continue

    valid_records.append((work_order, machine, status))

# Step 3: Aggregate valid records
machine_counts = {}

for work_order, machine, status in valid_records:
    machine_counts[machine] = machine_counts.get(machine, 0) + 1

# Step 4: Write human-readable report
with open(report_file, "w") as file:
    file.write("SHIFT LOG REPORT\n")
    file.write("=" * 65 + "\n")
    file.write(
        f"{'WORK ORDER':<15}{'MACHINE':<20}{'STATUS':<30}\n"
    )
    file.write("-" * 65 + "\n")

    for work_order, machine, status in valid_records:
        file.write(
            f"{work_order:<15}{machine:<20}{status:<30}\n"
        )

    file.write("\nMACHINE SUMMARY\n")
    file.write("-" * 30 + "\n")

    for machine, count in machine_counts.items():
        file.write(f"{machine:<20}{count:>5}\n")

    file.write("\n")
    file.write(f"Total input records: {len(lines)}\n")
    file.write(f"Accepted records: {len(valid_records)}\n")
    file.write(f"Rejected records: {len(rejected_records)}\n")

# Step 5: Write rejected records to CSV
with open(rejects_file, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Line Number", "Rejected Record", "Reason"])

    writer.writerows(rejected_records)

# Step 6: Print completion summary
print("FULL PIPELINE COMPLETED")
print("-----------------------")
print("Input records:", len(lines))
print("Accepted records:", len(valid_records))
print("Rejected records:", len(rejected_records))
print("\nOutput files created:")
print(report_file)
print(rejects_file)

  IT 08

import re

# Regex pattern:
# 1. Work order must follow WO + digits
# 2. Machine name is the second field
# 3. Status is the third field
# 4. Allows any spacing around | separators

pattern = re.compile(
    r"^\s*(WO\d+)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*$"
)

def parse_record(line):
    # OLD VERSION: split-based parser
    # parts = [part.strip() for part in line.split("|")]
    # if len(parts) != 3:
    #     return None
    # return parts[0], parts[1], parts[2]

    # NEW VERSION: Regex parser
    match = pattern.fullmatch(line)

    if match:
        work_order, machine, status = match.groups()

        if machine.strip() and status.strip():
            return work_order, machine.strip(), status.strip()

    return None


# Read actual input from file
input_file = "data/shift_log.txt"

valid_records = []
rejected_records = []

with open(input_file, "r") as file:
    for line_number, line in enumerate(file, start=1):
        result = parse_record(line.strip())

        if result:
            valid_records.append(result)
        else:
            rejected_records.append((line_number, line.strip()))

# Display results
print("REGEX PARSER RESULTS")
print("--------------------")

print("Valid records:", len(valid_records))
print("Rejected records:", len(rejected_records))

print("\nAccepted records:")
for record in valid_records:
    print(record)

print("\nRejected records:")
for record in rejected_records:
    print(record)

# Test comparison note:
# Regex parser survived more spacing variations than split().
# Split parser was simpler but did not validate the WO code shape.

  IT 06

import os
import re
import csv
from datetime import datetime
from collections import defaultdict

# Folder and output paths
DATA_DIR = "data"
HISTORY_FILE = os.path.join(DATA_DIR, "run_history.csv")
PLANT_REPORT = os.path.join(DATA_DIR, "plant_summary.txt")

os.makedirs(DATA_DIR, exist_ok=True)

# Regex parser
pattern = re.compile(
    r"^\s*(WO\d+)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*$"
)


def parse_record(line):
    match = pattern.fullmatch(line.strip())

    if not match:
        return None

    work_order, machine, status = match.groups()

    if not machine.strip() or not status.strip():
        return None

    # Reject suspicious test data
    if "NULL" in status or "ERROR" in status:
        return None

    if "HIGHHIGHHIGH" in status:
        return None

    return work_order, machine.strip(), status.strip()


def process_file(file_path):
    valid_records = []
    rejected_records = []
    total_records = 0

    with open(file_path, "r") as file:
        for line_number, line in enumerate(file, start=1):
            total_records += 1

            record = parse_record(line)

            if record:
                valid_records.append(record)
            else:
                rejected_records.append(
                    (line_number, line.strip(), "Invalid record")
                )

    return valid_records, rejected_records, total_records


def write_report(file_name, records, rejected, total):
    report_name = os.path.splitext(file_name)[0] + "_report.txt"
    report_path = os.path.join(DATA_DIR, report_name)

    machine_counts = defaultdict(int)

    for work_order, machine, status in records:
        machine_counts[machine] += 1

    with open(report_path, "w") as file:
        file.write("SHIFT REPORT\n")
        file.write("=" * 65 + "\n")

        file.write(
            f"{'WORK ORDER':<15}{'MACHINE':<20}{'STATUS':<30}\n"
        )
        file.write("-" * 65 + "\n")

        for work_order, machine, status in records:
            file.write(
                f"{work_order:<15}{machine:<20}{status:<30}\n"
            )

        file.write("\nMACHINE SUMMARY\n")
        file.write("-" * 30 + "\n")

        for machine, count in sorted(machine_counts.items()):
            file.write(f"{machine:<20}{count:>5}\n")

        file.write("\nTOTALS\n")
        file.write(f"Records processed: {total}\n")
        file.write(f"Accepted records: {len(records)}\n")
        file.write(f"Rejected records: {len(rejected)}\n")

    # Separate reject file for each input
    reject_path = os.path.join(
        DATA_DIR,
        os.path.splitext(file_name)[0] + "_rejects.csv"
    )

    with open(reject_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Line Number", "Rejected Record", "Reason"])
        writer.writerows(rejected)

    return report_path


def update_history(file_name, processed, rejects):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_exists = os.path.exists(HISTORY_FILE)
    needs_header = not file_exists or os.path.getsize(HISTORY_FILE) == 0

    with open(HISTORY_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if needs_header:
            writer.writerow([
                "Timestamp",
                "File Name",
                "Records Processed",
                "Rejects"
            ])

        writer.writerow([
            timestamp,
            file_name,
            processed,
            rejects
        ])


# MAIN BATCH JOB
all_records = []
total_processed = 0
total_rejected = 0
processed_files = []

print("PLANT BATCH JOB")
print("=" * 40)

# Only process source .txt files, not generated reports
for file_name in sorted(os.listdir(DATA_DIR)):

    if not file_name.lower().endswith(".txt"):
        continue


print("\nTotal line count:", len(lines))
