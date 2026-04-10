📘 Day 1 Notes – Python Basics (SRE/DevOps Focus)
    🎯 Objective
        Setup Python environment
        Learn core syntax
        Build a basic server status script
    ⚙️ Setup Commands
        python3 --version
        python3 -m venv venv
        source venv/bin/activate   # Mac/Linux
    🧠 Core Concepts
        🔹 1. Variables
            Used to store data
            server_name = "web-01"
            cpu_usage = 80

        🔹 2. Data Types
                Type	Example	Use Case
                str	"server1"	hostnames
                int	80	CPU usage
                float	75.5	metrics
                bool	True/False	health
                list	["srv1","srv2"]	multiple servers
                dict	{"cpu": 80}	configs

        🔹 3. Print (Formatted Output)
            print(f"Server {server_name} CPU is {cpu_usage}%")

            ✅ Preferred → f-strings (clean & readable)

        🔹 4. User Input
            server = input("Enter server: ")
            cpu = int(input("Enter CPU: "))

            ⚠️ Always convert numeric input using int()

        🔹 5. Basic Script Flow
            Take input
            Store in variables
            Print formatted output

    🛠 Day 1 Task (Final Script)
        server_name = input("Enter server name: ")
        cpu_usage = int(input("Enter CPU usage (%): "))
        print("\n--- Server Status ---")
        print(f"Server Name: {server_name}")
        print(f"CPU Usage: {cpu_usage}%")

    🔥 Optional Enhancement
        env = input("Enter environment: ")
        print(f"{server_name} in {env} is using {cpu_usage}% CPU")