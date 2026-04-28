📘 Day 4 Notes – Data Structures (List & Dictionary)

🎯 Objective
    Store multiple servers & metrics
    Represent real infra data
    Build scalable monitoring scripts

🧠 Core Concepts
    🔹 1. List (Ordered Collection)
        Stores multiple values
        servers = ["web-1", "web-2", "db-1"]
        Common Operations
        servers.append("web-3")   # add
        servers.remove("db-1")    # remove
        print(servers[0])         # access

        💡 Use Case:
        Servers list, pods list, IPs

    🔹 2. Dictionary (Key-Value) ⭐
        Stores structured data (like JSON)
        server = {
            "name": "web-1",
            "cpu": 80,
            "memory": 70
        }
        Access / Update
        print(server["cpu"])
        server["cpu"] = 85
        server["disk"] = 60

        💡 Use Case:
        Configs, metrics, API response

🔥 3. List of Dictionaries (MOST IMPORTANT)
    servers = [
        {"name": "web-1", "cpu": 85},
        {"name": "web-2", "cpu": 60},
        {"name": "db-1", "cpu": 95}
    ]

👉 Real-world structure (used everywhere)

🔹 4. Loop Through Data
    for server in servers:
        print(server["name"], server["cpu"])
    🛠 Core Script (Day 4 Task)
    servers = [
        {"name": "web-1", "cpu": 85},
        {"name": "web-2", "cpu": 60},
        {"name": "db-1", "cpu": 95}
    ]

    for server in servers:
        if server["cpu"] >= 90:
            print(f"{server['name']}: CRITICAL 🚨")
        elif server["cpu"] >= 75:
            print(f"{server['name']}: WARNING ⚠️")
        else:
            print(f"{server['name']}: HEALTHY ✅")

🔥 Advanced (CPU + Memory)
    for server in servers:
        if server["cpu"] >= 90 or server["memory"] >= 90:
            print("CRITICAL")

⚠️ Common Mistakes
    ❌ Missing quotes → server[name] ❌
    ❌ Wrong key → KeyError
    ❌ Confusing list vs dict
    💡 SRE/DevOps Insight
    JSON / YAML → Python dict
    APIs → dict
    Kubernetes configs → dict

    👉 Everything in DevOps = structured data

🔁 Quick Comparison
    Structure	        Purpose
    list	         multiple items
    dict	         structured data
    list of dict	 real infra