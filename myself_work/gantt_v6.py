import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pandas import Timestamp
from datetime import datetime, timedelta

#
# ##### DATA #####
# data = {'Task':
#                 {0: '攻击面--easm',
#                  1: '资产接入--asset_sync',
#                  2: '暗网信息监测--dark',
#                  3: '互联网监测--internet_monitor',
#                  4: '钓鱼工具--phish_tool',
#                  5: '漏管平台--vuln_module',
#                  6: '数据服务--dataService',
#                  7: '互联网风险扫描工具--goby',
#                  8: '互联网资产排查工具--intenet_easm_tool'},
#
#         'status': {0: 'coding',
#                    1: 'no_started',
#                    2: 'coding',
#                    3: 'finish',
#                    4: 'warn',
#                    5: 'coding',
#                    6: 'finish',
#                    7: 'warn',
#                    8: 'coding'},
#         # c_dict = {'延期-delay': '#FF0000', '风险-warn': '#FFFF00', '开发中-coding': '#90EE90', '未启动no_started': '#808080', '开发完成-finish': '#87CEFA'}
#
# 'Start': {0: Timestamp('2025-01-20'),
#                   1: Timestamp('2025-01-20'),
#                   2: Timestamp('2025-01-10'),
#                   3: Timestamp('2025-03-21'),
#                   4: Timestamp('2025-01-10'),
#                   5: Timestamp('2025-02-05'),
#                   6: Timestamp('2025-01-15'),
#                   7: Timestamp('2025-01-24'),
#                   8: Timestamp('2025-03-10')},
#
#         'End': {0: Timestamp('2025-02-15'),
#                 1: Timestamp('2025-02-10'),
#                 2: Timestamp('2025-03-10'),
#                 3: Timestamp('2025-03-28'),
#                 4: Timestamp('2025-03-10'),
#                 5: Timestamp('2025-04-10'),
#                 6: Timestamp('2025-03-15'),
#                 7: Timestamp('2025-02-10'),
#                 8: Timestamp('2025-04-22')},
#
# 'Completion': {0: 0.0,
#                1: 0.0,
#                2: 0.1,
#                3: 1,
#                4: 0.75,
#                5: 0.95,
#                6: 1,
#                7: 0.75,
#                8: 0.95}}
#
# # 定义任务数据
# tasks = [
#     {"name": "Task 1", "start": "2023-10-01", "end": "2023-10-05"},
#     {"name": "Task 2", "start": "2023-10-03", "end": "2023-10-08"},
#     {"name": "Task 3", "start": "2023-10-06", "end": "2023-10-10"},
#     {"name": "Task 4", "start": "2023-10-09", "end": "2023-10-12"},
# ]

data = [
    {"Task": "攻击面--easm", "status": "coding",  "Start": "2023-10-01", "End": "2023-10-05", "Completion": 0.5, },
    {"Task": "资产接入--asset_sync", "status": "coding",  "Start": "2023-10-03", "End": "2023-10-08", "Completion": 0.5,},
    {"Task": "暗网信息监测--dark",  "status": "coding", "Start": "2023-10-06", "End": "2023-10-10", "Completion": 0.5,},
    {"Task": "互联网监测--internet_monitor",  "status": "coding", "Start": "2023-10-09", "End": "2023-10-12", "Completion": 0.5,},
    {"Task": "互联网监测--internet_monitor", "status": "coding", "Start": "2023-10-09", "End": "2023-10-12", "Completion": 0.5, },

]
# 将日期字符串转换为 datetime 对象
for task in data:
    task["Start"] = Timestamp(task["Start"])
    task["End"] = Timestamp(task["End"])
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

# days between start and current progression of each task
df['current_num'] = (df.days_start_to_end * df.Completion)


# create a column with the color for each department
def color(row):
    c_dict = {'delay': '#FF0000', 'warn': '#FFFF00', 'coding': '#90EE90', 'no_started': '#808080', 'finish': '#87CEFA'}
    return c_dict[row['status']]


