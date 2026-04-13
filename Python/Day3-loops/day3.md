📘 Day 3 Notes – Loops (SRE/DevOps Focus)

🎯 Objective
Automate repetitive tasks
Process multiple servers/logs
Build base for bulk monitoring scripts

🧠 Core Concepts
    🔹 1. for Loop (Most Used)
    Iterates over a sequence (list, range, file)
    for item in sequence:
        # execute
    Example:
    servers = ["web-1", "web-2", "db-1"]

    for server in servers:
        print(server)

    💡 Use Case:
    Loop through servers, pods, logs

    🔹 2. while Loop (Condition-Based)
    Runs until condition becomes False
    while condition:
        # execute
    Example:
    count = 1

    while count <= 5:
        print(count)
        count += 1

    💡 Use Case:
    Monitoring loops
    Retry logic
    Wait for service

    🔹 3. break (Exit Loop)
    Stops loop immediately
    for i in range(5):
        if i == 3:
            break

    💡 Use Case:
    Stop on critical error
    Stop retry when success

    🔹 4. continue (Skip Iteration)
    Skips current iteration, continues loop
    for i in range(5):
        if i == 2:
            continue
        print(i)

    💡 Use Case:
    Skip healthy servers
    Ignore INFO logs

🛠 Core Script (Day 3 Task)
    servers = ["web-1", "web-2", "db-1"]

    for server in servers:
        cpu = int(input(f"Enter CPU for {server}: "))

        if cpu < 75:
            continue

        if cpu >= 90:
            print(f"{server}: CRITICAL 🚨")
            break
        else:
            print(f"{server}: WARNING ⚠️")
            
🔥 while Loop (Retry Example)
attempt = 1

while attempt <= 3:
    status = input("Success? (yes/no): ")

    if status == "yes":
        print("Done ✅")
        break

    attempt += 1