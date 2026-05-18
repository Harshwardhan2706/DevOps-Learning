🧠 Core Concepts
    🔹 1. Module
        Any .py file is a module

        Example:

        monitor.py
    🔹 2. Import Module
        utils.py --
        def greet():
            print("Hello")
        main.py
        import utils

        utils.greet()

    🔹 3. Import Specific Function
        from utils import greet
        greet()

        💡 Cleaner & commonly used

    🔹 4. Reusable Monitoring Module
        monitor.py --
        def get_status(cpu):

            if cpu >= 90:
                return "CRITICAL"

            elif cpu >= 75:
                return "WARNING"

            return "HEALTHY"
        main.py
        from monitor import get_status

        print(get_status(85))

    🔹 5. Package
        Folder containing modules
        Example:
        project/
        │
        ├── monitoring/
        │   ├── cpu.py
        │   └── __init__.py
        │
        └── main.py

    🔹 6. __init__.py
        Makes folder a Python package
        Can be empty.

🛠 Core Script
    monitor.py
    def get_status(cpu):

        if cpu >= 90:
            return "CRITICAL 🚨"

        elif cpu >= 75:
            return "WARNING ⚠️"

        return "HEALTHY ✅"
    main.py
    from monitor import get_status

    servers = [
        {"name": "web-1", "cpu": 85},
        {"name": "db-1", "cpu": 95}
    ]

    for server in servers:

        status = get_status(server["cpu"])

        print(f"{server['name']}: {status}")