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
#名字的多样性在提升
table = top1000.pivot_table('prop',index='year',columns='sex',aggfunc=sum)
table.plot(yticks=np.linspace(0,1.2,13),xticks=range(1880,2020,10))
pylab.title(u'1000个流行名字所占的比例', fontproperties='SimHei')
#pylab.show()

#方法二 计算占总出生人数前50%的不同名字的数量，我们只考虑2010年男孩的名字

df = boys[boys.year == 2010]
#print(df)
#对prop降序排列后，求的多少个名字加起来才够50%,索引结果要加个1
prop_cumsum = df.sort_values(by='prop',ascending=False).prop.cumsum()
#print(prop_cumsum.searchsorted(0.5))

#拿1900年数据做个对比，数字会小很多
df = boys[boys.year == 1900]
in1900 = df.sort_values(by='prop',ascending=False).prop.cumsum()
#print(in1900.searchsorted(0.5) + 1)

#对所有的year/sex组合执行这个计算
def get_quantile_count(group,q=0.5):
    group = group.sort_values(by='prop',ascending=False)
    return group.prop.cumsum().searchsorted(q) + 1

diversity = top1000.groupby(['year','sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex').astype(float)
#print(diversity.head())
#可以看出女孩名字的多样性高于男孩，而且变得越来越高
diversity.plot(title='Number of popular names in top 50%')
#pylab.show()

#最后一个字母的变革
#男孩女孩名字中各个末字母的比例
get_last_letter = lambda x:x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'

table = names.pivot_table('births',index=last_letters,columns=['sex','year'],aggfunc=sum)
subtable = table.reindex(columns=[1910,1960,2010],level='year')
#print(subtable.head())
letter_prop = subtable / subtable.sum().astype(float)
fig,axes = pylab.subplots(2,1,figsize=(10,8))
letter_prop['M'].plot(kind='bar',rot=0,ax=axes[0],title='Male')
letter_prop['F'].plot(kind='bar',rot=0,ax=axes[1],title='Female',legend=False)
#pylab.show()
#回到以前创建的那个完整的表，按照年度和性别对其进行规范化处理，并在男孩的名字中选取几个字母，最后进行转置以便将各个列做成一个时间序列
#各个年代的男孩名字以d/n/y结尾的比例曲线
letter_prop = table / table.sum().astype(float)
dny_ts = letter_prop.ix[['d','n','y'],'M'].T
dny_ts.plot()
#pylab.show()

#变成女孩名字的男孩名字（以及相反的情况）(以lesl为例)
all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesley_like = all_names[mask]

filtered = top1000[top1000.name.isin(lesley_like)]
filtered.groupby('name').births.sum()
table = filtered.pivot_table('births',index='year',columns='sex',aggfunc=sum)
table = table.div(table.sum(1),axis=0)
table.plot(style={'M':'k-','F':'k--'})
#pylab.show()






