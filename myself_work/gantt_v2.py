import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pandas import Timestamp

##### DATA #####
data = {'Task': {0: 'TSK M',
                 1: 'TSK N',
                 2: 'TSK L',
                 3: 'TSK K',
                 4: 'TSK J',
                 5: 'TSK H',
                 6: 'TSK I',
                 7: 'TSK G',
                 8: 'TSK F',
                 9: 'TSK E',
                 10: 'TSK D',
                 11: 'TSK C',
                 12: 'TSK B',
                 13: 'TSK A'},

        'Department': {0: 'IT',
                       1: 'MKT',
                       2: 'ENG',
                       3: 'PROD',
                       4: 'PROD',
                       5: 'FIN',
                       6: 'MKT',
                       7: 'FIN',
                       8: 'MKT',
                       9: 'ENG',
                       10: 'FIN',
                       11: 'IT',
                       12: 'MKT',
                       13: 'MKT'},

        'Start': {0: Timestamp('2022-03-17 00:00:00'),
                  1: Timestamp('2022-03-17 00:00:00'),
                  2: Timestamp('2022-03-10 00:00:00'),
                  3: Timestamp('2022-03-09 00:00:00'),
                  4: Timestamp('2022-03-04 00:00:00'),
                  5: Timestamp('2022-02-28 00:00:00'),
                  6: Timestamp('2022-02-28 00:00:00'),
                  7: Timestamp('2022-02-27 00:00:00'),
                  8: Timestamp('2022-02-26 00:00:00'),
                  9: Timestamp('2022-02-23 00:00:00'),
                  10: Timestamp('2022-02-22 00:00:00'),
                  11: Timestamp('2022-02-21 00:00:00'),
                  12: Timestamp('2022-02-19 00:00:00'),
                  13: Timestamp('2022-02-15 00:00:00')},

        'End': {0: Timestamp('2022-03-20 00:00:00'),
                1: Timestamp('2022-03-19 00:00:00'),
                2: Timestamp('2022-03-13 00:00:00'),
                3: Timestamp('2022-03-13 00:00:00'),
                4: Timestamp('2022-03-17 00:00:00'),
                5: Timestamp('2022-03-02 00:00:00'),
                6: Timestamp('2022-03-05 00:00:00'),
                7: Timestamp('2022-03-03 00:00:00'),
                8: Timestamp('2022-02-27 00:00:00'),
                9: Timestamp('2022-03-09 00:00:00'),
                10: Timestamp('2022-03-01 00:00:00'),
                11: Timestamp('2022-03-03 00:00:00'),
                12: Timestamp('2022-02-24 00:00:00'),
                13: Timestamp('2022-02-20 00:00:00')},

        'Completion': {0: 0.0,
                       1: 0.0,
                       2: 0.0,
                       3: 0.0,
                       4: 0.0,
                       5: 1.0,
                       6: 0.4,
                       7: 0.7,
                       8: 1.0,
                       9: 0.5,
                       10: 1.0,
                       11: 0.9,
                       12: 1.0,
                       13: 1.0}}

##### DATA PREP #####
df = pd.DataFrame(data)

# project start date
proj_start = df.Start.min()

# number of days from project start to task start
df['start_num'] = (df.Start - proj_start).dt.days

# number of days from project start to end of tasks
df['end_num'] = (df.End - proj_start).dt.days

# days between start and end of each task
df['days_start_to_end'] = df.end_num - df.start_num


# create a column with the color for each department
def color(row):
    c_dict = {'MKT': '#E64646', 'FIN': '#E69646', 'ENG': '#34D05C',
              'PROD': '#34D0C3', 'IT': '#3475D0'}
    return c_dict[row['Department']]


df['color'] = df.apply(color, axis=1)


from matplotlib.patches import Patch

# 创建一个画像和子图 -- 图1
fig, ax = plt.subplots(1, figsize=(16,6))
# 绘制条形图
ax.barh(df.Task, width=df.days_start_to_end, left=df.start_num, color=df.color)
##### LEGENDS #####
c_dict = {'MKT':'#E64646', 'FIN':'#E69646', 'ENG':'#34D05C',
          'PROD':'#34D0C3', 'IT':'#3475D0'}

# Patch 设置区域表面的颜色
legend_elements = [Patch(facecolor=c_dict[i], label=i)  for i in c_dict]
# 给图像加图例，图例是集中于地图一角或一侧的地图上各种符号和颜色所代表内容与指标的说明
plt.legend(handles=legend_elements)


##### TICKS #####
xticks = np.arange(0, df.end_num.max()+1, 3)
xticks_labels = pd.date_range(proj_start, end=df.End.max()).strftime("%m/%d")
xticks_minor = np.arange(0, df.end_num.max()+1, 1)

ax.set_xticks(xticks)
ax.set_xticks(xticks_minor, minor=True)
ax.set_xticklabels(xticks_labels[::3])
plt.show()
