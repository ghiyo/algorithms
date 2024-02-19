from sortedcontainers import SortedDict


d = SortedDict()
d[5] = 1
print(d)
d[4] = 5
print(d)
d[3] = 2
print(not d[5])
print(d.items()[0])
print(d.items()[-1])
