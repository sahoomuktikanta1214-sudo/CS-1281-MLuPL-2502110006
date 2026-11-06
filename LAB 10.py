IT12

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

INPUT_FILE = os.path.join(DATA_DIR, "shift_log.txt")
REPORT_FILE = os.path.join(DATA_DIR, "report.txt")
REJECTS_FILE = os.path.join(DATA_DIR, "rejects.csv")

IT10

import os
import re
import csv
from datetime import datetime
from collections import defaultdict

# ==========================================
# SHIFT LOG PROCESSING SYSTEM
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

HISTORY_FILE = os.path.join(DATA_DIR, "run_history.csv")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# Regex parser: extracts all three fields
PATTERN = re.compile(
    r"^\s*(WO\d+)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*$"
)


# ==========================================
# PARSE AND VALIDATE
# ==========================================

def parse_record(line):

    match = PATTERN.fullmatch(line.strip())

    if not match:
        return None, "Invalid record format"

    work_order, machine, status = match.groups()

    if not machine.strip():
        return None, "Missing machine name"

    if not status.strip():
        return None, "Missing status"

    if "???" in machine:
        return None, "Invalid machine name"

    if "NULL" in line.upper():
        return None, "NULL value found"

    if "ERROR" in status.upper():
        return None, "Error status found"

    if "HIGHHIGHHIGH" in status.upper():
        return None, "Invalid pressure value"

    return (
        (work_order, machine.strip(), status.strip()),
        None
    )


# ==========================================
# PROCESS ONE INPUT FILE
# ==========================================

def process_file(file_path):

    valid_records = []
    rejected_records = []
    total_records = 0

    with open(file_path, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            total_records += 1

            if not line.strip():
                rejected_records.append(
                    (line_number, line.strip(), "Empty record")
                )
                continue

            record, reason = parse_record(line)

            if record:
                valid_records.append(record)
            else:
                rejected_records.append(
                    (line_number, line.strip(), reason)
                )

    return valid_records, rejected_records, total_records


# ==========================================
# GENERATE INDIVIDUAL REPORT
# ==========================================

def write_report(file_name, records, rejected, total):

    base_name = os.path.splitext(file_name)[0]

    report_path = os.path.join(
        REPORT_DIR,
        base_name + "_report.txt"
    )

    machine_counts = defaultdict(int)

    for work_order, machine, status in records:
        machine_counts[machine] += 1

    with open(report_path, "w", encoding="utf-8") as file:

        file.write("SHIFT LOG REPORT\n")
        file.write("=" * 70 + "\n")

        file.write(
            f"{'WORK ORDER':<15}"
            f"{'MACHINE':<20}"
            f"{'STATUS':<35}\n"
        )

        file.write("-" * 70 + "\n")

        for work_order, machine, status in records:

            file.write(
                f"{work_order:<15}"
                f"{machine:<20}"
                f"{status:<35}\n"
            )

        file.write("\nMACHINE SUMMARY\n")
        file.write("-" * 35 + "\n")

        for machine, count in sorted(machine_counts.items()):
            file.write(f"{machine:<25}{count:>5}\n")

        file.write("\nTOTALS\n")
        file.write(f"Records processed: {total}\n")
        file.write(f"Accepted records: {len(records)}\n")
        file.write(f"Rejected records: {len(rejected)}\n")

    # Write rejected records
    reject_path = os.path.join(
        REPORT_DIR,
        base_name + "_rejects.csv"
    )

    with open(
        reject_path, "w", newline="", encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Line Number",
            "Rejected Record",
            "Reason"
        ])

        writer.writerows(rejected)


# ==========================================
# UPDATE RUN HISTORY
# ==========================================

def update_history(file_name, processed, rejects):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    needs_header = (
        not os.path.exists(HISTORY_FILE)
        or os.path.getsize(HISTORY_FILE) == 0
    )

    with open(
        HISTORY_FILE, "a", newline="", encoding="utf-8"
    ) as file:

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


# ==========================================
# COMBINED PLANT SUMMARY
# ==========================================

