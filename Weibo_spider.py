# -*- coding: utf-8 -*-
# @Author    : Eurkon
# @Date      : 2021/6/5 10:16

import json
import time
import requests
import os
from http.server import BaseHTTPRequestHandler


def get_data():
    """微博热搜

    Args:
        params (dict): {}

    Returns:
        json: {title: 标题, url: 地址, num: 热度数值, hot: 热搜等级}
    """

    data = []
    response = requests.get("https://weibo.com/ajax/side/hotSearch")
    data_json = response.json()['data']['realtime']
    jyzy = {
        '电影': '影',
        '剧集': '剧',
        '综艺': '综',
        '音乐': '音'
    }

    for data_item in data_json:
        hot = ''
        # 如果是广告，则不添加
        if 'is_ad' in data_item:
            continue
        if 'flag_desc' in data_item:
            hot = jyzy.get(data_item['flag_desc'])
        if 'is_boom' in data_item:
            hot = '爆'
        if 'is_hot' in data_item:
            hot = '热'
        if 'is_fei' in data_item:
            hot = '沸'
        if 'is_new' in data_item:
            hot = '新'

        dic = {
            'title': data_item['note'],
            'url': 'https://s.weibo.com/weibo?q=%23' + data_item['word'] + '%23',
            'num': data_item['num'],
            'hot': hot
        }
        data.append(dic)

    return data


# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         data = get_data()
#         self.send_response(200)
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.send_header('Cache-Control', 'no-cache')
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#         self.wfile.write(json.dumps(data).encode('utf-8'))
#         return


data = get_data()

# 解决存储路径
time_path = time.strftime('%Y{y}%m{m}%d{d}', time.localtime()).format(y='年', m='月', d='日')
time_name = time.strftime('%Y{y}%m{m}%d{d}%H{h}', time.localtime()).format(y='年', m='月', d='日', h='点')
year_path = time.strftime('%Y{y}', time.localtime()).format(y='年')
month_path = time.strftime('%m{m}', time.localtime()).format(m='月')
day_month = time.strftime('%d{d}', time.localtime()).format(d='日')
all_path = "./" + year_path + '/' + month_path + '/' + day_month
if not os.path.exists(all_path):
    # 创建多层路径
    os.makedirs(all_path)

# 最终文件存储位置
root = all_path + "/"
path = root + time_name + '.md'
num = 0
time_name_second = time_name = time.strftime('%Y{y}%m{m}%d{d}%H{h}%M{M}%S{s}', time.localtime()).format(y='年', m='月', d='日', h='点', M = '分',s = '秒')
print(path)
# 文件头部信息
with open(path, 'a') as f:
    f.write('{} {}\n\n'.format('# ', time_name_second + '数据'))
f.close()

for tr in (data):
    title = tr['title']
    hot_score = tr['num']
    hot_level = tr['hot']
    url = tr['url']
    num += 1



    with open(path, 'a') as f:

        f.write('{} {}、{}\n\n'.format('###', num, title))
        f.write('{} {}\n\n'.format('微博当时热度数值为：', hot_score))
        f.write('{} {}\n\n'.format('微博当时热度等级为：', hot_level))
        f.write('[{}]({})\n\n'.format('热搜跳转链接', url))

    f.close()


