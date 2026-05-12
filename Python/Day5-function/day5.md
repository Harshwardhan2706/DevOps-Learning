🧠 Core Concepts
    🔹 1. Function
        Reusable block of code
        def greet():
            print("Hello")
        Call Function
        greet()

    🔹 2. Function with Parameters
        Parameters = input to function
        def check_cpu(cpu):
            print(cpu)
        Call
        check_cpu(80)
    💡 Makes code reusable

    🔹 3. Return Statement ⭐
        Sends value back from function
        def get_status(cpu):
            if cpu >= 90:
                return "CRITICAL"
            else:
                return "HEALTHY"
        Store Output
        status = get_status(95)
        print(status)

    🔹 4. Multiple Parameters
        def check_health(cpu, memory):
            if cpu >= 90 or memory >= 90:
                return "CRITICAL"

        💡 Used for multi-metric checks

🛠 Core Script (Day 5 Task)
    def get_status(cpu, memory):
        if cpu >= 90 or memory >= 90:
            return "CRITICAL 🚨"
        elif cpu >= 75 or memory >= 75:
            return "WARNING ⚠️"
        else:
            return "HEALTHY ✅"


    servers = [
        {"name": "web-1", "cpu": 85, "memory": 70},
        {"name": "db-1", "cpu": 95, "memory": 92}
    ]

    for server in servers:
        status = get_status(server["cpu"], server["memory"])
        print(f"{server['name']}: {status}")

🔥 Summary Function Example
    def print_summary(critical, warning):
        print(f"Critical: {critical}")
        print(f"Warning: {warning}")
    💡 Why Functions Matter

    Without functions ❌:
        Repeated code
        Difficult debugging

    With functions ✅:
        Reusable
        Cleaner code
        Easier maintenance

🧠 SRE/DevOps Insight
    Functions are used for:
        Health checks
        API calls
        Monitoring tools
        Deployment automation

👉 Example:
    def restart_pod(pod_name):