import random
import numpy as np
#随机漫步模拟
position = 0
walk = [position]

steps = 1000

for i in range(steps):
    step = 1 if random.randint(0,1) else -1
    position += step
    walk.append(position)

#不难看出，这其实就是随机漫步中各步的累积和，可以用一个数组运算来实现

nsteps = 1000
draws = np.random.randint(0,2,size=nsteps)
steps = np.where(draws > 0,1,-1)
walk = steps.cumsum()

walk.min()
walk.max()


#一次模拟多个随机漫步
nwalks = 5000
nsteps = 1000
draws = np.random.randint(0,2,size=(nwalks,nsteps))
steps = np.where(draws > 0,1,-1)
walk = steps.cumsum(1)


#我们来计算30或-30的最小穿越时间
hits30 = (np.abs(walk) >= 30).any(1)
print(hits30)
#到达30或者-30的数量
print(hits30.sum())

#获取平均穿越时间
crossing_times = (np.abs(walk[hits30]) >= 30).argmax(1)
print(crossing_times.mean())
