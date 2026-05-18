from monitor import get_status
from cpu import check_cpu
from memory import check_memory

servers = [
    {"name": "web-1", "cpu": 85},
    {"name": "db-1", "cpu": 95}
]

for server in servers:
    status = get_status(server["cpu"])

    print(f"{server['name']}: {status}")

print("New------")

print(check_cpu(95))
print(check_memory(70))