df['color'] = df.apply(color, axis=1)

plt.rcParams['font.family']=['Arial Unicode MS'] ## mac

# plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置显示中文字体
# plt.rcParams['axes.unicode_minus'] = False  # 设置正常显示符号
##### PLOT #####
fig, (ax, ax1) = plt.subplots(2, figsize=(16, 3), gridspec_kw={'height_ratios': [6, 1]}, facecolor='#36454F')
ax.set_facecolor('#36454F')

ax1.set_facecolor('#36454F')
# bars
ax.barh(df.Task, df.current_num, left=df.start_num, color=df.color)
ax.barh(df.Task, df.days_start_to_end, left=df.start_num, color=df.color, alpha=0.5)

for idx, row in df.iterrows():
    ax.text(row.end_num + 0.1, idx, f"{int(row.Completion * 100)}%", va='center', alpha=0.8, color='w')
    ax.text(row.start_num - 0.1, idx, row.Task, va='center', ha='right', alpha=0.8, color='w')

# grid lines
ax.set_axisbelow(True)

# 设置x坐标轴（竖线）虚线
ax.xaxis.grid(color='k', linewidth=1, linestyle='dashed', alpha=0.4, which='both')
#设置Y坐标轴上(水平方向)的栅格线
#ax.yaxis.grid(color='r', linestyle='--', linewidth=1,alpha=0.3)
#同时设置两坐标轴上的栅格线
# ax.grid(color='r', linestyle='--', linewidth=1,alpha=0.3)
# ticks
xticks = np.arange(0, df.end_num.max() + 1, 5)
xticks_labels = pd.date_range(proj_start, end=df.End.max()).strftime("%m/%d")

# 主要刻度
ax.set_xticks(xticks)
# 给主要刻度设置标签
ax.set_xticklabels(xticks_labels[::5], color='w')

'''
Axes.tick_params(axis='both', **kwargs)
参数:
axis :  {'x', 'y', 'both'} 选择对哪个轴操作，默认是'both'
reset :  bool If True, set all parameters to defaults before processing other keyword arguments. Default is False.
which :  {'major', 'minor', 'both'} 选择对主or副坐标轴进行操作
direction/tickdir : {'in', 'out', 'inout'}刻度线的方向
size/length : float, 刻度线的长度
width :  float, 刻度线的宽度
color :  刻度线的颜色
pad :  float, 刻度线与刻度值之间的距离
labelsize :  float/str, 刻度值字体大小
labelcolor : 刻度值颜色
colors :  同时设置刻度线和刻度值的颜色
zorder : float Tick and label zorder.
bottom, top, left, right : bool, 分别表示上下左右四边，是否显示刻度线，True为显示
labelbottom, labeltop, labelleft, labelright :bool, 分别表示上下左右四边，是否显示刻度值，True为显示
labelrotation : 刻度值逆时针旋转给定的度数，如20
gridOn: bool ,是否添加网格线； grid_alpha:float网格线透明度 ； grid_color: 网格线颜色;  grid_linewidth:float网格线宽度； grid_linestyle: 网格线型 
tick1On, tick2On : bool分别表表示是否显示axis轴的(左/下、右/上)or(主、副)刻度线
label1On,label2On : bool分别表表示是否显示axis轴的(左/下、右/上)or(主、副)刻度值

ALL param:
['size', 'width', 'color', 'tickdir', 'pad', 'labelsize', 'labelcolor', 'zorder', 'gridOn', 'tick1On', 'tick2On', 
'label1On', 'label2On', 'length', 'direction', 'left', 'bottom', 'right', 'top', 'labelleft', 'labelbottom', 'labelright',
 'labeltop', 'labelrotation', 'grid_agg_filter', 'grid_alpha', 'grid_animated', 'grid_antialiased', 'grid_clip_box', 
 'grid_clip_on', 'grid_clip_path', 'grid_color', 'grid_contains', 'grid_dash_capstyle', 'grid_dash_joinstyle', 'grid_dashes', 
 'grid_drawstyle', 'grid_figure', 'grid_fillstyle', 'grid_gid', 'grid_label', 'grid_linestyle', 'grid_linewidth', 'grid_marker', 
 'grid_markeredgecolor', 'grid_markeredgewidth', 'grid_markerfacecolor', 'grid_markerfacecoloralt', 'grid_markersize', 
 'grid_markevery', 'grid_path_effects', 'grid_picker', 'grid_pickradius', 'grid_rasterized', 'grid_sketch_params', 'grid_snap', 
 'grid_solid_capstyle', 'grid_solid_joinstyle', 'grid_transform', 'grid_url', 'grid_visible', 'grid_xdata', 'grid_ydata', 
 'grid_zorder', 'grid_aa', 'grid_c', 'grid_ls', 'grid_lw', 'grid_mec', 'grid_mew', 'grid_mfc', 'grid_mfcalt', 'grid_ms']
'''


