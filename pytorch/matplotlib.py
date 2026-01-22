# @Auther   :Mateo
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["font.sans-serif"] = ["SimHei"]

# # 数据
# labels = ['学习', '娱乐', '运动', '睡觉']
# time_spent = [4, 2, 1, 8]
# colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
# explode = (0.1, 0, 0, 0)  # 仅突出第一块，设置突出块，0.1表示突出块离圆心的距离
#
# # 绘制爆炸式饼图
# plt.figure(figsize=(6, 6))
# plt.pie(time_spent, explode=explode, labels=labels, colors=colors,
#         autopct='%.1f%%', shadow=True, startangle=90) # shadow是为饼图加阴影
# plt.title('爆炸式饼图', fontsize=15)
# plt.show()

data = {
    '语文': [82, 85, 88, 70, 90, 76, 84, 83, 95],
    '数学': [75, 80, 79, 93, 88, 82, 87, 89, 92],
    '英语': [70, 72, 68, 65, 78, 80, 85, 90, 95]
}

plt.figure(figsize=(8, 6))
plt.boxplot(data.values(), labels=data.keys())

plt.title("各科成绩分布（箱线图）")
plt.ylabel("分数")
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.show()


def rcParams():
        return None