import matplotlib.pyplot as plt

def s(n):
    if n <= 1:
        return 1
    else:
        return s(n-1) + s(n-2) + s(n-3)

size = []
run = []
compare = []
for i in range(0, 25):
    size.append(i)
    run.append(s(i))
    compare.append(1.825**i)

plt.plot(size, run, label='run')
plt.plot(size, compare, label='compare')
plt.legend()
plt.show()