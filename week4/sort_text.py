"""
作者：Lucifer
日期：2023年03月16日
"""
import datetime


def sort(path):
    """
    对文档按天分类
    """
    get_text = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            text_str = fields[1]
            time_str = fields[2]
            time = datetime.datetime.strptime(time_str, '%a %b %d %H:%M:%S %z %Y').date()
            if time in get_text.keys():
                get_text[time].append(text_str)
            else:
                get_text[time] = [text_str]

        get_text = dict(sorted(get_text.items(), key=lambda x: x[0]))
    return get_text


if __name__ == "__main__":
    print(sort('weibo2.txt'))
