IT 12


import random

for i in range(10):
    diameter = random.uniform(24.90, 25.10)
    print(round(diameter, 2))

IT10
import random

accept = 0
rework = 0
scrap = 0

for i in range(100):
    diameter = random.uniform(24.90, 25.10)

    if 24.95 <= diameter <= 25.05:
        bin = "ACCEPT"
        accept += 1
    elif 24.90 <= diameter < 24.95 or 25.05 < diameter <= 25.10:
        bin = "REWORK"
        rework += 1
    else:
        bin = "SCRAP"
        scrap += 1

    print(f"Diameter: {diameter:.2f} -> {bin}")

print("\n--- SHIFT REPORT ---")
print(f"ACCEPT: {accept}")
print(f"REWORK: {rework}")
print(f"SCRAP: {scrap}")
print("\nSame code, ten times the work, zero extra effort.")


IT08
import random

mode = input("Enter mode (halt/skip): ").lower()

accept = 0
rework = 0
scrap = 0
inspected = 0

for i in range(100):
    diameter = random.uniform(24.90, 25.10)
    inspected += 1

    if 24.95 <= diameter <= 25.05:
        bin = "ACCEPT"
        accept += 1

    elif 24.90 <= diameter < 24.95 or 25.05 < diameter <= 25.10:
        bin = "REWORK"
        rework += 1

    else:
        bin = "SCRAP"
        scrap += 1
        print(f"Diameter: {diameter:.2f} -> SCRAP")

        if mode == "halt":
            print("HALT MODE: Scrap detected. Batch stopped.")
            break
        elif mode == "skip":
            print("SKIP MODE: Scrap logged. Continuing batch.")
            continue

    print(f"Diameter: {diameter:.2f} -> {bin}")

print("\n--- SHIFT REPORT ---")
print(f"Mode: {mode.upper()}")
print(f"Inspected: {inspected}")
print(f"ACCEPT: {accept}")
print(f"REWORK: {rework}")
print(f"SCRAP: {scrap}")

IT06
import random

consecutive_accepts = 0
attempts = 0
max_attempts = 500

while consecutive_accepts < 5 and attempts < max_attempts:
    diameter = random.uniform(24.90, 25.10)
    attempts += 1

    if 24.95 <= diameter <= 25.05:
        result = "ACCEPT"
        consecutive_accepts += 1
    else:
        result = "REWORK"
        consecutive_accepts = 0

    print(f"Part {attempts}: {diameter:.2f} -> {result} | Consecutive ACCEPTs: {consecutive_accepts}")

if consecutive_accepts == 5:
    print("\nSUCCESS: Five consecutive ACCEPTs achieved.")
    print(f"Parts required: {attempts}")
else:
    print("\nSAFETY STOP: Maximum attempts reached.")
    print(f"Parts inspected: {attempts}")

print("\nRECORD:")
print("An industrial program uses a safety cap so that an unexpected condition, faulty sensor, bad input, or endless process cannot make the machine run indefinitely.")
