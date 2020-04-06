
# matplotlib

凡例
```
plt.legend() # 凡例を表示
```

シンプル
```
import matplotlib.pyplot as plt
plt.xkcd()

x = np.arange(-3, 3, 0.1)
y = np.sin(x)
plt.plot(x, y, c='lightskyblue', label='y = sin(x)')
plt.plot([-3, 3], [-1, 1], c='lightcoral', label='y = 1/3x')
plt.legend()
plt.title('Line Plot')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
```

二軸
```
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()
ax1.set_ylabel('ax1 ylabel')
ax1.plot(data1)

ax2 = ax1.twinx()
ax2.set_ylabel('ax2 ylabel')
ax2.plot(data2)

plt.show()
```

二つのグラフを描画
```
fig, ax1 = plt.subplots(2)

ax1[0].set_ylabel('Traffic Process Rate [%]')
ax1[0].set_ylim([0,120])
ax1[0].set_xlim([xbegin, xend])
ax1[0].plot(idx, vnf0tpr, color="b")
ax1[0].plot(idx, vnf1tpr, color="r")

ax2 = ax1[0].twinx()
ax2.set_ylabel('Traffic Rate [pps]')
ax2.set_xlim([xbegin, xend])
ax2.set_ylim([0, 25000000])
ax2.bar(idx, vnf0traf, color="b")
ax2.bar(idx, vnf1traf, bottom=vnf0traf,color="r")

ax1[1].set_ylabel('Traffic Process Rate [%]')
ax1[1].set_ylim([0,120])
ax1[1].set_xlim([xbegin, xend])
ax1[1].plot(idx, vnf0tpr, color="b")
ax1[1].plot(idx, vnf1tpr, color="r")

ax2 = ax1[1].twinx()
ax2.set_ylabel('Conputer Resourcing [#cores]')
ax2.set_xlim([xbegin, xend])
ax2.set_ylim([0, 10])
ax2.bar(idx, vnf0core, color="b")
ax2.bar(idx, vnf1core, bottom=vnf0core, color="r")
```


