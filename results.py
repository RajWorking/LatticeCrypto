import matplotlib.pyplot as plt

t = [100, 1000, 10000, 20000, 70000, 100000]
s = [0.02139, 0.03458, 0.11499,  0.22753, 0.98822, 1.72572]
v = [0.03291, 0.04646, 0.12552,  0.25988, 0.97056, 1.53094]

plt.plot(t, s, label='sign')
plt.plot(t, v, label='ver')
plt.legend()
plt.show()
