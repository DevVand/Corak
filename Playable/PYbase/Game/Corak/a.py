global a, b
a = 10
b = 20

tempkeep = ["a", "b", "tempkeep"]
print(tempkeep)
print(globals())
temp = globals()
while len(tempkeep) > 1:
    if tempkeep[0] in temp:
        del temp[tempkeep[0]]
        tempkeep.remove(tempkeep[0])
        print(1)
print(globals())