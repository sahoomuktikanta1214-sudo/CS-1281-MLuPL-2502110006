IT12
# Eight hostile inputs from the rig
hostile = [
    "",
    "ABC",
    "12,",
    ",25",
    "12,25,30",
    "abc,25",
    "P101,-5",
    "P101,999999"
]


def parser(line):
    # Current lab05 parser
    code, dia = line.split(",")
    return code, float(dia)


print("Hostile input test:")

for i, test in enumerate(hostile, 1):
    try:
        result = parser(test)
        print(f"Test {i}: PASS -> {result}")
    except Exception as e:
        print(f"Test {i}: KILLED -> {type(e).__name__}: {e}")
      
IT10
hostile = [
    "",
    "ABC",
    "12,",
    ",25",
    "12,25,30",
    "abc,25",
    "P101,-5",
    "P101,999999"
]

rejects = []
parts = []


def parse(line):
    try:
        code, dia = line.split(",")
        dia = float(dia)

        if dia < 0:
            raise ValueError("negative diameter")

        return code, dia

    except ValueError as e:
        rejects.append((line, str(e)))
        return None


for line in hostile:
    result = parse(line)

    if result is not None:
        parts.append(result)


# Guarded average
if parts:
    average = sum(dia for code, dia in parts) / len(parts)
else:
    average = 0


print("Report")
print("Valid parts:", len(parts))
print("Average diameter:", average)

print("\nRejects")
for line, reason in rejects:
    print(f"{line!r} -> {reason}")
  
IT08
id="q7w4az"
class SpecViolation(Exception):
    pass


class Machine:
    def __init__(self, name, limit):
        self.name = name
        self.limit = limit
        self.parts = 0

    def operate(self, speed):
        if speed < 0 or speed > self.limit:
            raise SpecViolation(
                f"{self.name}: speed {speed} is outside limit {self.limit}"
            )

        self.parts += 1
        return f"{self.name} processed job"


machines = [
    Machine("Lathe", 100),
    Machine("Drill", 80),
    Machine("Mill", 120)
]

jobs = [50, 90, 150, 60, 70, 110, 40]

for i, speed in enumerate(jobs, 1):
    machine = machines[(i - 1) % len(machines)]

    try:
        print(machine.operate(speed))
    except SpecViolation as error:
        print("REJECTED:", error)

print("\nFleet Report")
for machine in machines:
    print(machine.name, ":", machine.parts, "parts")
  
IT06
def parse(line):
    try:
        code, dia = line.split(",")
        dia = float(dia)

        if not code.startswith("P"):
            raise ValueError("invalid part code")

        if dia < 0 or dia > 100:
            raise ValueError("diameter out of range")

        return code, dia

    except ValueError:
        return None


def run_tests():
    hostile = [
        "",
        "ABC",
        "12,",
        ",25",
        "12,25,30",
        "abc,25",
        "P101,-5",
        "P101,999999"
    ]

    print("PASS/FAIL TABLE")
    print("-------------------------------")

    for i, line in enumerate(hostile, 1):
        result = parse(line)

        if result is None:
            print(f"Test {i}: PASS - rejected {line!r}")
        else:
            print(f"Test {i}: FAIL - accepted {line!r}")


run_tests()
