IT12
# IT12 Rough cut · Three Jigs warm-up

# 1. inspect(dia) → bin label
def inspect(dia):
    if dia < 10:
        return "Small"
    elif dia < 20:
        return "Medium"
    else:
        return "Large"


# Test inspect()
print("inspect tests:")
print(inspect(5))
print(inspect(15))
print(inspect(25))


# 2. tally(labels) → count dictionary
def tally(labels):
    counts = {}
    for label in labels:
        if label in counts:
            counts[label] += 1
        else:
            counts[label] = 1
    return counts


# Test tally()
print("\ntally test:")
print(tally(["Small", "Medium", "Small", "Large", "Medium"]))


# 3. report(shift, counts) → formatted line
def report(shift, counts):
    return f"Shift {shift}: {counts}"


# Test report()
print("\nreport test:")
print(report("A", {"Small": 2, "Medium": 2, "Large": 1}))


# 4. Combine everything
print("\nCombined test:")

diameters = [5, 12, 8, 22, 15, 25]

labels = []
for dia in diameters:
    labels.append(inspect(dia))

counts = tally(labels)

print(report("A", counts))
IT10
# Before refactoring: 24 lines
# After refactoring: 17 lines
# Difference: 7 lines saved

def inspect(dia):
    if dia < 10:
        return "Small"
    elif dia < 20:
        return "Medium"
    return "Large"


def tally(labels):
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    return counts


def report(shift, counts):
    return f"Shift {shift}: {counts}"


diameters = [5, 12, 8, 22, 15, 25]
labels = [inspect(d) for d in diameters]
counts = tally(labels)
print(report("A", counts))

IT08
def inspect(dia):
    if dia < 10:
        return "Small"
    elif dia < 20:
        return "Medium"
    return "Large"


def lookup(catalogue, code):
    return catalogue.get(code, 0)


def scrap_codes(catalogue):
    return {code for code, dia in catalogue.items()
            if dia < 10 or dia > 20}


# Parsed log lines
logs = [
    "P101,12",
    "P102,25",
    "P103,8",
    "P104,15"
]

# Build {part_code: diameter}
catalogue = {}
for line in logs:
    code, dia = line.split(",")
    catalogue[code] = float(dia)

print("Catalogue:", catalogue)

print("Lookup P101:", lookup(catalogue, "P101"))
print("Lookup P999:", lookup(catalogue, "P999"))

print("Scrap codes:", scrap_codes(catalogue))

IT06
def inspect(dia):
    if dia < 10:
        return "Small"
    elif dia < 20:
        return "Medium"
    return "Large"

def lookup(catalogue, code):
    return catalogue.get(code, 0)

def scrap_codes(catalogue):
    return {code for code, dia in catalogue.items() if dia < 10 or dia > 20}

def tally(labels):
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    return counts

def report(shift, counts):
    return f"Shift {shift}: {counts}"

logs = ["P101,12", "P102,25", "P103,8", "P104,15"]
catalogue = {x.split(",")[0]: float(x.split(",")[1]) for x in logs}

labels = [inspect(dia) for dia in catalogue.values()]
counts = tally(labels)

print(report("A", counts))
print("Lookup P999:", lookup(catalogue, "P999"))
print("Scrap:", scrap_codes(catalogue))
