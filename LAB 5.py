IT12

# Raw bench line
line = "P123 25.4 3.5"

# Extract the fields
part_code, dia, shift = line.split()

# Convert diameter to a real float
dia = float(dia)

# Print each value with a label
print("Part code:", part_code)
print("Diameter:", dia)
print("Shift:", shift)

# Prove diameter is a number
print("Diameter + 0.01:", dia + 0.01)

IT10
# 10 log lines with messy spacing
logs = [
    "P101   25.4   A",
    "P102  30.2 B",
    "P103    18.7    C",
    "P104 22.5 D",
    "P105     27.8 E",
    "P106  31.0    F",
    "P107   19.6 G",
    "P108  24.3     H",
    "P109 29.7 I",
    "P110    21.5    J"
]

# One list to store all diameters
diameters = []

# Parse each log line
for line in logs:
    parts = line.split()

    part_code = parts[0]
    diameter = float(parts[1])
    shift = parts[2]

    diameters.append(diameter)

# Report the results
count = len(diameters)
average = sum(diameters) / count
minimum = min(diameters)
maximum = max(diameters)

print("Diameters:", diameters)
print("Count:", count)
print("Average:", average)
print("Minimum:", minimum)
print("Maximum:", maximum)

# Justification:
# A list is used because we want to keep every diameter,
# including duplicate values, and preserve their order.
# A set would remove duplicate values and does not preserve
# the original order in the same way. 

IT08
# 10 messy log lines
logs = [
    "P101   25.4   A",
    "P102  30.2 B",
    "P103    18.7    C",
    "P104 22.5 D",
    "P105     27.8 E",
    "P106  31.0    F",
    "P107   19.6 G",
    "P108  24.3     H",
    "P109 29.7 I",
    "P110    21.5    J"
]

# Three separate bins
accepted = []
rework = []
scrap = []

# Store the part codes that are scrapped
scrap_parts = []

# Parse and classify each log
for line in logs:
    parts = line.split()

    part_code = parts[0]
    diameter = float(parts[1])

    # Example diameter rules:
    # 22 <= diameter <= 28: accepted
    # 20 <= diameter < 22 or 28 < diameter <= 30: rework
    # Otherwise: scrap
    if 22 <= diameter <= 28:
        accepted.append(diameter)

    elif 20 <= diameter < 22 or 28 < diameter <= 30:
        rework.append(diameter)

    else:
        scrap.append(diameter)
        scrap_parts.append(part_code)

# Counts
print("Accepted count:", len(accepted))
print("Rework count:", len(rework))
print("Scrap count:", len(scrap))

# Accepted average
if accepted:
    accepted_average = sum(accepted) / len(accepted)
    print("Accepted average:", accepted_average)
else:
    print("Accepted average: No accepted parts")

# Part codes that were scrapped
print("Scrapped part codes:", scrap_parts)

IT06
# Day-shift log lines
day_logs = [
    "P101   25.4   ACCEPT",
    "P102  30.2   SCRAP",
    "P103    18.7   SCRAP",
    "P104 22.5   ACCEPT",
    "P105     27.8   REWORK",
    "P106  31.0 SCRAP",
    "P107   19.6   SCRAP",
    "P108  24.3   ACCEPT",
    "P109 29.7   REWORK",
    "P110    21.5   ACCEPT"
]

# Night-shift log lines
night_logs = [
    "P101  25.4 ACCEPT",
    "P102    30.2 SCRAP",
    "P103 18.7 SCRAP",
    "P111   23.5 ACCEPT",
    "P112  31.5 SCRAP",
    "P113    27.2 REWORK",
    "P114 19.2 SCRAP",
    "P108   24.3 ACCEPT",
    "P115 29.5 REWORK",
    "P116  21.8 ACCEPT"
]


def parse_shift(logs):
    """Parse one shift and return total parts, accepted count, and scrap codes."""
    accepted_count = 0
    scrap_codes = []

    for line in logs:
        parts = line.split()

        part_code = parts[0]
        status = parts[2]

        if status == "ACCEPT":
            accepted_count += 1
        elif status == "SCRAP":
            scrap_codes.append(part_code)

    return len(logs), accepted_count, scrap_codes


# Parse day and night separately
day_total, day_accepted, day_scrap = parse_shift(day_logs)
night_total, night_accepted, night_scrap = parse_shift(night_logs)

# Calculate accept rates
day_accept_rate = day_accepted / day_total * 100
night_accept_rate = night_accepted / night_total * 100

print("DAY SHIFT")
print("Accept rate:", day_accept_rate, "%")
print("Scrap codes:", day_scrap)

print("\nNIGHT SHIFT")
print("Accept rate:", night_accept_rate, "%")
print("Scrap codes:", night_scrap)


# Convert scrap lists to sets for comparison
day_scrap_set = set(day_scrap)
night_scrap_set = set(night_scrap)

# Parts scrapped in BOTH shifts
scrapped_both = day_scrap_set & night_scrap_set

# Parts unique to the day shift
day_only_scrap = day_scrap_set - night_scrap_set

# Parts unique to the night shift
night_only_scrap = night_scrap_set - day_scrap_set

print("\nSCRAP COMPARISON")
print("Scrapped in both shifts:", sorted(scrapped_both))
print("Scrapped only during day:", sorted(day_only_scrap))
print("Scrapped only during night:", sorted(night_only_scrap))
