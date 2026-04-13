#################### for loop & if/else ########################
# servers = ["web-1", "web-2", "db-1"]
# for server in servers:
#     cpu = int(input(f"Enter CPU for {server}: "))
#     if cpu > 90:
#         print(f"{server} CRITICAL 🚨")
#     elif 75 < cpu < 89:
#         print(f"{server} WARNING ⚠️")
#     else:
#         print(f"{server} HEALTHY ✅")
#################### for + if/else + continuos ##################
# servers = ["web-1", "web-2", "db-1"]
# for server in servers:
#     cpu = int(input(f"Enter CPU for {server}: "))
#     if cpu <= 75:
#         continue # skip healthy server
#     elif 89 > cpu > 75:
#         print(f"{server} WARNING ⚠️")
#     else:
#         print(f"{server} CRITICAL 🚨")
#################### for + if/else + break ##################
# servers = ["web-1", "web-2", "db-1"]
# for server in servers:
#     cpu = int(input(f"Enter CPU for {server}: "))
#     if cpu >= 90:
#         print(f"{server} CRITICAL 🚨")
#         break
#     elif 89 > cpu > 75:
#         print(f"{server} WARNING ⚠️")
#     else:
#         print(f"{server} HEALTHY ✅")
#################### for + if/else + break ##################
# servers = ["web-1", "web-2", "db-1"]
# critical_count = 0
# for server in servers:
#     cpu = int(input(f"Enter CPU for {server}: "))

#     if cpu >= 90:
#         print(f"{server} CRITICAL 🚨")
#         critical_count += 1
# print(f"Number of critical servers: {critical_count}")
#################### while ##################
attempt = 1
while attempt <= 3:
    status = input("Is deployment successful? (Yes/No): ")
    if status == "Yes":
        print("Deployment Successful ✅")
        break
    print(f"Retrying... Attempt {attempt}")
    attempt += 1