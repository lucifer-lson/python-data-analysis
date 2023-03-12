"""
作者：Lucifer
日期：2023年03月09日
"""
import jieba
import random
import matplotlib
import matplotlib.pyplot as plt
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import GeoType

matplotlib.rcParams["font.sans-serif"] = ["SimSun"]  # 设置字体
matplotlib.rcParams["axes.unicode_minus"] = False


def All_path():  # 获得所有情绪词典的路径
    anger_p = 'D:\\PycharmProjects\\python_2023\\week3\\anger.txt'
    disgust_p = 'D:\\PycharmProjects\\python_2023\\week3\\disgust.txt'
    fear_p = 'D:\\PycharmProjects\\python_2023\\week3\\fear.txt'
    joy_p = 'D:\\PycharmProjects\\python_2023\\week3\\joy.txt'
    sadness_p = 'D:\\PycharmProjects\\python_2023\\week3\\sadness.txt'
    path_list = [anger_p, disgust_p, fear_p, joy_p, sadness_p]
    return path_list


def addToDict():  # 将情绪词典加入jieba的自定义词典
    path_list = All_path()
    for i in path_list:
        jieba.load_userdict(i)


def load_txt(path):  # 加载文件
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def get_clear_text(text):  # 对文本进行停用词清除
    ts = []
    for word in jieba.lcut(text):
        if (word not in load_txt('stop_words.txt')) and (word != ' '):
            ts.append(word)
    return ts


def find_max(lis):  # 一个比大小的函数，根据mood的频数得到最终该条微博的情绪结论判断
    temp0 = []
    if lis[0][1] == 0:
        return 'neutral'
    else:
        for i in range(len(lis)):
            if lis[i][1] == lis[0][1]:
                temp0.append(lis[i])
        x = random.randint(1, len(temp0))
        return temp0[x - 1][0]


def get_mood():
    """ 得到单条微博的情感倾向(anger/disgust/fear/joy/sadness/neutral) """
    mood_list = []  # 存放五个情绪词典读取后的文本
    path_list = All_path()
    for i in path_list:
        mood_list.append(load_txt(i))

    def count_mood(word_list):  # 分析单条文本的情绪
        nonlocal mood_list
        mood_counter = {'anger': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'sadness': 0}
        for i in word_list:
            for j in range(len(mood_list)):
                if i in mood_list[j]:
                    mood_counter[list(mood_counter.keys())[j]] += 1
                    break
        temp = sorted(mood_counter.items(), key=lambda x: x[1], reverse=True)
        return find_max(temp)
    return count_mood


def time_mood_consequence():
    """ 获取微博的情绪、时间、经纬度序列 """
    all_mood = []  # 存放整个文件中每条微博情绪的合集
    all_time = []  # 存放整个文件中每条微博的发布时间
    all_spot = []  # 存放整个文件中每条微博的发布地经纬度
    a = get_mood()
    with open('weibo.txt', 'r', encoding='utf-8') as f:
        for line in f:
            content = line.strip().split('\t')
            ts = get_clear_text(content[1])
            single_mood = a(ts)
            all_mood.append(single_mood)
            tm = get_clear_text(content[2])
            all_time.append(tm)
            tp = get_clear_text(content[0])
            all_spot.append(tp)
    return all_mood, all_time, all_spot


