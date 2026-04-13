server = input("Name of the server: ")
CPU = int(input("Cpu usage: "))
memory = int(input("memory usage: "))
print(f"\nChecking server: {server}")
if (CPU > 90 or memory > 90):
    print(f"Status: CRITICAL 🚨  with {CPU}% CPU and {memory}% Memory utilisation")
elif 75 < CPU < 89 or 75< memory < 89 :
    print(f"Status: WARNING ⚠️  with {CPU}% CPU and {memory}% Memory utilisation")
else:
    print(f"Status: HEALTHY ✅  with {CPU}% CPU and {memory}% Memory utilisation")
