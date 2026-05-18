try:

    cpu = int(input("Enter CPU usage: "))

    if cpu > 100:
        print("Invalid CPU Value")

    result = 100 / cpu

    print(result)

except ValueError:
    print("Please enter numbers only 🚨")

except ZeroDivisionError:
    print("CPU cannot be zero 🚨")

# 

servers = [
    {"name": "web-1", "cpu": 85},
    {"name": "db-1", "cpu": "high"}
]

for server in servers:

    try:

        cpu = int(server["cpu"])

        if cpu >= 90:
            print(f"{server['name']}: CRITICAL 🚨")

        elif cpu >= 75:
            print(f"{server['name']}: WARNING ⚠️")

        else:
            print(f"{server['name']}: HEALTHY ✅")

    except ValueError:
        print(f"{server['name']}: Invalid CPU Data 🚨")

    finally:
        print("All execution done")