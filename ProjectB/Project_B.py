import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
# from mlxtend.preprocessing import TransactionEncoder
# 数据加载
data = pd.read_csv('./订单表.csv', encoding='gbk')
print(data)

#  按照客户分组将订单表分组
products = data.groupby(data['客户ID'])['产品名称'].value_counts().unstack()
products[products > 1] = 1
products[np.isnan(products)] = 0


# 读入转化为0-1编码订单记录，用apriori算法得到频繁项集和关联规则并打印
 # 挖掘频繁项集
frequent_itemsets = apriori(products, min_support=0.05, use_colnames=True)
rules = association_rules(frequent_itemsets, metric='lift', min_threshold=1)
frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False)
print('频繁项集：', frequent_itemsets)
# 挖掘关联规则 
pd.options.display.max_columns = 100
rules = rules.sort_values(by='lift', ascending=False)
print('关联规则：', rules)