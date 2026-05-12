# def get_status(cpu, memory):
#     if cpu >= 90 or memory >= 90:
#         return "CRITICAL"
#     elif cpu >= 75 or memory >= 75:
#         return "WARNING"
#     else:
#         return "HEALTHY"
    
# servers = [
#     {"name": "web-1", "cpu": 85, "memory": 70},
#     {"name": "web-2", "cpu": 60, "memory": 50},
#     {"name": "db-1", "cpu": 95, "memory": 92}
# ]

# for server in servers:   
#     status = get_status(server["cpu"],server["memory"])
# print(f"Server is in {status} state")

def get_status(cpu, memory):
    if cpu >= 90 or memory >= 90:
        return "CRITICAL"
    elif cpu >= 75 or memory >= 75:
        return "WARNING"
    else:
        return "HEALTHY"


def print_summary(critical, warning, healthy):
    print("\n--- Summary ---")
    print(f"Critical: {critical}")
    print(f"Warning: {warning}")
    print(f"Healthy: {healthy}")


servers = [
    {"name": "web-1", "cpu": 85, "memory": 70},
    {"name": "web-2", "cpu": 60, "memory": 50},
    {"name": "db-1", "cpu": 95, "memory": 92},
    {"name": "db-2", "cpu": 91, "memory": 95},
    {"name": "web-3", "cpu": 91, "memory": 95},
    {"name": "db-3", "cpu": 91, "memory": 95},
    {"name": "db-4", "cpu": 78, "memory": 87}
]

critical = warning = healthy = 0

for server in servers:
    status = get_status(server["cpu"], server["memory"])
    print(f"{server['name']}: {status}")

    if status == "CRITICAL":
        critical += 1
    elif status == "WARNING":
        warning += 1
    else:
        healthy += 1

print_summary(critical, warning, healthy)