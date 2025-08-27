users = ["tanya", "mike", "andrey"]
for tanya in users:
    print("testing login:", tanya)
    if tanya == "admin":
        print("Admin login test")
    else:
        print("regular user login test")
