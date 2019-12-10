import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit, OptimizeWarning

x = [1.2, 1.3, 1.4, 1.5, 1.7, 1.9, 2.0]
y = [3.0, 7.3, 11.0, 13.0, 15.0, 19.8, 21.3]
font = {'fontname':'Glacial Indifference'}

def func(x, a, b, c):
    return a * np.log(b * x) + c

popt, pcov = curve_fit(func, x, y)

if OptimizeWarning:
    print("Covariance array has infinite elements.")

fig, ax = plt.subplots()
scat = ax.scatter(x, y, facecolors='none', edgecolors='#ffc252')
fig.canvas.draw()

line = plt.plot(np.asarray(x), func(np.asarray(x), *popt), color='#ffc252', alpha=1.0)[0]
ax.add_line(line)
ax.set_ylabel('I / mA', **font)
ax.set_xlabel(r'N / $\frac{1}{s}$', **font)
plt.rc('grid', linestyle="-", color='#ffc252')
ax.grid(color='#ffc252', linestyle='-')
ax.spines['bottom'].set_color('#ffc252')
ax.spines['top'].set_color('#ffc252') 
ax.spines['right'].set_color('#ffc252')
ax.spines['left'].set_color('#ffc252')
ax.xaxis.label.set_color('#ffc252')
ax.tick_params(axis='x', colors='#ffc252')
ax.yaxis.label.set_color('#ffc252')
ax.tick_params(axis='y', colors='#ffc252')

plt.savefig('2d_physics_graph.png', transparent=True)
# plt.show()
