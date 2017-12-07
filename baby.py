#-*- coding: utf-8 -*-
import pandas as pd
import pylab
import numpy as np
path = 'datasets/babynames'
names1880 = pd.read_csv(path + '/yob1880.txt',names=['name','sex','births'])
#print(names1880)
#按照births列的sex进行扥组小计该年的births(计算1880年出生的男女各多少)
by_sex_births = names1880.groupby('sex').births.sum()
#print(by_sex_births[:10])

#将所有的数据组装到DataFrame中
years = range(1880,2011)
pieces = []
columns = ['name','sex','births']

for year in years:
    filepath = path + '/yob%d.txt' % year
    frame = pd.read_csv(filepath,names=columns)
    frame['year'] = year
    pieces.append(frame)

#将所有的数据整合到一个dataframe中
names = pd.concat(pieces,ignore_index=True)
#print(names[:10])

total_births = names.pivot_table('births',index='year',columns='sex',aggfunc=sum)
#print(total_births.tail())
total_births.plot()
pylab.title(u'按性别和年份统计婴儿出生数量', fontproperties='SimHei')
#pylab.show()


#下面我们来插入一个prop列，用于存放指定名字的婴儿数相对于总出生数的比例
#prop值为0.02表示每100名婴儿中有2名取了当前的这个名字
def add_prop(group):
    # 整数除法会向下圆整
    births = group.births.astype(float)
    group['prop'] = births / births.sum()
    return group

names = names.groupby(['year','sex']).apply(add_prop)
#有效性检查，检查所有分组的prop总和是否为1
assert np.allclose(names.groupby(['year','sex']).prop.sum(),1) == True

#取出数据的子集：每对sex/year组合的前1000个名字
def get_top1000(group):
    return group.sort_values(by='births',ascending=False)[:1000]

grouped = names.groupby(['year','sex'])
top1000 = grouped.apply(get_top1000)
#print(top1000)

#根据这个top1000数据进行分析命名趋势等
#先将top1000按照男女分为两部分
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']
#生成一张按照year和name统计的总的出生数表
total_births = top1000.pivot_table('births',index='year',columns='name',aggfunc=sum)
#print(total_births)

#绘制几个名字的曲线(title中文的问题)
subset = total_births[['John','Harry','Mary','Marilyn']]
subset.plot(subplots=True,figsize=(12,10),grid=False)
#pylab.title(u'这几个名字每年出生的数量', fontproperties='SimHei')
#pylab.show()

#是否最流行的几个名字越来越不被家长采用呢，我们使用计算最流行的1000个名字所占比例的方式，按year和sex进行聚合并绘图
table = top1000.pivot_table('prop',index='year',columns='sex',aggfunc=sum)
table.plot()
pylab.title(u'1000个流行名字所占的比例', fontproperties='SimHei')
pylab.show()


