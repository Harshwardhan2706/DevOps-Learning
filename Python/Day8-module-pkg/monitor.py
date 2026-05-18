def get_status(cpu):
    if cpu >= 90:
        return "CRITICAL 🚨"
    elif cpu >= 75:
        return "WARNING ⚠️"
    else: 
        return "HEALTHY ✅"