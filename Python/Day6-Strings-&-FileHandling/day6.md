🧠 Core Concepts
    🔹 1. Strings
        Text data inside quotes
        server = "web-1"
        log = "ERROR Disk Full"

    🔹 2. Important String Methods
        Method	Use
        .lower()	lowercase
        .upper()	uppercase
        .strip()	remove spaces/newline
        .split()	split text

        "ERROR" in line	search text
        Examples
        line.strip()
        log.split()
        if "ERROR" in log:
        📂 File Handling

    🔹 Open File
        open("logs.txt", "r")
        Mode	Meaning
        r	read
        w	write
        a	append

    🔹 Best Practice ⭐
        with open("logs.txt", "r") as file:
            print(file.read())
        💡 Automatically closes file

    🔹 Read Line by Line
        with open("logs.txt", "r") as file:
            for line in file:
                print(line.strip())
        💡 Most important pattern for log processing

🛠 Core Script
    with open("logs.txt", "r") as file:

        for line in file:

            line = line.strip()

            if "ERROR" in line:
                print(f"Alert 🚨 -> {line}")

🔥 Count Errors
    error_count = 0

    with open("logs.txt", "r") as file:

        for line in file:

            if "ERROR" in line:
                error_count += 1

    print(error_count)

🚀 Write to File
    with open("output.txt", "w") as file:
        file.write("Server Healthy")