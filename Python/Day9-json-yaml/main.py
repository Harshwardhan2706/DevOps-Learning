import json

critical_servers = []

with open("servers.json", "r") as file:
    servers = json.load(file)

    for server in servers:
        if server["cpu"] >= 90:
            critical_servers.append(server)
            print(f"{server['name']}: CRITICAL 🚨")

            with open("critical.json", "w") as file:

                json.dump(critical_servers, file, indent=4)

        elif server["cpu"] >= 75:
            print(f"{server['name']}: WARNING ⚠️")

        else:
            print(f"{server['name']}: HEALTHY ✅")

