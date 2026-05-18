🧠 Core Concepts
    🔹 1. JSON
        Structured data format
        Similar to Python dictionary

        Example:

        {
        "name": "web-1",
        "cpu": 85
        }

    🔹 2. Import JSON Module
        import json

    🔹 3. Dict → JSON
        json.dumps(data)

        Example:

        import json

        server = {"name": "web-1"}

        print(json.dumps(server))

    🔹 4. JSON → Dict
        json.loads(data)

        Example:

        import json

        data = '{"cpu": 85}'

        print(json.loads(data))
    
    🔹 5. Read JSON File ⭐
        import json

        with open("servers.json", "r") as file:

            data = json.load(file)

            print(data)

    🔹 6. Write JSON File
        import json

        with open("output.json", "w") as file:

            json.dump(data, file, indent=4)

        💡 indent=4 → formatted output

🔥 YAML Basics

    Example:
    server: web-1
    cpu: 85

    🔹 Install YAML Library
        pip install pyyaml

    🔹 Read YAML File
        import yaml

        with open("config.yaml", "r") as file:

            data = yaml.safe_load(file)

            print(data)
        🛠 Core Script
        servers.json
        [
        {"name": "web-1", "cpu": 85},
        {"name": "db-1", "cpu": 95}
        ]
        Python Script
        import json

        with open("servers.json", "r") as file:

            servers = json.load(file)

            for server in servers:

                if server["cpu"] >= 90:
                    print(f"{server['name']}: CRITICAL 🚨")

                elif server["cpu"] >= 75:
                    print(f"{server['name']}: WARNING ⚠️")

                else:
                    print(f"{server['name']}: HEALTHY ✅")

🔁 Quick Summary
    Function	                Purpose
    json.dumps()	        dict → JSON string
    json.loads()	        JSON string → dict
    json.load()	            read JSON file
    json.dump()	            write JSON file
    yaml.safe_load()	    read YAML