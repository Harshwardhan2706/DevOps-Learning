error_count = 0
warning_count = 0
with open("log.txt", "r") as file:
    for line in file:
        line = line.strip()
        if "ERROR" in line:
            print(f"Alert Found 🚨 -> {line}")
            error_count += 1
        if "WARNING" in line:
            print(f"Warning Found ⚠️ -> {line}")
            warning_count += 1
print(f"Number of Error: {error_count}")
print(f"Number of Warning: {warning_count}")

with open("log.txt", "r") as file, open("errors.txt", "w") as error_file:

    for line in file:

        if "ERROR" in line:
            error_file.write(line)