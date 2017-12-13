#-*- coding: utf-8 -*-
#美国农业部制作了一份关于食物营养的数据库，一位英国的技术牛人制作了该数据的json版
#每种食物都带有若干的标识性属性以及两个有关营养成分和分量的列表
import json
from pandas import DataFrame
import pandas as pd
import pylab as plt
db = json.load(open('datasets/usda_food/database.json'))
#db中的每一个条目都是一个含有某种食物的全部数据的字典，nutrients字段是一个字典列表，其中的每一个字典对应一种营养成分
#print(db[0].keys())
#print(db[0]['nutrients'][0])

nutrients = DataFrame(db[0]['nutrients'])
#打印前七个营养成分
#print(nutrients[:7])

#在将字典列表转换为DataFrame时，可以只抽取其中的一部分字段，这里我们取出食物的名称、分类、编号以及制造商等信息
info_keys = ['description','group','id','manufacturer']
info = DataFrame(db,columns=info_keys)
#print(info[:5])
#通过value_counts查看食物的类别分布情况
#print(pd.value_counts(info.group)[:10])

#为了对全部营养数据做一些分析，最简单的方法是将所有的食物的营养成分整合到一个大的表中。
#我们分几个步骤实现该目的，首先将各食物的营养成分列表装换成一个DataFrame，并添加一个表示编号的列
#然后将该DataFrame添加到一个列表中，最后通过concat将这些东西连接起来

nutrients = []
for rec in db:
    fnuts = DataFrame(rec['nutrients'])
    fnuts['id'] = rec['id']
    nutrients.append(fnuts)

nutrients = pd.concat(nutrients,ignore_index=True)

#print(nutrients)

#删除其中的一些重复项
#print(nutrients.duplicated().sum())
nutrients = nutrients.drop_duplicates()
#由于两个DataFrame对象中都有group和description，为了分清到底谁是谁，需要对他们进行重命名
col_mapping = {'description':'food','group':'fgroup'}
info = info.rename(columns=col_mapping,copy=False)
col_mapping = {'description':'nutrient','group':'nutgroup'}
nutrients = nutrients.rename(columns=col_mapping,copy=False)

ndata = pd.merge(nutrients,info,on='id',how='outer')
#print(ndata.iloc[30000])
#根据食物分类和营养类型画出一张中位值图
result = ndata.groupby(['nutrient','fgroup'])['value'].quantile(0.5)
# Zinc Zn的中位值
result['Zinc, Zn'].sort_values().plot(kind='barh')
#plt.show()

#各营养成分最为丰富的食物
by_nutrient = ndata.groupby(['nutgroup','nutrient'])
get_maximum = lambda x: x.xs(x.value.idxmax())
get_minimum = lambda x: x.xs(x.value.idxmin())
max_foods = by_nutrient.apply(get_maximum)[['value','food']]
#让food小一点
max_foods.food = max_foods.food.str[:50]
print(max_foods.ix['Amino Acids']['food'])