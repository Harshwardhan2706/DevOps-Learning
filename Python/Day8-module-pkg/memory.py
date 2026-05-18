def check_memory(memory):

    if memory >= 90:
        return "CRITICAL"

    return "OK"