🧠 Core Concepts
    🔹 1. try-except
        try:
            # risky code

        except:
            # handle error

        💡 Used to handle failures gracefully

    🔹 2. Handle Specific Exceptions ⭐
        try:
            with open("logs.txt", "r") as file:
                print(file.read())

        except FileNotFoundError:
            print("File not found 🚨")

    🔹 3. Multiple Exceptions
        try:
            number = int(input("Enter number: "))
            result = 10 / number

        except ValueError:
            print("Invalid input")

        except ZeroDivisionError:
            print("Cannot divide by zero")

    🔹 4. finally
        Always runs
        finally:
            print("Execution completed")

        💡 Used for cleanup/logging

    🔹 5. else
        Runs only if no error occurs
        else:
            print("Success")
            
🛠 Core Script
    try:

        with open("logs.txt", "r") as file:

            for line in file:
                print(line.strip())

    except FileNotFoundError:
        print("Log file not found 🚨")

🔥 Safe Monitoring Example
    servers = [
        {"name": "web-1", "cpu": 85},
        {"name": "db-1", "cpu": "high"}
    ]

    for server in servers:

        try:

            cpu = int(server["cpu"])

            if cpu >= 90:
                print("CRITICAL")

        except ValueError:
            print("Invalid CPU Data 🚨")

⚠️ Common Errors
        Error	                    Cause
    FileNotFoundError	        missing file
    ValueError	                wrong input type
    ZeroDivisionError	        divide by zero
    KeyError	                wrong dictionary key


🔁 Quick Summary
        Keyword	                Purpose
        try	                    risky code
        except	                handle errors
        finally	                always executes
        else	                executes if success