def time_mood_mode(mood, all_mood, all_time):
    """ 得到五种情绪分别随小时、周、月变化的列表 """
    hour_list_anger = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0,
                       15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0}
    hour_list_disgust = hour_list_anger.copy()
    hour_list_fear = hour_list_anger.copy()
    hour_list_joy = hour_list_anger.copy()
    hour_list_sadness = hour_list_anger.copy()
    week_list_anger = {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0, 'Sun': 0}
    week_list_disgust = week_list_anger.copy()
    week_list_fear = week_list_anger.copy()
    week_list_joy = week_list_anger.copy()
    week_list_sadness = week_list_anger.copy()
    month_list_anger = {'Jan': 0, 'Feb': 0, 'Mar': 0, 'Apr': 0, 'May': 0, 'Jun': 0, 'Jul': 0, 'Aug': 0,
                        'Sep': 0, 'Oct': 0, 'Nov': 0, 'Dec': 0}
    month_list_disgust = month_list_anger.copy()
    month_list_fear = month_list_anger.copy()
    month_list_joy = month_list_anger.copy()
    month_list_sadness = month_list_anger.copy()
    for i in range(len(all_mood)):
        if all_mood[i] == 'anger':
            hour_list_anger[int(all_time[i][3])] += 1
            week_list_anger[all_time[i][0]] += 1
            month_list_anger[all_time[i][1]] += 1
        elif all_mood[i] == 'disgust':
            hour_list_disgust[int(all_time[i][3])] += 1
            week_list_disgust[all_time[i][0]] += 1
            month_list_disgust[all_time[i][1]] += 1
        elif all_mood[i] == 'fear':
            hour_list_fear[int(all_time[i][3])] += 1
            week_list_fear[all_time[i][0]] += 1
            month_list_fear[all_time[i][1]] += 1
        elif all_mood[i] == 'joy':
            hour_list_joy[int(all_time[i][3])] += 1
            week_list_joy[all_time[i][0]] += 1
            month_list_joy[all_time[i][1]] += 1
        elif all_mood[i] == 'sadness':
            hour_list_sadness[int(all_time[i][3])] += 1
            week_list_sadness[all_time[i][0]] += 1
            month_list_sadness[all_time[i][1]] += 1
    if mood == 'anger':
        return [hour_list_anger, week_list_anger, month_list_anger]
    elif mood == 'disgust':
        return [hour_list_disgust, week_list_disgust, month_list_disgust]
    elif mood == 'fear':
        return [hour_list_fear, week_list_fear, month_list_fear]
    elif mood == 'joy':
        return [hour_list_joy, week_list_joy, month_list_joy]
    elif mood == 'sadness':
        return [hour_list_sadness, week_list_sadness, month_list_sadness]
    else:  # 不提供其他情绪的查询服务
        return "404 not found"


def plot_mode(mode, mood, all_mood, all_time):  # mode = 'week'/'month'/'hour'  mood = 'anger'/……
    """ 作出用户所需要的对应情绪(mood)和模式(mode)的折线图 """
    temp = {'hour': 0, 'week': 1, 'month': 2}
    dic = time_mood_mode(mood, all_mood, all_time)[temp[mode]]
    x_list = list(dic.keys())
    y_list = list(dic.values())
    plt.figure(figsize=(12.8, 7.2))
    plt.plot(x_list, y_list)
    plt.title(mood + ' with ' + mode)  # 设置子图标题
    plt.xlabel(mode)  # 设置横纵坐标轴标签
    plt.ylabel("times")
    plt.show()


def plot_Geo(all_spot, all_mood):
    """ 作出情绪在空间中的分布图（仅取1000条数据） """
    g = Geo()
    g.add_schema(maptype="北京")
    data_pair = []
    mood_set = {'joy': 5, 'sadness': 15, 'fear': 25, 'disgust': 35, 'anger': 45}
    for i in range(len(all_spot)):
        if all_mood[i] != 'neutral':
            g.add_coordinate(str(i), all_spot[i][1], all_spot[i][0])
            data_pair.append(('s' + str(i), mood_set[all_mood[i]]))
    g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=5)
    g.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    pieces = [
        {'min': 1, 'max': 10, 'label': 'joy', 'color': '#FCF84D'},
        {'min': 10, 'max': 20, 'label': 'sadness', 'color': '#81AE9F'},
        {'min': 20, 'max': 30, 'label': 'fear', 'color': '#E2C568'},
        {'min': 30, 'max': 40, 'label': 'disgust', 'color': '#3700A4'},
        {'min': 40, 'max': 50, 'label': 'anger', 'color': '#DD0200'}
    ]
    g.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces),
        title_opts=opts.TitleOpts(title="Beijing-mood with space"),
    )
    return g


def main():
    all_mood, all_time, all_spot = time_mood_consequence()
    mode, mood = input().split()
    plot_mode(mode, mood, all_mood, all_time)
    g = plot_Geo(all_spot, all_mood)
    g.render('Beijing-mood with space.html')  # 渲染成html，保存在代码文件的相同目录下


main()
