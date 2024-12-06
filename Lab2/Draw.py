import matplotlib.pyplot as plt
x = []
y = []
with open('stats.txt') as f:
    for i in range(5):
        s = f.readline().split()
        x.append(int(s[0]))
        y.append(float(s[1]))

plt.plot(x, y, color='red', marker='o', markersize=7)
plt.xlabel('Количество потоков')
plt.ylabel('Время')
plt.title('График')
plt.show()
