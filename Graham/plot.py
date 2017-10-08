import numpy as np
import matplotlib.pylab as plt
import pandas as pd

df = pd.read_csv('points.csv')

pid = df.x.map(str).str[:6] + "," + df.y.map(str).str[:6]

fig, ax = plt.subplots()
ax.plot(df.x,df.y, ls="", marker="o")
for xi, yi, pidi in zip(df.x,df.y,pid):
    ax.annotate(str(pidi), xy=(xi,yi))


plt.show()
