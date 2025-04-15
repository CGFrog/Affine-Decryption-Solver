decrypt = [5, 4, 18, 74, 3, 47, 5, 15, 20, 88, 23, 56, 7, 36, 4, 68]
msg = ""

for c in decrypt:
    value = (c ^ 1108) % 2771
    msg += str(value) + " "

print(msg)
