# -*- coding: UTF-8 -*-
'''
@Project ：CloudFlask 
@File    ：haijiaoapi.py
@IDE     ：PyCharm 
@Author  ：PoorSteven
@Date    ：2023-05-20 18:41 
'''
import requests
import re
import time
import base64
import json
# url = 'https://hjcaecf.com/'

url = 'https://www.haijiao.com/post/details?pid=1105441'
if 'details'  in url:
    url_id = url.split('=')[-1]
    print(f'帖子ID=>{url_id}')
resquest_url = 'https://hj6fdf61.top/api/topic/'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

res = requests.get(url=resquest_url+url_id,headers=headers)
print(f'网站状态码:',res.status_code)
if res.status_code == 200:
    topic_data = res.json()
    if topic_data['success'] == True:
        print('帖子解析成功!')
        # print(topic_data)
        data = topic_data['data']
        #解密
        atob_data_1 = base64.urlsafe_b64decode(data.encode())
        atob_data_2 = base64.urlsafe_b64decode(atob_data_1)
        atob_data_3 = base64.urlsafe_b64decode(atob_data_2)
        data_json = json.loads(atob_data_3.decode())
        print(f'data_json=>{data_json}')
        title = data_json['title']
        print(f'解析视频标题=>{title}')
        # print(data_json['attachments'])
        str_data = str(data_json['attachments'])
        # print(str_data)
        if '.m3u8' in str_data:
            for remote_data in data_json['attachments']:
                if '.m3u8' in remote_data['remoteUrl']:
                    remote_url = remote_data['remoteUrl']
                    m3u8_data = requests.get(url=remote_url)
                    if m3u8_data.status_code == 200:
                        # print(m3u8_data.text)
                        real_url_id = re.findall(r'.*/(.*?)_i.*?.ts',m3u8_data.text,re.S)[0]
                        # print(real_url_id)
                        new_remote_url_list = remote_url.split('/')
                        # print(new_remote_url_list)
                        new_remote_url_list.pop()
                        # print(new_remote_url_list)
                        new_remote_url = '/'.join(new_remote_url_list)+'/'+real_url_id+'_i.m3u8'
                        print(f'真实解析地址=>{new_remote_url}')

        elif 'api/address' in str_data:
            for remote_data in data_json['attachments']:
                if 'api/address' in remote_data['remoteUrl']:
                    remote_url = 'https://hjc72204.top'+ remote_data['remoteUrl']

                    print(f'真实解析地址=>{remote_url}')
        else:
            print('帖子没有付费视频')


    else:
        print(f'帖子返回错误')
else:
    print(f'帖子解析失败')