def write_plant_summary(records, files, processed, rejected):

    summary_path = os.path.join(
        REPORT_DIR,
        "plant_summary.txt"
    )

    machine_counts = defaultdict(int)

    for work_order, machine, status in records:
        machine_counts[machine] += 1

    with open(summary_path, "w", encoding="utf-8") as file:

        file.write("COMBINED PLANT SUMMARY\n")
        file.write("=" * 45 + "\n")

        file.write(f"Files processed: {len(files)}\n")
        file.write(f"Records processed: {processed}\n")
        file.write(f"Accepted records: {len(records)}\n")
        file.write(f"Rejected records: {rejected}\n")

        file.write("\nMACHINE TOTALS\n")
        file.write("-" * 35 + "\n")

        for machine, count in sorted(machine_counts.items()):
            file.write(f"{machine:<25}{count:>5}\n")


# ==========================================
# MAIN BATCH JOB
# ==========================================

def main():

    all_records = []
    total_processed = 0
    total_rejected = 0
    processed_files = []

    try:

        # Find every source TXT file
        input_files = sorted(
            name for name in os.listdir(DATA_DIR)
            if name.lower().endswith(".txt")
        )

        if not input_files:
            print("ERROR: No input TXT files found in data/")
            return

        print("\nSHIFT LOG BATCH PROCESSOR")
        print("=" * 45)

        for file_name in input_files:

            file_path = os.path.join(DATA_DIR, file_name)

            print("\nProcessing:", file_name)

            try:

                records, rejected, total = process_file(file_path)

                write_report(
                    file_name,
                    records,
                    rejected,
                    total
                )

                all_records.extend(records)

                total_processed += total
                total_rejected += len(rejected)

                processed_files.append(file_name)

                update_history(
                    file_name,
                    total,
                    len(rejected)
                )

                print("Accepted:", len(records))
                print("Rejected:", len(rejected))

            except (OSError, UnicodeError) as error:

                print(
                    "ERROR: Could not process",
                    file_name,
                    "-",
                    error
                )

        # Generate combined summary
        if processed_files:

            write_plant_summary(
                all_records,
                processed_files,
                total_processed,
                total_rejected
            )

        print("\n" + "=" * 45)
        print("BATCH JOB COMPLETED")
        print("=" * 45)

        print("Files processed:", len(processed_files))
        print("Total records:", total_processed)
        print("Accepted:", len(all_records))
        print("Rejected:", total_rejected)

        print("\nOUTPUT FILES")
        print("Individual reports:", REPORT_DIR)
        print("Plant summary:", os.path.join(
            REPORT_DIR, "plant_summary.txt"
        ))
        print("Run history:", HISTORY_FILE)

    except (OSError, PermissionError) as error:

        print("SYSTEM ERROR:", error)


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()
  
IT08

git status
git add .
git commit -m "Complete shift log batch processing system v1.0"
git push origin main

IT06
def run_tests():
    print("\nHOSTILE INPUT TEST")
    print("=" * 45)

    test_cases = [
        ("WO01 | Machine A | Normal operation", True),
        ("WO02|Machine B|Completed", True),
        ("WO03   |   Machine C   | Running", True),
        ("XX04 | Machine D | Normal", False),
        ("WO05 | Machine E", False),
        ("WO06 | ??? | NULL", False),
        ("WO07 | Machine G | ERROR: Failure", False),
        ("WO08 | Machine H | Pressure HIGHHIGHHIGH", False),
        ("", False),
        ("WO09 | | Missing machine", False)
    ]

    passed = 0
    failed = 0

    for test_input, expected in test_cases:

        record, reason = parse_record(test_input)

        actual = record is not None

        if actual == expected:
            print("[PASS]", repr(test_input))
            passed += 1
        else:
            print("[FAIL]", repr(test_input))
            print("Expected:", expected)
            print("Actual:", actual)
            failed += 1

    print("\nTEST RESULTS")
    print("Passed:", passed)
    print("Failed:", failed)

    if failed == 0:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")

    return failed == 0

SHIFT LOG REPORT
======================================================================
WORK ORDER     MACHINE             STATUS
----------------------------------------------------------------------
WO01           Machine A           Normal operation
WO02           Machine B           Maintenance completed
WO03           Machine C           Inspection passed
WO04           Machine A           Temperature stable
WO05           Machine B           Filter replaced
WO06           Machine C           Running normally
WO07           Machine D           Inspection completed
WO09           Machine D           Inspection passed
WO10           Machine A           Operating normally
WO11           Machine B           Oil level checked
WO12           Machine C           Maintenance required
WO13           Machine D           Shift completed

MACHINE SUMMARY
-----------------------------------
Machine A                    3
Machine B                    3
Machine C                    3
Machine D                    3

TOTALS
Records processed: 15
Accepted records: 12
Rejected records: 3
