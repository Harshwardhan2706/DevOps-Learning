def check_cpu(cpu):

    if cpu >= 90:
        return "CRITICAL"

    return "OK"