# 次要刻度,设置虚线(次要刻度)和步进数
xticks_minor = np.arange(0, df.end_num.max() + 2, 1)
ax.set_xticks(xticks_minor, minor=True)

y_positions = np.arange(0, len(data) * 2, 2)  # 步长为2，间隔增大
ax.set_yticks(y_positions)
# ax.set_yticklabels([task["Task"] for task in data])

# y轴去掉
# ax.set_yticks([])

# 设置x轴为白色
plt.setp([ax.get_xticklines()], color='w')

# align x axis x轴范围
ax.set_xlim(0, df.end_num.max())

# remove spines 隐藏对应坐标的线 和给对应的线上色
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['left'].set_position(('outward', 10))
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_color('w')

# 画布标题
plt.suptitle('work schedule', color='w')

##### LEGENDS ##### 第二块画布， https://developer.baidu.com/article/details/1934385
legend_elements = [Patch(facecolor='#FF0000', label='delay'),
                   Patch(facecolor='#FFFF00', label='warn'),
                   Patch(facecolor='#808080', label='no_started'),
                   Patch(facecolor='#90EE90', label='coding'),
                   Patch(facecolor='#87CEFA', label='finish')]
# legend函数用于标出一个图例。loc参数，用于控制图例的位置。 https://blog.csdn.net/qq_35240640/article/details/89478439

# 显示图例
'''loc:图例位置， 
   fontsize：字体大小，
   frameon：是否显示图例边框，
   ncol：图例的列的数量，一般为1,
   title:为图例添加标题
   shadow:为图例边框添加阴影,
   markerfirst:True表示图例标签在句柄右侧，false反之，
   markerscale：图例标记为原图标记中的多少倍大小，
   numpoints:表示图例中的句柄上的标记点的个数，一半设为1,
   fancybox:是否将图例框的边角设为圆形
   framealpha:控制图例框的透明度
   borderpad: 图例框内边距
   labelspacing: 图例中条目之间的距离
   handlelength:图例句柄的长度
   bbox_to_anchor: (横向看右，纵向看下),如果要自定义图例位置或者将图例画在坐标外边，用它，比如bbox_to_anchor=(1.4,0.8)，这个一般配合着ax.get_position()，set_position([box.x0, box.y0, box.width*0.8 , box.height])使用
   用不到的参数可以直接去掉,有的参数没写进去，用得到的话加进去     , bbox_to_anchor=(1.11,0)
'''

'''
https://www.cnblogs.com/zywnnblog/p/15098824.html
'''
legend = ax1.legend(handles=legend_elements, loc='upper center', ncol=5, frameon=False)
plt.setp(legend.get_texts(), color='w')

# clean second axis
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.set_xticks([])
ax1.set_yticks([])
# plt.show()
plt.savefig('gantt_ab1c.png', facecolor='#36454F')