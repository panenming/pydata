import json
from collections import Counter
from pandas import DataFrame,Series
import pandas as pd
import numpy as np
import pylab as plt

path = 'datasets/bitly_usagov/example.txt'

#循环读取每行数据转化为json
records = [json.loads(line) for line in open(path)]

#对时区进行计数
time_zones = [rec['tz'] for rec in records if 'tz' in rec]

#计数方法
def get_counts(sequence):
    counts = {}
    for x in  sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts

counts = get_counts(time_zones)

#获取排行top 10 的时区(默认是10)
def top_counts(count_dict,n =10):
    value_key_pairs = [(count,tz) for tz,count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]

top_counts(counts)

#使用python标准库获取排行前十的数据
counts = Counter(time_zones)
counts.most_common(10)

#使用pandas对时区进行计数
frame = DataFrame(records)
frame['tz'][:10]
tz_counts = frame['tz'].value_counts()
#print(tz_counts[:10])

#绘图
#为未知或者空时区填上一个替代值
clean_tz = frame['tz'].fillna('Missing')
#print("-----",clean_tz[clean_tz==''])
clean_tz[clean_tz==''] = 'Unknown'
tz_counts = clean_tz.value_counts()
#print(tz_counts[:10])

#利用counts对象的plot方法即可得到一张水平条形表 plt.show()必须的
tz_counts[:10].plot(kind='barh',rot=0)
#plt.show()

#解析agent字段信息，正则表达式
results = Series([x.split()[0] for x in frame.a.dropna()])
agent_counts = results.value_counts()
agent_counts[:10].plot(kind='barh',rot=0)
#plt.show()
# 按照windows用户和非windows用户对时区统计信息进行分类
cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'),'Windows','Not Windows')
#print(operating_system[:5])
by_tz_os = cframe.groupby(['tz',operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)
#print(agg_counts[:5])
indexer = agg_counts.sum(1).argsort()
#print(indexer[:10])
#去最后十行
count_subset = agg_counts.take(indexer)[-10:]
#print(count_subset)
count_subset.plot(kind='barh',stacked=True)
normed_subset = count_subset.div(count_subset.sum(1),axis=0)
normed_subset.plot(kind='barh',stacked=True)
#plt.show()











