📘 Day 2 Notes – Conditionals & Alert Logic (SRE Focus)

    🎯 Objective
    Use decision-making in Python
    Build alert logic based on thresholds
    Simulate real monitoring behavior

    🧠 Core Concepts
        🔹 1. Conditionals (if-elif-else)
        if condition:
            # execute
        elif condition:
            # second check
        else:
            # fallback

        🔹 2. Comparison Operators
        Operator	            Meaning	Example
        >	greater than	    cpu > 80
        <	less than	        cpu < 50
        >=	greater/equal	    cpu >= 90
        ==	equal	            status == "down"
        !=	not equal	        env != "prod"

        🔹 3. Logical Operators
        Operator	        Use
        and	                both conditions must be true
        or	                at least one true
        not	                reverse condition
        
        Example:
        if cpu > 80 and memory > 75:
            print("High Load")

        🔹 4. Alert Levels (Important Pattern)
        if cpu >= 90:
            print("CRITICAL 🚨")
        elif cpu >= 75:
            print("WARNING ⚠️")
        else:
            print("HEALTHY ✅")

        💡 Order matters (top → highest priority)

    🛠 Day 2 Task (Core Script)
        server_name = input("Enter server name: ")
        cpu_usage = int(input("Enter CPU usage (%): "))

        print(f"\nChecking server: {server_name}")

        if cpu_usage >= 90:
            print("Status: CRITICAL 🚨")
        elif cpu_usage >= 75:
            print("Status: WARNING ⚠️")
        else:
            print("Status: HEALTHY ✅")

    🔥 Advanced Task (CPU + Memory)
        server = input("Enter server name: ")
        cpu = int(input("Enter CPU usage: "))
        memory = int(input("Enter Memory usage: "))

        if cpu > 90 or memory > 90:
            print("CRITICAL 🚨")
        elif cpu > 75 or memory > 75:
            print("WARNING ⚠️")
        else:
            print("HEALTHY ✅")