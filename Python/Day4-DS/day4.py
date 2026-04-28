servers = [
    {"name": "web-1", "cpu": 85, "memory": 70},
    {"name": "web-2", "cpu": 60, "memory": 50},
    {"name": "db-1", "cpu": 95, "memory": 92},
    {"name": "db-2", "cpu": 91, "memory": 95},
    {"name": "web-3", "cpu": 91, "memory": 95},
    {"name": "db-3", "cpu": 91, "memory": 95},
    {"name": "db-4", "cpu": 78, "memory": 87}
]

critical = 0
warning = 0
healthy = 0

for server in servers:
    if server["cpu"] >= 90 or server["memory"] >= 90:
        critical += 1
        print(f"{server['name']}: CRITICAL 🚨")
    elif server["cpu"] >= 75 or server["memory"] >= 75:
        warning += 1
        print(f"{server['name']}: WARNING ⚠️")
    else:
        healthy += 1
        print(f"{server['name']}: HEALTHY ✅")


print("\n----Summary----")
print(f"No. of Critical servres: {critical}")
print(f"No. of Warning servres: {warning}")
print(f"No. of Healthy servres: {healthy}\n")