#-*- coding: utf-8 -*-
import pandas as pd
import pylab as plt
import numpy as np

#加载数据
fec = pd.read_csv('datasets/fec/P00000001-ALL.csv')
#print(fec[:10])
#print(fec.ix[123456])
#数据中没有党派信息，把它加进去，通过unique，获取全部的候选人名单
unique_cands = fec.cand_nm.unique()
#print(unique_cands)
#利用字典说明党派关系
parties = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}

#print(fec.cand_nm[123456:123461])
#print(fec.cand_nm[123456:123461].map(parties))

#将其添加为一个新列
fec['party'] = fec.cand_nm.map(parties)
#print(fec['party'].value_counts())

#该数据既包括赞助也包括退款（负的出资额）
#print((fec.contb_receipt_amt > 0).value_counts())
#删除负的出资额
fec = fec[fec.contb_receipt_amt > 0]
#针对Barack Obama和Mitt Romney是最主要的两名候选人，我们专门准备子集，分析这两个人的竞选信息
fec_mrbo = fec[fec.cand_nm.isin(['Obama, Barack', 'Romney, Mitt'])]
#print(fec_mrbo.contbr_occupation.value_counts()[:10])
#职业和基本工作类型的关系
occ_mapping = {
   'INFORMATION REQUESTED PER BEST EFFORTS' : 'NOT PROVIDED',
   'INFORMATION REQUESTED' : 'NOT PROVIDED',
   'INFORMATION REQUESTED (BEST EFFORTS)' : 'NOT PROVIDED',
   'C.E.O.': 'CEO'
}
# 如果没有提供相关映射，则返回x
f = lambda x: occ_mapping.get(x, x)
fec.contbr_occupation = fec.contbr_occupation.map(f)
#雇主信息做处理
emp_mapping = {
   'INFORMATION REQUESTED PER BEST EFFORTS' : 'NOT PROVIDED',
   'INFORMATION REQUESTED' : 'NOT PROVIDED',
   'SELF' : 'SELF-EMPLOYED',
   'SELF EMPLOYED' : 'SELF-EMPLOYED',
}
#如果没有提供相关映射，则返回x
f = lambda x: emp_mapping.get(x, x)
fec.contbr_employer = fec.contbr_employer.map(f)

#通过pivot_table根据党派和职业对数据进行聚合，过滤掉总出资额不足200w美元的数据
by_occupation = fec.pivot_table('contb_receipt_amt', index='contbr_occupation',columns='party',aggfunc=sum)
over_2mm = by_occupation[by_occupation.sum(1) > 2000000]
#print(over_2mm)
over_2mm.plot(kind='barh')

#plt.show()

def get_top_amounts(group,key,n=5):
    totals = group.groupby(key)['contb_receipt_amt'].sum()
    #根据key对totals进行降序排列
    return totals.nlargest(n)

#根据职业和雇主进行聚合
grouped = fec_mrbo.groupby('cand_nm')
grouped.apply(get_top_amounts,'contbr_occupation',n=7)
grouped.apply(get_top_amounts,'contbr_employer',n=10)

#根据出资额的大小将数据离散化到多个面元中
bins = np.array([0, 1, 10, 100, 1000, 10000,
                 100000, 1000000, 10000000])
labels = pd.cut(fec_mrbo.contb_receipt_amt,bins)
#print(labels)
#根据候选人姓名以及面元标签对数据进行分组
grouped = fec_mrbo.groupby(['cand_nm',labels])
grouped.size().unstack(0)
#在小额赞助方面，obama获得的数量比romney多得多，还可以对出资额求和并在面元内规格化，以便图形化显示两位候选人的各种赞助额度的比例
bucket_sums = grouped.contb_receipt_amt.sum().unstack(0)
normed_sums = bucket_sums.div(bucket_sums.sum(axis=1), axis=0)
normed_sums[:-2].plot(kind='barh')

#plt.show()
#根据州统计赞助信息
grouped = fec_mrbo.groupby(['cand_nm','contbr_st'])
totals = grouped.contb_receipt_amt.sum().unstack(0).fillna(0)
totals = totals[totals.sum(1) > 100000]
percent = totals.div(totals.sum(1),axis=0)
#print(percent)
percent.plot(kind='barh')


#plt.show()
