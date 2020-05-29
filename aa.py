import random
d = {'VENEZUELA':'CARACAS', 'CANADA':'OTTAWA'}

list = [0, 0, 0, 0]
print(list)
print(list[0])
list[0] = 4
list[0] = "a"
print(list)
for i in range(4):
    list.append(random.choice(list(d.keys())))

print(list)